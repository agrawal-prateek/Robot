#!/usr/bin/env /home/pi/env/bin/python

import re

from src.actions import alarm
from src.actions import call
from src.actions import display
from src.actions import restart
from src.actions import send
from src.actions import shutdown
from src.actions import sound
from src.actions import volume
from src.grpc.pushtotalk import main

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
    # elif re.search('(.*)turn(.*)up(.*)volume(.*)', query) \
    #         or re.search('(.*)increase(.*)volume(.*)', query) \
    #         or re.search('(.*)high(.*)volume(.*)', query) \
    #         or re.search('(.*)speak(.*)loud(.*)', query):
    #     volume.increase()

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
        pass

    # Throw/Roll a dice
    elif re.search('(.*)roll(.*)dice(.*)', query) \
            or re.search('(.*)throw(.*)dice(.*)', query):
        pass

    # Flip a coin
    elif re.search('(.*)flip(.*)coin(.*)', query) \
            or re.search('(.*)throw(.*)coin(.*)', query):
        pass

    # Random No.
    elif re.search('(.*)pick(.*)between(.*)', query) \
            or re.search('(.*)random(.*)between(.*)', query):
        pass

    # Definition of a word
    elif re.search('(.*)what(.*)mean(.*)', query) \
            or re.search('(.*)how(.*)define(.*)', query):
        pass

    # Spell a word
    elif re.search('(.*)how(.*)spell(.*)', query):
        pass

    # Sports
    elif re.search('for sports', query):
        pass

    # Send to tablet
    elif re.search('(.*)send(.*)my(.*)tablet(.*)', query) \
            or re.search('(.*)show(.*)my(.*)tablet(.*)', query) \
            or re.search('(.*)show(.*)my(.*)tab(.*)', query):
        pass

    # Show current screen to other`s tablet
    elif re.search('(.*)show(.*)on(.*)tablet(.*)', query) \
            or re.search('(.*)show(.*)on(.*)tab(.*)', query):
        pass

    # Lights ON/OFF
    elif re.search('(.*)(turn|switch)(.*)(on|off)(.*)', query):
        pass

    # To Dim Lights/fan
    elif re.search('(.*)dim(.*)', query):
        pass

    # Temperature
    elif re.search('(.*)set(.*)temperature(.*)', query) \
            or re.search('(.*)raise(.*)temperature(.*)', query):
        pass

    # Door Lock
    elif re.search('(.*)lock(.*)door(.*)', query) \
            or re.search('(.*)lock(.*)gate(.*)', query):
        pass

    # Discover/Find Devices
    elif re.search('(.*)discover(.*)device(.*)', query) \
            or re.search('(.*)find(.*)my(.*)device(.*)', query) \
            or re.search('(.*)where(.*)device(.*)', query):
        pass

    # Bluetooth
    elif re.search('(.*)connect(.*)to(.*)', query) \
            or re.search('(.*)bluetooth(.*)', query):
        pass

    # Switch Account
    elif re.search('(.*)switch(.*)account(.*)', query):
        pass

    # Get Profile
    elif re.search('(.*)whose(.*)profile(.*)', query) \
            or re.search('(.*)who(.*)is(.*)this(.*)', query):
        pass

    # GOOD Morning
    elif re.search('(.*)good(.*)morning(.*)', query):
        pass

    # Tell a joke
    elif re.search('(.*)tell(.*)joke(.*)', query):
        pass
