"""
    Copyright (c) 2016, 2017 - o2r project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""


from extract import metaextract
from broker import metabroker
from harvest import metaharvest
from validate import metavalidate

import argparse
import datetime
import os
import sys


def status_note(msg, **kwargs):
    verbose = kwargs.get('debug', None)
    if verbose is None:
        print(''.join(('[o2rmeta] ', str(msg))))
    else:
        if verbose:
            print(''.join(('[o2rmeta][debug] ', str(msg))))
        else:
            pass

# Main
if __name__ == "__main__":
    if sys.version_info[0] < 3 and sys.version_info[1] < 4:
        status_note('requires python 3.4+')
        sys.exit(0)
    else:
        # arg parse setup:
        parser = argparse.ArgumentParser(description='description')
        parser.add_argument('-debug', help='debug mode', action='store_true', default=False, required=False)
        subparsers = parser.add_subparsers(title='extractor', dest='tool')
        # - - - - - - - - - - - - - - - - - -
        extractor = subparsers.add_parser("extract")
        extractor.add_argument("-i", "--inputdir", type=str, required=True)
        group = extractor.add_mutually_exclusive_group(required=True)
        group.add_argument('-o', '--outputdir', type=str, help='output directory for extraction docs')
        group.add_argument('-s', '--outputtostdout', help='output the result of the extraction to stdout',
                           action='store_true', default=False)
        extractor.add_argument('-e', '--ercid', type=str, help='erc identifier', required=False)
        extractor.add_argument('-b', '--basedir', type=str, help='base directory for relative paths', required=False)
        extractor.add_argument('-xml', '--modexml', help='output xml', action='store_true', default=False, required=False)
        extractor.add_argument('-xo', '--stayoffline', help='skip all http requests', action='store_true', default=False,
                            required=False)
        extractor.add_argument('-m', '--metafiles', help='output all metafiles', action='store_true', default=False,
                            required=False)
        # - - - - - - - - - - - - - - - - - -
        # the broker has two modes:
        # 1.) mapping mode creates fitting metadata for a given map
        # 2.) checking mode returns missing metadata information for a target service
        broker = subparsers.add_parser("broker")
        maingroup = broker.add_mutually_exclusive_group(required=True)
        maingroup.add_argument("-c", "--check", type=str, required=False)
        maingroup.add_argument("-m", "--map", type=str, required=False)
        broker.add_argument("-i", "--inputfile", type=str, required=True)
        group = broker.add_mutually_exclusive_group(required=True)
        group.add_argument('-o', '--outputdir', type=str, help='output directory for brokering docs')
        group.add_argument('-s', '--outputtostdout', help='output the result of the brokering to stdout',
                           action='store_true', default=False)
        # - - - - - - - - - - - - - - - - - -
        harvester = subparsers.add_parser("harvest")
        harvester.add_argument('-e', '--element', type=str,  help='element type, e.g. doi or creator',required=True)
        harvester.add_argument('-q', '--query', type=str,  help='query string', required=True)
        # - - - - - - - - - - - - - - - - - -
        validator = subparsers.add_parser("validate")
        validator.add_argument("-s", "--schema", type=str, required=True)
        validator.add_argument("-c", "--candidate", type=str, required=True)
        # - - - - - - - - - - - - - - - - - -
        args = parser.parse_args()
        argsd = vars(args)
        status_note(''.join(('received arguments: ', str(argsd))), debug=argsd['debug'])
        try:
            if argsd['tool'] == "extract":
                status_note('launching extractor')
                metaextract.start(i=argsd['inputdir'], o=argsd['outputdir'], s=argsd['outputtostdout'], xo=argsd['stayoffline'], e=argsd['ercid'], b=argsd['basedir'], m=argsd['metafiles'], xml=argsd['modexml'])
            elif argsd['tool'] == "broker":
                status_note('launching broker')
                metabroker.start(c=argsd['check'], m=argsd['map'], i=argsd['inputfile'], o=argsd['outputdir'], s=argsd['outputtostdout'])
            elif argsd['tool'] == "validate":
                status_note('launching validator')
                metavalidate.start(s=argsd['schema'], c=argsd['candidate'])
            elif argsd['tool'] == "harvest":
                status_note('launching harvester')
                metaharvest.start(e=argsd['element'], q=argsd['query'])
            else:
                pass
        except:
            raise
