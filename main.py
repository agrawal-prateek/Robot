#!/usr/bin/env python

import os
import re
from multiprocessing import Process

from src.actions import openapplication, email

query = 'can you please send the email'
# query = 'open firefox'
if re.search('open(.*)', query):
    Process(target=openapplication.openapp, args=(re.search('open(.*)', query).group(1),)).start()
elif re.search('(.*)send(.*)email(.*)', query):
    Process(target=email.sendmailui).start()
else:
    os.system("src/speaktext.sh 'sorry, We can not proceed your request! Please try again with different keyword'")
print(1)
