#!/usr/bin/env /home/pi/env/bin/python

import re
from src.grpc.pushtotalk import main
from src.actions import email
from src.actions import shutdown
from src.actions import volume
from src.actions import display

while True:
    query = None
    try:
        query = main()
    except Exception as e:
        print(e)

    # Send Email
    if re.search('(.*)send(.*)email(.*)', query):
        email.sendmailui()

    # Shut Down
    elif re.search('(.*)shut down(.*)', query):
        shutdown.shutdown()

    # Decrease Volume
    elif re.search('(.*)turn(.*)down(.*)volume(.*)', query) \
            or re.search('(.*)decrease(.*)volume(.*)', query) \
            or re.search('(.*)slow(.*)volume(.*)', query):
        volume.decrease()

    # Increase Volume
    elif re.search('(.*)turn(.*)up(.*)volume(.*)', query) \
            or re.search('(.*)increase(.*)volume(.*)', query) \
            or re.search('(.*)high(.*)volume(.*)', query) \
            or re.search('(.*)speak(.*)loud(.*)', query):
        volume.increase()

    # Tell me about This image
    elif re.search('(.*)tell(.*)this(.*)image(.*)', query) \
            or re.search('(.*)know(.*)this(.*)image(.*)', query) \
            or re.search('(.*)tell(.*)this(.*)picture(.*)', query) \
            or re.search('(.*)know(.*)this(.*)image(.*)', query):
        display.tell_about_image()

    # Show Pictures
    elif re.search('(.*)show(.*)pictures(.*)', query):
        display.show_images(query)

    # Show Calender
    elif re.search('(.*)show(.*)calender(.*)', query):
        display.show_calender()

    # Show videos
    elif re.search('(.*)show(.*)trailer(.*)', query) \
            or re.search('(.*)show(.*)youtube(.*)', query) \
            or re.search('(.*)show(.*)video(.*)', query) \
            or re.search('(.*)show(.*)recipe(.*)', query):
        display.show_video(query)
