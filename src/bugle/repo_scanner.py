# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'maxwu'

import tempfile
import shutil
from git.cmd import Git
from git.repo.base import Repo
from jinja2 import Template, Environment, PackageLoader
from folder_scanner import *
from bugle.utils import *


class CaseRepo(object):
    def __init__(self, root=None, folders=None, name=None, url=None, ):
        self.DEFAULT_BRANCH = 'master'

        if root is None:
            self.root = tempfile.mkdtemp(prefix="bugle_"+name+"_")
            self.is_root_tmp = True
        else:
            self.root = root
            self.is_root_tmp = False

        if name is None:
            self.name = os.path.basename(root)
        else:
            self.name = name

        self.url = url
        # Make sure folder is a git repo
        if self.is_root_tmp and self.url is None:
            raise Exception("New folder with no repo URL")
        self.git = Git(self.root)
        self.git_clone()

        self.repo = Repo(self.root)

        if folders is None:
            self.folders = ['.']
        else:
            self.folders =  folders

        self.files = {}
        self.branches = {}
        self.total_count = {}
        self.branch_count = {}
        print "creating repo %s under %s, folders %s" %(name, self.root, self.folders)

    @proxy_decorate
    def git_clone(self):
        cmd = " ".join((self.url, self.root))
        print "git clone %s" %cmd
        print self.git.clone(self.url, self.root)

    def clean_up(self, forced=False):
        if self.is_root_tmp or forced:
            shutil.rmtree(self.root, True)

    def get_all_remote_branch(self):
        rlist = []
        for b in self.git.branch('--remote').splitlines():
            b = b.strip()[len('origin/'):]
            #FIXME: add ignore branch key words.
            if 'HEAD' in b or '/' in b or 'PVT' in b:
                print "ignore branch %s" %b
                continue
            rlist.append(b)
        print "all remote branches: %s" %beauty_dump(rlist)
        return rlist

    @property
    def branches_names(self):
        return self.branches.keys()

    @proxy_decorate
    def scan_branch(self, branch=None, folders=None):
        """
        Scan specific branch and return the flie list which has case/kw included.
        :param branch: branch name, default to master
        :return: file list, each file is a dict of cases and kws.
            The list item is defined as below:
            files[fullpath] = dict(name=res['name'], cases=res['cases'], kws=res['kws'])
        """
        if branch is None:
            branch = self.DEFAULT_BRANCH
        # checkout to target branch
        print self.git.checkout(branch)
        print self.git.pull()
        print self.repo.active_branch
        files = {}
        # scan folder list
        if folders is None:
            folders = self.folders
        for folder in sorted(folders):
            print "scan folder %s for repo %s branch %s" %(folder, self.name, branch)
            if folder == '.':
                fs = FolderScanner(self.root)
            else:
                fs = FolderScanner(os.path.join(self.root, folder))
            files.update(fs.scan())
            #print beauty_dump(fs.count())
        self.branch_count[branch] = self.count(files)
        print "branch %s, count=%s" %(branch, beauty_dump(self.branch_count[branch]))
        return dict(branch=branch, files=files)

    def scan_branches(self, branches=None):
        """
        The main entry to search branches with interested folders.
        :param branches: The dict param { 'branch name in str': [folder list] }
        :return: final files merged up.
        """
        if branches is None:
            branches = {}
            for br in self.get_all_remote_branch():
                print "automatically add branch %s" %br
                branches[br] = None
        self.branches = branches
        self.files = {}
        bs_list = []
        for br, folders in branches.items():
            self.branches_names.append(br)
            bs = self.scan_branch(br, folders=folders)
            bs_list.append(bs)
        self.files = self.merge_up(bs_list)

        # Process total count and figure out unique data for branches
        self.total_count = self.count()
        self.total_count['unique'] = {}
        for b in self.branches_names:
            self.total_count['unique'][b] = {'cases': 0, 'kws': 0}

        for k, v in self.files.items():
            for c in v['cases']:
                if len(c['branches']) == 1:
                    self.total_count['unique'][c['branches'][0]]['cases'] += 1
            for k in v['kws']:
                if len(k['branches']) == 1:
                    self.total_count['unique'][k['branches'][0]]['kws'] += 1

        return self.files

    def merge_up(self, bs_list):
        """
        Merge up branch scan results per Case and Keyword Name.
        :param bs_list: branch scan result list
        :return: a new list.
        """
        if bs_list is None:
            return None
        files = {}
        for bs in bs_list:
            print "merging up branch %s with %d files" %(bs['branch'], len(bs['files']))
            #print beauty_dump(bs)
            for k, v in bs['files'].items():
                if k in files:
                    # merge file
                    files[k] = self._merge_file(files[k], bs['files'][k], bs['branch'])
                    pass
                else:
                    # new add
                    files[k] = dict(name=v['name'], branches=[bs['branch']])
                    cases = []
                    for tc in v['cases']:
                        cases.append(dict(case=tc, branches=[bs['branch']]))
                    kws = []
                    for kw in v['kws']:
                        kws.append(dict(kw=kw, branches=[bs['branch']]))
                    files[k]['cases'] = cases
                    files[k]['kws'] = kws
                    # form now on, each case has a list to record branches it shows up
                    files[k]['branches'] = [bs['branch']]
                    # from now on, files[k] added a list with key 'branch' to record
                    # how many branches it exist in.
            #print "Taken branch %s,\n%s" %(bs['branch'], beauty_dump(files))
        return files

    @staticmethod
    def _merge_file(orig, new, branch):
        assert branch is not None
        assert orig is not None
        assert new is not None
        # Add file branch info.
        if branch not in orig['branches']:
            orig['branches'].append(branch)

        for tc2 in new['cases']:
            merged = False
            for tc1 in orig['cases']:
                if tc1['case'] == tc2 and branch not in tc1['branches']:
                    tc1['branches'].append(branch)
                    merged = True
                    break
            if not merged:
                orig['cases'].append(dict(case=tc2, branches=[branch] ))
        # TODO: common method shall be added.
        for kw2 in new['kws']:
            merged = False
            for kw1 in orig['kws']:
                if kw1['kw'] == kw2 and branch not in kw1['branches']:
                    kw1['branches'].append(branch)
                    merged = True
                    break
            if not merged:
                orig['kws'].append(dict(kw=kw2, branches=[branch]))
        return orig

    def count(self, files=None):
        if files is None:
            files = self.files
        counts = {'cases': 0, 'kws': 0}
        counts['cases'] = sum([len(v['cases']) for k, v in files.items()])
        counts['kws'] = sum([len(v['kws']) for k, v in files.items()])
        return counts

    def dump_html(self, temp='files_table.html', output=None):
        if output is None:
            output = './' + self.name + '_case_report.html'
        env = Environment(loader=PackageLoader('bugle.bugle_site', 'templates'))
        print "loading template: %s" %temp
        template = env.get_template(temp)

        print "rendering to: %s" %output
        with open(output, 'wt') as f:
            f.write(template.render(cr=self))
        print "report generated at %s" %output


if __name__ == '__main__':
    pass