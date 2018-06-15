import concurrent.futures
import json
import logging
import multiprocessing
import os
import os.path
import re
import sys
import uuid

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import grpc
import pathlib2 as pathlib
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception

from src.actions import alarm
from src.actions import call
from src.actions import display
from src.actions import restart
from src.actions import send
from src.actions import shutdown
from src.actions import sound
from src.actions import volume

from src.grpc import assistant_helpers, audio_helpers, device_helpers

ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
END_OF_UTTERANCE = embedded_assistant_pb2.AssistResponse.END_OF_UTTERANCE
DIALOG_FOLLOW_ON = embedded_assistant_pb2.DialogStateOut.DIALOG_FOLLOW_ON
CLOSE_MICROPHONE = embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE
DEFAULT_GRPC_DEADLINE = 185
assistant_query_and_response = multiprocessing.Manager().dict()
home_dir = os.path.expanduser('~')
started_timer = None


class SampleAssistant(object):
    def __init__(
            self, language_code, device_model_id, device_id, conversation_stream, channel, deadline_sec, device_handler
    ):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_stream = conversation_stream
        self.conversation_state = None
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)
        self.deadline = deadline_sec
        self.device_handler = device_handler

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False
        self.conversation_stream.close()

    def is_grpc_error_unavailable(e):
        is_grpc_error = isinstance(e, grpc.RpcError)
        if is_grpc_error and (e.code() == grpc.StatusCode.UNAVAILABLE):
            logging.error('grpc unavailable error: %s', e)
            return True
        return False

    @retry(reraise=True, stop=stop_after_attempt(3),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def assist(self):
        global started_timer
        device_actions_futures = []
        self.conversation_stream.start_recording()
        logging.info('Recording audio request.')

        def iter_assist_requests():
            for c in self.gen_assist_requests():
                assistant_helpers.log_assist_request_without_audio(c)
                yield c
            self.conversation_stream.start_playback()

        query = None
        assistant_response = False
        for resp in self.assistant.Assist(iter_assist_requests(), self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.event_type == END_OF_UTTERANCE:
                logging.info('End of audio request detected')
                self.conversation_stream.stop_recording()
            if resp.speech_results:
                query = ' '.join(r.transcript for r in resp.speech_results)
                query = query.lower()
            if len(resp.audio_out.audio_data) > 0:
                print(query)
                if query.find('') != -1:
                    if not assistant_response:
                        # Send Email
                        if re.search('(.*)send(.*)email(.*)', query):
                            send.send_email()
                            break

                        # Send Message
                        if re.search('(.*)send(.*)message(.*)', query) \
                                or re.search('(.*)cancel(.*)message(.*)', query):
                            send.send_message()
                            break

                        # Shut Down
                        elif re.search('(.*)shut down(.*)', query) \
                                or re.search('(.*)turn off(.*)', query):
                            shutdown.shutdown()
                            break

                        # Decrease Volume
                        elif re.search('(.*)turn(.*)down(.*)volume(.*)', query) \
                                or re.search('(.*)decrease(.*)volume(.*)', query) \
                                or re.search('(.*)slow(.*)volume(.*)', query):
                            volume.decrease()
                            break

                        # Increase Volume
                        elif re.search('(.*)turn(.*)up(.*)volume(.*)', query) \
                                or re.search('(.*)increase(.*)volume(.*)', query) \
                                or re.search('(.*)high(.*)volume(.*)', query) \
                                or re.search('(.*)speak(.*)loud(.*)', query):
                            volume.increase()
                            break

                        # Tell me about This image
                        elif re.search('(.*)tell(.*)this(.*)image(.*)', query) \
                                or re.search('(.*)know(.*)this(.*)image(.*)', query) \
                                or re.search('(.*)tell(.*)this(.*)picture(.*)', query) \
                                or re.search('(.*)know(.*)this(.*)image(.*)', query):
                            display.tell_about_image()
                            break

                        # Show Pictures
                        elif re.search('(.*)show(.*)pictures(.*)', query):
                            display.show_images(query)
                            break

                        # Show Calender
                        elif re.search('(.*)show(.*)calender(.*)', query):
                            display.show_calender(query)
                            break

                        # Show videos
                        elif re.search('(.*)show(.*)trailer(.*)', query) \
                                or re.search('(.*)show(.*)youtube(.*)', query) \
                                or re.search('(.*)show(.*)video(.*)', query) \
                                or re.search('(.*)show(.*)recipe(.*)', query) \
                                or re.search('(.*)play(.*)video(.*)', query) \
                                or re.search('(.*)play(.*)videos(.*)', query):
                            display.show_video(query)
                            break

                        # Show Holiday
                        elif re.search('(.*)show(.*)holiday(.*)', query) \
                                or re.search('(.*)show(.*)holidays(.*)', query):
                            display.show_holidays(query)
                            break

                        # Timer or Named Timer
                        elif re.search('(.*)start(.*)timer(.*)', query) \
                                or re.search('(.*)set(.*)timer(.*)', query):
                            started_timer = multiprocessing.Process(target=display.start_timer, args=(query,))
                            started_timer.start()
                            break

                        # Cancel Timer
                        elif re.search('(.*)cancel(.*)timer(.*)', query) \
                                or re.search('(.*)remove(.*)timer(.*)', query):
                            if started_timer:
                                started_timer.terminate()
                                started_timer = None
                            break

                        # Music
                        elif re.search('(.*)play(.*)music(.*)', query) \
                                or re.search('(.*)play(.*)song(.*)', query) \
                                or re.search('(.*)start(.*)music(.*)', query) \
                                or re.search('(.*)start(.*)song(.*)', query):
                            sound.play(query)
                            break

                        # Restart
                        elif re.search('(.*)restart(.*)', query):
                            restart.restart_task(query)
                            break

                        # Set Alarm
                        elif re.search('(.*)set(.*)alarm(.*)', query) \
                                or re.search('(.*)wake(.*)me(.*)', query):
                            alarm.set_alarm(query)
                            break

                        # Cancel Alarm
                        elif re.search('(.*)cancel(.*)alarm(.*)', query) \
                                or re.search('(.*)remove(.*)alarm(.*)', query):
                            alarm.cancel_alarm(query)
                            break

                        # Call
                        elif re.search('(.*)make(.*)call(.*)', query):
                            call.make_call(query)
                            break

                        # Abort Call
                        elif re.search('(.*)hang(.*)up(.*)', query) \
                                or re.search('(.*)abort(.*)call(.*)', query):
                            call.abort_call(query)
                            break

                        # Get Price
                        elif re.search('(.*)tell(.*)price(.*)', query):
                            break

                        # Throw/Roll a dice
                        elif re.search('(.*)roll(.*)dice(.*)', query) \
                                or re.search('(.*)throw(.*)dice(.*)', query):
                            break

                        # Flip a coin
                        elif re.search('(.*)flip(.*)coin(.*)', query) \
                                or re.search('(.*)throw(.*)coin(.*)', query):
                            break

                        # Random No.
                        elif re.search('(.*)pick(.*)between(.*)', query) \
                                or re.search('(.*)random(.*)between(.*)', query):
                            break

                        # Definition of a word
                        elif re.search('(.*)what(.*)mean(.*)', query) \
                                or re.search('(.*)how(.*)define(.*)', query):
                            break

                        # Spell a word
                        elif re.search('(.*)how(.*)spell(.*)', query):
                            break

                        # Sports
                        elif re.search('for sports', query):
                            break

                        # Send to tablet
                        elif re.search('(.*)send(.*)my(.*)tablet(.*)', query) \
                                or re.search('(.*)show(.*)my(.*)tablet(.*)', query) \
                                or re.search('(.*)show(.*)my(.*)tab(.*)', query):
                            break

                        # Show current screen to other`s tablet
                        elif re.search('(.*)show(.*)on(.*)tablet(.*)', query) \
                                or re.search('(.*)show(.*)on(.*)tab(.*)', query):
                            break

                        # Lights ON/OFF
                        elif re.search('(.*)(turn|switch)(.*)(on|off)(.*)', query):
                            break

                        # To Dim Lights/fan
                        elif re.search('(.*)dim(.*)', query):
                            break

                        # Temperature
                        elif re.search('(.*)set(.*)temperature(.*)', query) \
                                or re.search('(.*)raise(.*)temperature(.*)', query):
                            break

                        # Door Lock
                        elif re.search('(.*)lock(.*)door(.*)', query) \
                                or re.search('(.*)lock(.*)gate(.*)', query):
                            break

                        # Discover/Find Devices
                        elif re.search('(.*)discover(.*)device(.*)', query) \
                                or re.search('(.*)find(.*)my(.*)device(.*)', query) \
                                or re.search('(.*)where(.*)device(.*)', query):
                            break

                        # Bluetooth
                        elif re.search('(.*)connect(.*)to(.*)', query) \
                                or re.search('(.*)bluetooth(.*)', query):
                            break

                        # Switch Account
                        elif re.search('(.*)switch(.*)account(.*)', query):
                            break

                        # Get Profile
                        elif re.search('(.*)whose(.*)profile(.*)', query) \
                                or re.search('(.*)who(.*)is(.*)this(.*)', query):
                            break

                        # GOOD Morning
                        elif re.search('(.*)good(.*)morning(.*)', query):
                            break

                        # Tell a joke
                        elif re.search('(.*)tell(.*)joke(.*)', query):
                            break

                        else:
                            assistant_response = True
                    if assistant_response:
                        self.conversation_stream.write(resp.audio_out.audio_data)
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                logging.debug('Updating conversation state.')
                self.conversation_state = conversation_state
            if resp.device_action.device_request_json:
                device_request = json.loads(
                    resp.device_action.device_request_json
                )
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)

        if len(device_actions_futures):
            logging.info('Waiting for device executions to complete.')
            concurrent.futures.wait(device_actions_futures)

        logging.info('Finished playing assistant response.')
        self.conversation_stream.stop_playback()
        return query

    def gen_assist_requests(self):
        dialog_state_in = embedded_assistant_pb2.DialogStateIn(
            language_code=self.language_code,
            conversation_state=b''
        )
        if self.conversation_state:
            logging.debug('Sending conversation state.')
            dialog_state_in.conversation_state = self.conversation_state
        config = embedded_assistant_pb2.AssistConfig(
            audio_in_config=embedded_assistant_pb2.AudioInConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
            ),
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
                volume_percentage=self.conversation_stream.volume_percentage,
            ),
            dialog_state_in=dialog_state_in,
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id=self.device_id,
                device_model_id=self.device_model_id,
            )
        )
        yield embedded_assistant_pb2.AssistRequest(config=config)
        for data in self.conversation_stream:
            yield embedded_assistant_pb2.AssistRequest(audio_in=data)


