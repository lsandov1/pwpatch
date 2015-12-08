#!/usr/bin/env python2
#
# Tiny Patchwork wrapper for a project
#

import patchwork as pw

class Project:
    """(Tiny) Wrapper for a project's series"""

    def __init__(self, linkname):
        self.linkname = linkname
        self._project = pw.get.projects(self.linkname)

    @property
    def series(self):
        if not hasattr(self, '_series'):
            json = pw.get.projects(linkname=self.linkname, series=True)
            self._series = json['results']
        return self._series

    @property
    def last_mbox(self):
        return self.n_mbox(0)

    def n_mbox(self, n):
        series_id = self.series[n]['id']
        revision = self.series[n]['version']
        mbox = pw.get.series(series_id=series_id,
                             version=revision,
                             revisions=True, mbox=True)
        return (series_id, revision, mbox)

    def url(self):
        return self._project['scm_url']
