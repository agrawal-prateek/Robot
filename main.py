#!/usr/bin/env /home/pi/env/bin/python

import re
from src.grpc.pushtotalk import main
from src.actions import send
from src.actions import shutdown
from src.actions import volume
from src.actions import display
from src.actions import sound
from src.actions import restart
from src.actions import alarm
from src.actions import call
from src.actions import search

while True:
    query = None
    try:
        query = main()
    except Exception as e:
        print(e)

    # Send Email
    if re.search('(.*)send(.*)email(.*)', query):
        send.send_email(query)

    # Send Message
    if re.search('(.*)send(.*)message(.*)', query):
        send.send_message(query)

    # Shut Down
    elif re.search('(.*)shut down(.*)', query) \
            or re.search('(.*)turn off(.*)', query):
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
        display.tell_about_image(query)

    # Show Pictures
    elif re.search('(.*)show(.*)pictures(.*)', query):
        display.show_images(query)

    # Show Calender
    elif re.search('(.*)show(.*)calender(.*)', query):
        display.show_calender(query)

    # Show videos
    elif re.search('(.*)show(.*)trailer(.*)', query) \
            or re.search('(.*)show(.*)youtube(.*)', query) \
            or re.search('(.*)show(.*)video(.*)', query) \
            or re.search('(.*)show(.*)recipe(.*)', query) \
            or re.search('(.*)play(.*)video(.*)', query) \
            or re.search('(.*)play(.*)videos(.*)', query):
        display.show_video(query)

    # Show Holiday
    elif re.search('(.*)show(.*)holiday(.*)', query) \
            or re.search('(.*)show(.*)holidays(.*)', query):
        display.show_holidays(query)

    # Timer or Named Timer
    elif re.search('(.*)start(.*)timer(.*)', query) \
            or re.search('(.*)set(.*)timer(.*)', query):
        display.start_timer(query)

    # Cancel Timer
    elif re.search('(.*)cancel(.*)timer(.*)', query) \
            or re.search('(.*)remove(.*)timer(.*)', query):
        display.cancel_timer(query)

    # Music
    elif re.search('(.*)play(.*)music(.*)', query) \
            or re.search('(.*)play(.*)song(.*)', query) \
            or re.search('(.*)start(.*)music(.*)', query) \
            or re.search('(.*)start(.*)song(.*)', query):
        sound.play(query)

    # Restart
    elif re.search('(.*)restart(.*)', query):
        restart.restart_task(query)

    # Set Alarm
    elif re.search('(.*)set(.*)alarm(.*)', query) \
            or re.search('(.*)wake(.*)me(.*)', query):
        alarm.set_alarm(query)

    # Cancel Alarm
    elif re.search('(.*)cancel(.*)alarm(.*)', query) \
            or re.search('(.*)remove(.*)alarm(.*)', query):
        alarm.cancel_alarm(query)

    # Call
    elif re.search('(.*)make(.*)call(.*)', query):
        call.make_call(query)

    # Abort Call
    elif re.search('(.*)hang(.*)up(.*)', query) \
            or re.search('(.*)abort(.*)call(.*)', query):
        call.abort_call(query)

    # Get Price
    elif re.search('(.*)tell(.*)price(.*)', query):
        search.get_price(query)
