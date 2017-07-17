#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
from urlparse import urlparse, parse_qs
from .ZattooEmbed import ZattooEmbed

class IPProxyHttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        m3u8 = None
        url = urlparse(self.path)
        params = parse_qs(url.query)
        channel = params.get('channel', [None])[0]

        # not method given
        if channel == None:
            self.send_error(500, 'No channel declared')
            return

        if channel == 'tele5':
            zattoo_tele5 = ZattooEmbed()
            m3u8 = zattoo_tele5.tele5_m3u8()

        if channel == 'sport1':
            zattoo_sport1 = ZattooEmbed()
            m3u8 = zattoo_sport1.sport1_m3u8()

        if m3u8 is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(m3u8)
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Not found')        

    def log_message(self, format, *args):
        return
