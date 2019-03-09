import redis


class ClueLogger:
    def __init__(self, block, model):
        self.block = block
        self.r = redis.StrictRedis('redis')

    def out(self, model, value):
        self.r.xadd(self.block, {'model': model, 'value': value})
