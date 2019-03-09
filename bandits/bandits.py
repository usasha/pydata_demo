import time
from typing import Dict

import docker
import pandas as pd
import redis

RECONFIG_INTERVAL = 15 # seconds
MIN_WEIGHT = 1
WEIGHT_SCALE = 30
TIME_WINDOW = 24 * 60 * 1000  # hours -> milliseconds


class MultiarmedBandit:
    def __init__(self, feedback_path: str, metrics_period: int = None) -> None:
        """
        :param feedback_path: path to tsv file with at least time, model, like/dislike columns
        :param metrics_period: seconds from now to consider feedback
        """
        self.feedback_path = feedback_path
        self.docker = docker.from_env()
        self.metrics_period = metrics_period
        self.r = redis.StrictRedis()

    def calculate_weights(self, services: pd.DataFrame) -> Dict:
        """
        calculate weights for load balancer for each service,
        weights are proportional to precision score but not less than MIN_WEIGHT,
        sum of weights for all services approximately equal to WEIGHT_SCALE

        if service use replication, weight will be divided by replicas number

        :param services: dataframe with active services (block, model, n_replicas, service)
        :return: dict with service as a key and weight as value
        """
        start_time = int(time.time() * 1000) - TIME_WINDOW

        for block in services['block'].unique():
            if block:
                score = self.r.xrange(block, min=start_time, max='+')

        score = pd.DataFrame([x for _, x in score])
        score.columns = [c.decode() for c in score.columns]
        score['like'] = score['like'].astype(int)
        score['model'] = score['model'].apply(lambda x: x.decode())
        score = score.groupby('model', as_index=False).mean()
        score = services.merge(score, on='model')
        score['weight'] = (score['like']
                              / score['like'].sum()
                              * WEIGHT_SCALE
                              / score['replicas']
                              ).fillna(0)

        score['weight'] = score['weight'].astype(int)
        score.loc[score['weight'] == 0, 'weight'] = MIN_WEIGHT

        return score.set_index('service').to_dict()['weight']

    def get_active_services(self) -> pd.DataFrame:
        """
        find all active services (blocks), all models (docker container image) and replication factor

        :return: dataframe with 'service', 'model' and 'replicas' columns
        """
        services = []
        for s in self.docker.services.list():
            service = s.name
            model = s.attrs['Spec']['Labels']['com.docker.stack.image'].split(':')[0]
            block = s.attrs['Spec']['Labels'].get('traefik.backend')
            replicas = s.attrs['Spec']['Mode']['Replicated']['Replicas']
            services.append({'service': service, 'block': block,
                             'model': model, 'replicas': replicas})
        return pd.DataFrame(services)

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
        services = self.get_active_services()
        weights = self.calculate_weights(services)

        for service in weights:
            self.update_service_weight(service, weights[service])


if __name__ == '__main__':
    b = MultiarmedBandit('../data/likes.tsv', RECONFIG_INTERVAL * 3)

    while True:
        time.sleep(RECONFIG_INTERVAL)
        b.reconfigure_load_balancer()
