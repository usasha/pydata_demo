# Basic multiarmed bandits for microservices
### I made this demo for PyData Moscow october 2018
As we all know, release naming is not easy.
In this example we made couple of algorithms to generate release names:
- adjective + pokemon name
- greek letter + space object name

Also there is a bandits service which will reconfigure routing according 
to user feedback (better algorithm get more requests).

#### quick start:

- intstall docker
- build images:
```
docker build -t model_a model_a
docker build -t model_b model_b
docker build -t bandits bandits
```
- run demo: `docker stack deploy -c docker-compose.yml demo`
- check model weights and server performance on traefik [dashboard](http://localhost:8080/dashboard/)
- stop demo: `docker stack rm demo`
