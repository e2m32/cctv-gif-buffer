#!/usr/bin/env python
# Nat Morris (c) 2017
# @E2M32 Edits: Logger stores logfile with timestamps, 
#               added defaults if not set in config,
#               added timeout for http request
#               added more logging
#               
"""CCTV GIF buffer - Service."""

import collections
import imageio
import logging
import requests
import threading
import time
import io

from cctvgifbuffer import version
from cctvgifbuffer.webserver import WebServer
from requests.auth import HTTPBasicAuth

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('service_log.txt', mode='w')
    handler.setFormatter(formatter)
    #screen_handler = logging.StreamHandler(stream=sys.stdout)
    #screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    #logger.addHandler(screen_handler)
    return logger

LOG = setup_custom_logger(__name__)

def camworker(name, config, queue, lock, LOG):
    if "interval" in config:
        snap_interval = config['interval']
    else:
        snap_interval = 1
    if "store" in config:
        img_store_cnt = config['store']
    else:
        img_store_cnt = 30
    LOG.info("%s camworker started." % name)
    while True:
        with lock:
            respargs = {}
            if "auth" in config:
                if config["auth"] == "basic":
                    respargs["auth"] = HTTPBasicAuth(config["username"], config["password"])
            respargs["timeout"] = snap_interval*5
            try: 
                resp = requests.get(config["url"], **respargs)
                if resp.status_code == 200:
                    try:
                        queue.append(imageio.imread(io.BytesIO(resp.content), format='jpg'))
                    except:
                        LOG.error("%s failed to write captured image!" % name)
                else:
                    LOG.error("%s failed to connect! Status Code: %d" % name,  resp.status_code)
                    time.sleep(snap_interval)
            except Exception as exc:
                LOG.error(exc)

            if len(queue) > img_store_cnt:
                queue.popleft()
             
        time.sleep(snap_interval)


class Service(object):

    cameras = None

    def __init__(self, config):
        LOG.info("Initializing service v%s", version())
        self.cameras = {}
        LOG.info("Checking camera configs")
        for name, cameracfg in config["cameras"].items():
            self.validate_camera_config(name=name, camera=cameracfg)
            self.cameras[name] = {"config": cameracfg}
        LOG.info("%d cameras: %s", len(self.cameras), ', '.join(self.cameras.keys()))
        # setup each camera with its own lock and thread
        for name, camera in self.cameras.items():
            LOG.debug("%s: %s", name, camera)
            camera["buffer"] = collections.deque()
            camera["lock"] = threading.Lock()
            camera["thread"] = threading.Thread(target=camworker, args=(name, camera["config"], camera["buffer"], camera["lock"], LOG))

    def start(self):
        LOG.info("Starting camera threads")
        # start each camera
        for name, camera in self.cameras.items():
            camera["thread"].start()

        ws = WebServer(service=self)
        ws.start()

        # test gif gen
        # ws.gif('side_door', 10, 0.25)

        while True:
            time.sleep(10)

    def validate_camera_config(self, name, camera):
        return
