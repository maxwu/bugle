# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'maxwu'

import json
import tempfile
from git.cmd import Git

def get_all_remote_branch(url):
    tmp = tempfile.mkdtemp(prefix="repo_br")
    git = Git(tmp)
    git.clone(url, tmp)
    return [b.strip()[len('origin/'):] for b in git.branch('--remote').splitlines() if not 'HEAD' in b]

def beauty_dump(obj):
    return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))

if __name__ == '__main__':
    print beauty_dump(get_all_remote_branch('https://github.com/maxwu/robotframework-suites'))