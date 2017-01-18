import threading
import time

def determineInterval(api):
    return (api.rateDelta / api.rateLimit / len(api.ops)).total_seconds()

def getAndStoreData(namespace, op):
    print(namespace, op["fn"]())

class watcher (threading.Thread):

    def __init__(self, api, exitEvent):
        threading.Thread.__init__(self)
        self.exitEvent = exitEvent
        self.api = api
        self.interval = determineInterval(api)
        self.terminate = False
    
    def run(self):
        while not self.exitEvent.is_set():
            for op in self.api.ops:
                begin=datetime.now()
                getAndStoreData(self.api.name, op)
                duration=(datetime.now() - begin).total_seconds()
                if(duration < self.interval):
                    time.sleep(float(self.interval - duration))
