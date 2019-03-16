#! /usr/bin/python3
#
#    Copyright (C) 2015 VMware, Inc. All rights reserved.
#    publishtool for working with photonpublish
#
#    Author(s): Priyesh Padmavilasom
#

import sys
import getopt

from photonpublish import photonPublish
from publishconst import publishConst

const = publishConst()

class publishTool:
    def __init__(self, context):
        self._context = context
        self._publish = photonPublish(context)

    #check local files against remote repo
    def check(self):
        result = self._publish.check(self._context['srcroot'])
        print('Updates: %d'   % len(result[const.updates]))
        print('New: %d'       % len(result[const.new]))
        print('Verified: %d'  % len(result[const.verified]))
        print('Obsoletes: %d' % len(result[const.obsoletes]))
        print('New files are : %s' %(result[const.new]))
        return result

    def hasPendingSync(self, advice):
        return advice[const.updates] or advice[const.new]

    #apply advices to sync remote.
    #note: discarding/removing is stll getting resolved pending bintray api
    def push(self):
        advice = self.check()
        if not self._context['silent']:
            if not self.hasPendingSync(advice):
                print('No changes to push.')
                return
            choice = input('Continue? y/N:')
            if choice != 'y':
                print('Aborted on user command')
                return
        print('push local changes to remote...')
        self._publish.syncRemote(self._context['srcroot'], advice)


    def printsha1(self, files, label):
        print('sha1sum of %s >>>' % label)
        for f in files:
            print('%s - %s' % (f['name'], f['sha1']))

    def makesha1(self):
        advice = self.check()
        verified = len(advice[const.verified])
        if verified <= 0:
            print('no files verified. nothing to do.')
            return
        self.printsha1(advice[const.verified], const.verified)

    def writesha1(self):
        if 'sha1file' not in self._context.keys():
            raise Exception('writesha1 requires a file to write to. specify in --sha1file')

        advice = self.check()
        verified = advice[const.verified]
        verifiedLen = len(advice[const.verified])
        if verifiedLen <= 0:
            print('no files verified. nothing to do.')
            return

        with open(self._context['sha1file'], 'w') as sha1file:
            for f in verified:
                if f['name'] == const.sha1allfilename:
                    continue
                sha1file.write('%s - %s\n' % (f['name'], f['sha1']))

    def publish(self):
        pending = self._publish.getUnpublished()
        pendingCount = len(pending)
        if not self._context['silent']:
            if pendingCount == 0:
                print('No pending changes to publish.')
                return
            print('Found %d pending files to publish' % pendingCount)
            choice = input('Continue? y/N:')
            if choice != 'y':
                print('Aborted on user command')
                return
            print(self._publish.publish())

def showUsage():
    print('Usage:')
    print('check status: publishTool.py \
--config <config file> --srcroot <source root folder> \
--action check')
    print('push files: publishTool.py \
--config <config file> --srcroot <source root folder> \
--action push')
    print('publish pushed files: publishTool.py \
--config <config file> folder> --action publish')
    print('make sha1 file: publishTool.py \
--config <config file> folder> --srcroot <source root folder> \
--action makesha1')
    print('write sha1 file: publishTool.py \
--config <config file> folder> --srcroot <source root folder> \
--sha1file <sha1 file path> --action writesha1')

#
def main(argv):
    try:
        context = {'silent':False}
        opts, args = getopt.getopt(
            sys.argv[1:],
            '',
            ['config=',
             'srcroot=',
             'action=',
             'sha1file=',
             'silent=',
             'help'])
        for opt, arg in opts:
            if opt == '--config':
                context['config'] = arg
            elif opt == '--srcroot':
                context['srcroot'] = arg
            elif opt == '--action':
                context['action'] = arg
            elif opt == '--silent':
                context['silent'] = arg
            elif opt == '--sha1file':
                context['sha1file'] = arg
            elif opt == '--help':
                showUsage()
                return
    except Exception as e:
        showUsage()
        sys.exit(1)

    try:
        tool = publishTool(context)
        if context['action'] == 'push':
            tool.push()
        elif context['action'] == 'check':
            tool.check()
        elif context['action'] == 'makesha1':
            tool.makesha1()
        elif context['action'] == 'writesha1':
            tool.writesha1()
        elif context['action'] == 'publish':
            tool.publish()
    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
