#!/usr/bin/env python

import os
import re
import sys

from src.actions import openapplication, email

query = 'can you please send the email'
if re.search('open(.*)', query):
    openapplication.openapp(re.search('open(.*)', query).group(1))
elif re.search('(.*)send(.*)email(.*)', query):
    email.sendmailui()
else:
    os.system("src/speaktext.sh 'sorry, We can not proceed your request! Please try again with different keyword'")
