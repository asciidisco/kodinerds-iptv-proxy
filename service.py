#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module: service
# Created on: 26.01.2017

import threading
import SocketServer
import socket
from xbmc import Monitor
from resources.lib.IPProxyHttpRequestHandler import IPProxyHttpRequestHandler

# port for the internal IPTV HTTP proxy service
PORT = 12345

# server defaults
SocketServer.TCPServer.allow_reuse_address = True

# configure the IPTV Data Server
iptv_server = SocketServer.TCPServer(('127.0.0.1', PORT), IPProxyHttpRequestHandler)
iptv_server.server_activate()
iptv_server.timeout = 1

if __name__ == '__main__':
    monitor = Monitor()

    # start thread for IPTV HTTP service
    nd_thread = threading.Thread(target=iptv_server.serve_forever)
    nd_thread.daemon = True
    nd_thread.start()

    # kill the service if kodi monitor tells us to
    while not monitor.abortRequested():
        if monitor.waitForAbort(5):
            iptv_server.shutdown()
            break

    # IPTV service shutdown sequence
    iptv_server.server_close()
    iptv_server.socket.close()
    iptv_server.shutdown()
