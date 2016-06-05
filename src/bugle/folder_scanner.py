# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'maxwu'

import sys
import os
from robot.parsing.model import (
    TestData,
    TestCaseFile,
    ResourceFile,
    DataError
)
from bugle.utils import *


class FolderScanner(object):
    def __init__(self, absfolder):
        self.absfolder = absfolder
        self.files = {}
        self.counts = {}
        pass

    def check_extension(self, f):
        ext = os.path.splitext(f.lower())[-1][1:]
        return ext in ['html', 'htm', 'xhtml', 'tsv' , 'rst', 'rest', 'txt', 'robot']

    def scan(self):
        print "scan folder: %s" % (self.absfolder)
        # each file has (path=str, name=str, cases=[], kws=[])
        self.files = {}
        for root, subfolders, files in os.walk(self.absfolder):
            for f in sorted(files):
                if self.check_extension(f):
                    fullpath = os.path.join(root, f)
                    print "file: %s" %fullpath
                    relpath = fullpath[len(root):]
                    #self.scan_suite(fullpath) or self.scan_res(fullpath)

                    res = self.scan_suite(fullpath)
                    if res:
                        self.files[fullpath] = dict(name=res['name'], cases=res['cases'], kws=res['kws'])
                        continue
                    res = self.scan_res(fullpath)
                    if res:
                        self.files[fullpath] = dict(name=res['name'], cases=[], kws=res['kws'])
        self.count()
        return self.files

    def scan_suite(self, file):
        #return None if file is not a test suite file.
        try:
            st = TestCaseFile(source=file)
            st.populate()
            cases = []
            kws = []
            ftags = []
            for kw in st.keywords:
                print "-- keyword: %s" % (kw.name)
                kws.append(kw.name.strip())
            for cs in st.testcase_table.tests:
                print "-- test case: %s" % (cs.name)
                cases.append(cs.name.strip())
            if st.setting_table.force_tags:
                ftags = st.setting_table.force_tags.value
                print "## force tags: %s" % ftags
            return dict(name=st.name, cases=cases, kws=kws, ftags=ftags)
        except Exception as e:
            print "not a suite: %s, %s" % (file, e)
            return None

    def scan_res(self, file):
        # return None if file is not a test suite file.
        try:
            rs = ResourceFile(source=file)
            rs.populate()
            kws = []
            for kw in rs.keywords:
                print "-- keywords: %s" % (kw.name)
                kws.append(kw.name)
            return dict(name=rs.name, kws=kws)
        except Exception as e:
            print "not a resource: %s, %s" % (file, e)
            return None

    def count(self):
        self.counts = {'cases': 0, 'kws': 0}
        self.counts['cases'] = sum([len(v['cases']) for k,v in self.files.items()])
        self.counts['kws'] = sum([len(v['kws']) for k,v in self.files.items()])
        return self.counts

if __name__ == '__main__':
    rfolder = FolderScanner(sys.argv[1])
    # pprint.pprint(rfolder.scan())
    # rfolder.count()
    # print "%s cases number %d" %(rfolder.absfolder, rfolder.counts['cases'])
    # print "%s keywords number %d" % (rfolder.absfolder, rfolder.counts['kws'])
    rfolder.scan()
    print json.dumps(rfolder.count(), sort_keys=True, indent=2, separators=(',', ': '))
    print json.dumps(rfolder.files, sort_keys=True,indent=2, separators=(',', ': '))

    pass