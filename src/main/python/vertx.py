# Copyright 2011 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" 
This module provides the entry point to the vert.x platform 
"""

import org.vertx.java.deploy.impl.VertxLocator
import org.vertx.java.core.json
import org.vertx.java.deploy.impl

from core.http import HttpServer, HttpClient
from core.net import NetServer, NetClient
from core.sock_js import SockJSServer
from core.handlers import TimerHandler, DoneHandler
from core.javautils import map_to_java, map_from_java

__author__ = "Scott Horn"
__email__ = "scott@hornmicro.com"
__credits__ = "Based entirely on work by Tim Fox http://tfox.org"

class Vertx(object):
    config = None

def create_http_server(**kwargs):
    """ Return a HttpServer """
    return HttpServer(**kwargs)

def create_http_client(**kwargs):
    """ Return a HttpClient """
    return HttpClient(**kwargs)

def create_net_server(**kwargs):
    """ Return a NetServer """
    return NetServer(**kwargs)

def create_net_client(**kwargs):
    """ Return a NetClient """
    return NetClient(**kwargs)

def create_sockjs_server(http_server):
    """ Return a SockJSServer """
    return SockJSServer(http_server)

def get_logger():
    """ Get the logger for the verticle"""
    return org.vertx.java.deploy.impl.VertxLocator.container.getLogger()

def deploy_verticle(main, config=None, instances=1, handler=None):
    """Deploy a verticle. The actual deploy happens asynchronously

    Keyword arguments:
    main -- the main of the verticle to deploy
    config -- dict configuration for the verticle
    instances -- number of instances to deploy
    handler -- will be executed when deploy has completed

    returns Unique id of deployment
    """
    if config != None:
        config = org.vertx.java.core.json.JsonObject(map_to_java(config))
  
    return org.vertx.java.deploy.impl.VertxLocator.container.deployVerticle(main, config, instances, DoneHandler(handler))

def deploy_worker_verticle(main, config=None, instances=1, handler=None):
    """Deploy a workerverticle. The actual deploy happens asynchronously

    Keyword arguments:
    main -- the main of the verticle to deploy
    config -- dict configuration for the verticle
    instances -- the number of instances to deploy
    handler -- handler will be executed when deploy has completed
    """
    if config != None:
        config = org.vertx.java.core.json.JsonObject(map_to_java(config))
    return org.vertx.java.deploy.impl.VertxLocator.container.deployWorkerVerticle(main, config, instances, DoneHandler(handler))

def undeploy_verticle(id):
    """Undeploy a verticle

    Keyword arguments:
    id -- the unique id of the deployment
    """
    org.vertx.java.deploy.impl.VertxLocator.container.undeployVerticle(id)

def config():
    """Get config for the verticle

    returns dict config for the verticle
    """
    if Vertx.config is None:
        Vertx.config = map_from_java(org.vertx.java.deploy.impl.VertxLocator.container.getConfig().toMap())
    return Vertx.config

def java_vertx():
    return org.vertx.java.deploy.impl.VertxLocator.vertx

def set_timer(delay, handler):
    """Sets a one-shot timer that will fire after a certain delay.
    This method will accept either a Proc or a block.

    Keyword arguments:
    delay -- the delay, in milliseconds
    handler -- a block representing the code that will be run after the delay the unique id of the timer
    """
    java_vertx().setTimer(delay, TimerHandler(handler))

def set_periodic(delay, handler):
    """Sets a periodic timer.

    Keyword arguments:
    delay -- the period of the timer, in milliseconds
    handler -- a block representing the code that will be when the timer fires the unique id of the timer
    """
    java_vertx().setPeriodic(delay, TimerHandler(handler))


def cancel_timer(id):
    """Cancels a timer.

    Keyword arguments:
    id -- the id of the timer, as returned from set_timer or set_periodic

    returns true if the timer was cancelled, false if it wasn't found.
    """
    java_vertx().cancelTimer(id)


def run_on_loop(handler):
    """Put the handler on the event queue for this loop so it will be run asynchronously
    ASAP after this event has been processed

    Keyword arguments:
    handler -- a block representing the code that will be run ASAP
    """
    java_vertx().runOnLoop(DoneHandler(handler))
