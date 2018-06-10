from tkinter import *
from time import sleep
from os import system
from src.actions import nlp


def tell_about_image():
    import io

    import google.cloud.vision
    import os

    try:
        os.remove('/home/pi/data/images/temp.jpg')
    except Exception as e:
        print(e)

    if not os.path.exists('/home/pi/data'):
        os.mkdir('/home/pi/data')
        os.mkdir('/home/pi/data/images')
    elif not os.path.exists('/home/pi/data/images'):
        os.mkdir('/home/pi/data/images')

    os.system('raspistill -o /home/pi/data/images/temp.jpg')
    image_file_name = '/home/pi/data/images/temp.jpg'

    vision_client = google.cloud.vision.ImageAnnotatorClient()
    with io.open(image_file_name, 'rb') as image_file:
        content = image_file.read()

    image = google.cloud.vision.types.Image(content=content)

    labels = vision_client.label_detection(image=image)
    webs = vision_client.web_detection(image=image)
    # texts = vision_client.text_detection(image=image)
    # faces = vision_client.face_detection(image=image)
    # lands = vision_client.landmark_detection(image=image)
    # logos = vision_client.logo_detection(image=image)

    output_text = ''
    if labels:
        output_text += labels.label_annotations[0].description
    if webs:
        output_text += ' ' + webs.web_detection.web_entities[0].description
        output_text += ' ' + webs.web_detection.best_guess_labels[0].label

    if output_text:
        os.system("/home/pi/Robot/src/speaktext.sh '" + output_text + "'")
    else:
        os.system(
            "/home/pi/Robot/src/speaktext.sh "
            "'Sorry, we could not analyse this image."
            " Please try with different position and angles."
            " Or you could try with more lightning. Thank you'"
        )


def show_images(query):
    pass


def show_calender(query):
    pass


def show_video(query):
    from apiclient.discovery import build
    from apiclient.errors import HttpError
    import cv2
    import pytube

    DEVELOPER_KEY = "AIzaSyAIUKy0S4IavWzn0OLjr6LciDHJzNzWlRw"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=1
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                           search_result["id"]["videoId"]))

        # print ("Videos:\n", "\n".join(videos), "\n")
        # print(videos[0])
        print("Playing... ", "https://www.youtube.com/watch?v=",
              list(videos[0].split())[-1][1:len(list(videos[0].split())[-1]) - 1], sep='')
        link = "https://youtu.be/qLMpH6tpvBY"
        yt = pytube.YouTube(link)
        stream = yt.streams.first()
        stream.download(tmpdir='/home/pi/Robot/src/temp/video.mp4')
        cap = cv2.VideoCapture('video.mp4')
        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error opening video stream or file")

        # Read until video is completed
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:

                # Display the resulting frame
                cv2.imshow('Frame', frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()
    except HttpError as e:
        print("error")
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


def start_timer(query):
    class Timer:
        def __init__(self, hour, minute, sec):
            self.root = Tk()
            self.hour = hour
            self.minute = minute
            self.sec = sec
            self.main_hour = hour
            self.main_minute = minute
            self.main_sec = sec
            self.root.attributes('-fullscreen', True)
            self.root.bind('<Escape>', exit)
            self.frame = Frame(self.root)
            self.time = Label(
                self.frame,
                text=str(self.hour) + ' : ' + str(self.minute) + ' : ' + str(self.sec),
                font=('Helvetica', 88)
            )
            self.frame.pack(expand=True)
            self.time.pack()
            self.start_timer()

        def update_time(self):
            self.sec -= 1
            if self.sec < 0:
                self.sec = 59
                self.minute -= 1
            if self.minute < 0:
                self.hour -= 1
                self.minute = 59
            self.time['text'] = str(self.hour) + ' : ' + str(self.minute) + ' : ' + str(self.sec)
            self.time.update()

        def alarm(self):
            text = "/home/pi/Robot/src/speaktext.sh '"
            if self.main_hour != 0:
                text += str(self.main_hour) + " hour "
            if self.main_minute != 0:
                text += str(self.main_minute) + " minute "
            if self.main_sec != 0:
                text += str(self.main_sec) + " second "
            text += "has been finished!'"
            system(text)

        def run_timer(self):
            while True:
                self.update_time()
                if self.hour == 0 and self.minute == 0 and self.sec == 0:
                    self.alarm()
                    self.root.destroy()
                sleep(0.99)

        def start_timer(self):
            self.root.after(1000, self.run_timer)
            self.root.mainloop()

    h = 0
    m = 0
    s = 0
    h_m_s = []
    data = nlp.get_parts_of_speech(query)
    for part in data:
        if part['parts_of_speech'] == 'NUM':
            h_m_s.append(part['token'])
        elif part['parts_of_speech'] == 'NOUN':
            if part['token'] == 'seconds' or \
                    part['token'] == 'second' or \
                    part['token'] == 'hour' or \
                    part['token'] == 'hours' or \
                    part['token'] == 'minutes' or \
                    part['token'] == 'minute':
                h_m_s.append(part['token'])
    for i in range(1, len(h_m_s)):
        if h_m_s[i] == 'second' or h_m_s[i] == 'seconds':
            s = int(h_m_s[i - 1])
        if h_m_s[i] == 'minute' or h_m_s[i] == 'minutes':
            m = int(h_m_s[i - 1])
        if h_m_s[i] == 'hour' or h_m_s[i] == 'hours':
            h = int(h_m_s[i - 1])
    if not h and not s and not m:
        system('mpg123 /home/pi/Robot/src/audio/pleaseTellMeTheDurationOfTime.mp3')
        return
    Timer(hour=h, minute=m, sec=s)


def cancel_timer(query):
    pass


def show_holidays(query):
    pass
