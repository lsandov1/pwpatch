#!/usr/bin/env python2

import os
import shutil
import subprocess

from project import Project

class Mbox:
    def __init__(self, workdir, linkname, since='last', series=None):
        self.workdir = workdir
        self.linkname = linkname
        self.since = since
        self.series = series

        self._project = Project(self.linkname)

    def _subprocess(self, args, cwd=None):
        return subprocess.Popen(args,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=cwd)

    def _mbox_dir(self):
        return os.path.join(self.workdir, self.linkname, 'mbox')

    def _project_dir(self):
        return os.path.join(self.workdir, self.linkname, 'repo')

    def _create_dir(self, d):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    def _mbox_files(self):
        mbox_dir = self._mbox_dir()
        files = [os.path.abspath(os.path.join(mbox_dir,f)) for f in os.listdir(mbox_dir)]
        return files

    def download(self, mbox_name='mbox'):
        print 'getting mboxs since: %s' % self.since

        mbox_dir = self._mbox_dir()
        self._create_dir(mbox_dir)

        mboxs = {}
        if self.since == 'last':
            (series, revision, mbox) = self._project.last_mbox
            mboxs[series] = {revision:mbox}
        else:
            # TODO: this is the most important missing
            pass

        for (series, revisions) in mboxs.iteritems():
            for (rev, mbox) in revisions.iteritems():
                mbox_filename = os.path.join(mbox_dir,
                                             'mbox-%s-%s' % (series, rev) )
                print '\tmbox %s' % mbox_filename
                with open(mbox_filename, 'w') as fd:
                    fd.write(mbox)

    def clone_repo(self, branch='test'):
        # Reuse repo if already exists
        project_dir = self._project_dir()
        if os.path.exists(os.path.join(project_dir, '.git')):
            self._subprocess(['git', 'am', '--abort'],
                             cwd=project_dir).communicate()
            self._subprocess(['git', 'clean', '-fdx'],
                             cwd=project_dir).communicate()
        else:
            self._create_dir(project_dir)
            url = self._project.url()
            self._subprocess(['git', 'clone', url, project_dir]).communicate()

        self._subprocess(['git', 'checkout', 'master'],
                         cwd=project_dir).communicate()
        self._subprocess(['git', 'pull'],
                         cwd=project_dir).communicate()
        self._subprocess(['git', 'branch', '-D', branch],
                         cwd=project_dir).communicate()
        self._subprocess(['git', 'checkout', '-b', branch],
                         cwd=project_dir).communicate()

    def patch(self):
        project_dir = self._project_dir()
        print 'patching the repo %s' % project_dir
        for mbox in self._mbox_files():
            p = self._subprocess(['git', 'am', mbox], cwd=project_dir)
            (out,err) = p.communicate()
            if p.returncode != 0:
                print '\tpatch %s failed %s: %s' % (mbox, p.returncode, out)
            else:
                print '\tpatch %s applied' % mbox

