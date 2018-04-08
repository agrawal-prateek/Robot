import os
import sys
import re
import operator
import glob

appName = sys.argv[1]  # give string as an argument which is appname spoke by user

files = glob.glob('/usr/share/applications/*.desktop')
found = None
probability = dict()

for file in files:
    with open(file, 'r') as desktopFile:
        data = re.search('%s(.*)%s' % ('Name=', '\n'), desktopFile.read()).group(1)
        probability[file] = len(
            set(re.split(';|,|\*|\n| |; |, |\* |\.|\. |-|- ', data.upper())) & set(appName.upper().split())
        )

maxProbability = max(probability.items(), key=operator.itemgetter(1))[0]
if not probability[maxProbability] == 0:
    with open(maxProbability, 'r') as desktopFile:
        app = re.search('%s(.*)%s' % ('Exec=', '\n'), desktopFile.read()).group(1)
        if app:
            found = 1
            os.system(app + ' &')
if not found:
    os.system("src/speaktext.sh 'sorry, Application could not found'")
