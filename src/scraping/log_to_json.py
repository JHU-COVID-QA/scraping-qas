# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import sys
import json

def main():
    text = ""
    with open(sys.argv[1]) as fp:
        text = fp.read()

    contents = {}
    contents['text'] = text
    with open('tmp.json', 'w+') as fp:
        json.dump(contents, fp)

if __name__ == '__main__':
    main()
