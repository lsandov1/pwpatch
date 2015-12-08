#!/usr/bin/env python2
#
# patchwork - Simple REST Client for patchwork [1]
#
# [1] http://patchwork-freedesktop.readthedocs.org/en/latest/index.html
#

import requests

class patchwork:
    root='http://patchwork.freedesktop.org/'
    api='api/1.0/'

    @classmethod
    def url(cls, url=''):
        return cls.root + cls.api + url

    @classmethod
    def series(cls, series_id=None, revisions=False, version=None):
        url=''
        if series_id:
            url = "%s/" % series_id
            if revisions:
                url += "revisions/"
                if version:
                    url += "%s/" % version
        return 'series/' + url

    @classmethod
    def _request(cls, verb, url, raw=False):
        v = verb.lower()
        if v == 'get':
            method = requests.get
        elif ml == 'post':
            method = requests.post
        abs_url = cls.url(url)
        r = method(abs_url)
        data = None
        try:
            r.raise_for_status()
            data = r.text if raw else r.json()
        except requests.exceptions.HTTPError:
            print('Request fail (%s) for %s' % (r.status_code, abs_url))
        return data

class get(patchwork):
    @classmethod
    def projects(cls, linkname=None,project_id=None, events=False, series=False):
        url = ''
        if linkname:
            url = "%s/" % linkname
        elif project_id:
            url = "%s/" % project_id
        if url:
            if events:
                url += "events/"
            elif series:
                url += "series/"
        return cls._request('get', 'projects/' + url)

    @classmethod
    def series(cls, series_id=None, revisions=False, version=None, mbox=False):
        raw = False
        url = patchwork.series(series_id, revisions, version)
        if version and mbox:
            raw = True
            url += 'mbox/'
        return cls._request('get', url, raw=raw)

class post(patchwork):
    @classmethod
    def series(cls, series_id, version):
        return cls._request('post',
                            patchwork.series(series_id=series_id,
                                             version=version,
                                             revisions=True) + 'test-results/')
