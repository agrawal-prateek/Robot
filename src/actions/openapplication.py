import glob
import operator
import os
import re

home_dir = os.path.expanduser('~')


def openapp(app_name):
    files = glob.glob('/usr/share/applications/*.desktop')
    found = None
    probability = dict()

    for file in files:
        with open(file, 'r') as desktopFile:
            data = re.search('%s(.*)%s' % ('Name=', '\n'), desktopFile.read()).group(1)
            probability[file] = len(
                set(re.split(';|,|\*|\n| |; |, |\* |\.|\. |-|- ', data.upper())) & set(app_name.upper().split())
            )

    max_probability = max(probability.items(), key=operator.itemgetter(1))[0]
    if not probability[max_probability] == 0:
        with open(max_probability, 'r') as desktopFile:
            app = re.search('%s(.*)%s' % ('Exec=', '\n'), desktopFile.read()).group(1)
            if app:
                found = 1
                os.system(app + ' &')
    if not found:
        os.system(home_dir + "/Robot/src/speaktext.sh 'sorry, Application could not found'")
