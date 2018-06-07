#!/usr/bin/env /home/pi/env/bin/python

from src.grpc.pushtotalk import main
while True:
    try:
        main()
    except Exception as e:
        print(e)
