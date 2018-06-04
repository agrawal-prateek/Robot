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
    pass


def start_timer(query):
    pass


def cancel_timer(query):
    pass


def show_holidays(query):
    pass
