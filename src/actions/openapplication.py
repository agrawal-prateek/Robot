import os
import sys
import re
import operator

appName = sys.argv[1]  # give string as an argument which is appname spoke by user

files = os.listdir('/usr/share/applications')
found = None
probability = dict()

for file in files:
    probability[file] = len(
        set(re.split(';|,|\*|\n| |; |, |\* |\.|\. |-|- ', file.upper())) & set(appName.upper().split()))

maxProbability = max(probability.items(), key=operator.itemgetter(1))[0]
if not probability[maxProbability] == 0:
    with open('/usr/share/applications/' + maxProbability, 'r') as desktopFile:
        app = re.search('%s(.*)%s' % ('Exec=', '\n'), desktopFile.read()).group(1)
        if app:
            found = 1
            os.system(app + ' &')
if not found:
    os.system("src/speaktext.sh 'sorry, Application could not found'")
