#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid
import requests

class ZattooEmbed(object):

    def _get_app_token(self, page_text):
        _app_token = page_text[page_text.index('window.appToken =')+19:]
        app_token = _app_token[:_app_token.index(';<')-1]
        return app_token

    def _get_request_headers(self): 
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

    def _get_request_data(self, channel, page):
        return [
            ('uuid', str(uuid.uuid4())),
            ('session_token', self._get_app_token(page.text)),
            ('device_type', ''),
            ('partner_site', 'partner_zapi'),
            ('cid', channel),
            ('stream_type', 'hls'),
            ('https_watch_urls', 'True'),
        ]

    def sport1_m3u8(self):
        s = requests.Session()
        # fetch page data that includes the app_token
        page = s.get('http://embed-zattoo.com/dsf/?hiq=false&branded=false')
        # fetch stream url, load m3u8 data & add missing host
        res = s.post('http://embed-zattoo.com/zapi/watch', headers=self._get_request_headers(), data=self._get_request_data('dsf', page))
        return s.get(json.loads(res.content).get('stream').get('url')).text.replace('DSF-live', 'http://zh2-5-hls-live.zahs.tv/DSF-live')

    def tele5_m3u8(self):
        s = requests.Session()
        # fetch page data that includes the app_token
        page = s.get('http://embed-zattoo.com/tele-5/?hiq=false&branded=false')
        # fetch stream url, load m3u8 data & add missing host
        res = s.post('http://embed-zattoo.com/zapi/watch', headers=self._get_request_headers(), data=self._get_request_data('tele-5', page))
        return s.get(json.loads(res.content).get('stream').get('url')).text.replace('DE_tele5', 'http://zh2-5-hls-live.zahs.tv/DE_tele5')