def main():
    api_endpoint = ASSISTANT_API_ENDPOINT
    project_id = 'linux-ai'
    device_model_id = 'linuxai-200815-linux-ai-znrszd'
    device_id = 'a052c58c-3dac-11e8-9cf3-2c6e851f5f04'
    device_config = home_dir + '/Robot/src/credentials/googlesamples-assistant/device_config.json'
    credentials = home_dir + '/Robot/src/credentials/google-oauthlib-tool/credentials.json'
    lang = 'en-US'
    verbose = False
    audio_sample_rate = audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE
    audio_sample_width = audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH
    audio_iter_size = audio_helpers.DEFAULT_AUDIO_ITER_SIZE
    audio_block_size = audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
    audio_flush_size = audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
    grpc_deadline = DEFAULT_GRPC_DEADLINE

    # Setup logging.
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        os.system('mpg123 /home/pi/Robot/src/audio/networkNotFound.mp3')

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    # Configure audio source and sink.
    audio_device = None
    audio_source = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
    )
    audio_sink = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
    )
    # Create conversation stream with the given audio source and sink.
    conversation_stream = audio_helpers.ConversationStream(
        source=audio_source,
        sink=audio_sink,
        iter_size=audio_iter_size,
        sample_width=audio_sample_width,
    )
    if not device_id or not device_model_id:
        try:
            with open(device_config) as f:
                device = json.load(f)
                device_id = device['id']
                device_model_id = device['model_id']
                logging.info("Using device model %s and device id %s",
                             device_model_id,
                             device_id)
        except Exception as e:
            logging.warning('Device config not found: %s' % e)
            logging.info('Registering device')
            if not device_model_id:
                logging.error('Option --device-model-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            if not project_id:
                logging.error('Option --project-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            device_base_url = (
                    'https://%s/v1alpha2/projects/%s/devices' % (api_endpoint,
                                                                 project_id)
            )
            device_id = str(uuid.uuid1())
            payload = {
                'id': device_id,
                'model_id': device_model_id,
                'client_type': 'SDK_SERVICE'
            }
            session = google.auth.transport.requests.AuthorizedSession(
                credentials
            )
            r = session.post(device_base_url, data=json.dumps(payload))
            if r.status_code != 200:
                logging.error('Failed to register device: %s', r.text)
                sys.exit(-1)
            logging.info('Device registered: %s', device_id)
            pathlib.Path(os.path.dirname(device_config)).mkdir(exist_ok=True)
            with open(device_config, 'w') as f:
                json.dump(payload, f)

    device_handler = device_helpers.DeviceRequestHandler(device_id)

    with SampleAssistant(
            lang, device_model_id, device_id, conversation_stream, grpc_channel, grpc_deadline, device_handler
    ) as assistant:
        os.system('mpg123 /home/pi/Robot/src/audio/ping.mp3')
        assistant.assist()


def start_robot():
    while True:
        try:
            main()
        except Exception as e:
            print(e)
