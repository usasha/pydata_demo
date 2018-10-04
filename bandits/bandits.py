import time
from typing import Dict

import docker
import pandas as pd

RECONFIG_INTERVAL = 15 # seconds
MIN_WEIGHT = 1
WEIGHT_SCALE = 30


class MultiarmedBandit:
    def __init__(self, feedback_path: str, metrics_period: int = None) -> None:
        """
        :param feedback_path: path to tsv file with at least time, model, like/dislike columns
        :param metrics_period: seconds from now to consider feedback
        """
        self.feedback_path = feedback_path
        self.docker = docker.from_env()
        self.metrics_period = metrics_period

    def get_metrics(self) -> pd.Series:
        """
        calculate precision for each model
        :return: series with block, with model as index and score as value
        """
        df = pd.read_csv(self.feedback_path, sep='\t', header=None)
        df.rename(columns={0: 'time',
                           1: 'model',
                           2: 'feedback',
                           },
                  inplace=True)

        if self.metrics_period:
            df = df[time.time() - df['time'] < self.metrics_period]

        df['p'] = (df['feedback']
                   .str.replace('dislike', '0')
                   .str.replace('like', '1')
                   .astype(int))

        score = df.groupby('model')['p']
        return score.sum() / score.count()

    def get_active_services(self) -> pd.DataFrame:
        """
        find all active services (blocks), all models (docker container image) and replication factor

        :return: dataframe with 'service', 'model' and 'replicas' columns
        """
        services = []
        for s in self.docker.services.list():
            service = s.name
            model = s.attrs['Spec']['Labels']['com.docker.stack.image'].split(':')[0]
            replicas = s.attrs['Spec']['Mode']['Replicated']['Replicas']
            services.append({'service': service, 'model': model, 'replicas': replicas})
        return pd.DataFrame(services)

    @staticmethod
    def get_services_weights(metrics: pd.Series, services: pd.DataFrame) -> Dict:
        """
        calculate weights for load balancer for each service,
        weights are proportional to precision score but not less than MIN_WEIGHT,
        sum of weights for all services approximately equal to WEIGHT_SCALE

        if service use replication, weight will be divided by replicas number

        :param metrics: dict with model as key and p as value
        :param services: dataframe with active services (model, n_replicas, service)
        :return: dict with service as a key and weight as value
        """
        services = services.merge(pd.DataFrame(metrics), on='model')

        services['weight'] = (services['p']
                              / services['p'].sum()
                              * WEIGHT_SCALE
                              / services['replicas']
                              ).fillna(0)

        services['weight'] = services['weight'].astype(int)
        services.loc[services['weight'] == 0, 'weight'] = MIN_WEIGHT

        return services[['service', 'weight']].set_index('service').to_dict()['weight']

    def update_service_weight(self, name: str, weight: int) -> bool:
        """
        add label f"traefik.weight={weight}" to service
        use of service will be proportional to this weight

        if service is replicated, use of service will be proportional to number_of_replicas * weight

        :param name: name of service
        :param weight: integer weight
        :return: success status
        """
        for s in self.docker.services.list():
            if s.name == name:
                labels = s.attrs['Spec']['Labels']
                labels['traefik.weight'] = str(weight)
                s.update(labels=labels)
                return True

        return False

    def reconfigure_load_balancer(self) -> None:
        """
        reconfigure traefik.weight for services proportional to model precision
        """
        metrics = self.get_metrics()
        services = self.get_active_services()
        weights = self.get_services_weights(metrics, services)

        for service in weights:
            self.update_service_weight(service, weights[service])


if __name__ == '__main__':
    b = MultiarmedBandit('../data/likes.tsv', RECONFIG_INTERVAL * 3)

    while True:
        time.sleep(RECONFIG_INTERVAL)
        b.reconfigure_load_balancer()
