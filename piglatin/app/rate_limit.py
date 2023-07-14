import redis
    

class RateLimit:
    def __init__(self):
        self.upperLimit = 5
        self.ttl = 60
        self.remainingTries = 0

    def get_limit(self, userToken):
        r = redis.Redis(host='cache', port=6379, decode_responses=True, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")

        if r.get(userToken) is None:
            self.remainingTries = self.upperLimit - 1

            r.setex(userToken, self.ttl, value = self.remainingTries)
        else:
            self.remainingTries = int(r.get(userToken)) - 1

            r.setex(userToken, r.ttl(userToken), value=self.remainingTries)

            self.ttl = r.ttl(userToken)
