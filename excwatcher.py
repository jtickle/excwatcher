#!/usr/bin/env python3
import time
import signal
import threading
from datetime import datetime
from apis import *
from libwatcher import *

start = datetime.now()

apis = [coinbase]
threads = []

exitAll = threading.Event()

for api in apis:
    threads.append(watcher(api, exitAll))

for thread in threads:
    thread.start()

def exit_gracefully(signal, frame):
    print("Terminating threads...")
    for thread in threads:
        exitAll.set()

signal.signal(signal.SIGINT, exit_gracefully)

for thread in threads:
    thread.join()
print("Exiting main thread")
