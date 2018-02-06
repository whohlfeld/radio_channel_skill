from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from alsaaudio import Mixer
import random
import time
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None
from bs4 import BeautifulSoup
import requests


__author__ = 'whohlfeld'

LOGGER = getLogger(__name__)


DLF_URL = 'http://st01.dlf.de/dlf/01/128/mp3/stream.mp3'
DRADIO_URL = 'http://st02.dlf.de/dlf/02/128/mp3/stream.mp3'
NOVA_URL = 'http://st03.dlf.de/dlf/03/128/mp3/stream.mp3'
ENERGYHH_URL = 'http://185.52.127.131/de/33009/mp3_128.mp3'

URLS =[DLF_URL, DRADIO_URL, NOVA_URL, ENERGYHH_URL]
NAME = ["DLF","DRADIO","NOVA","ENERGY" ]

POSITION = 0


class RadioChannelSkill(MycroftSkill):
    def __init__(self):
        super(RadioChannelSkill, self).__init__(name="RadioChannelSkill")
        self.audioservice = None

    def initialize(self):
        if AudioService:
            self.audioservice = AudioService(self.emitter)

        random_intent = IntentBuilder("RandomIntent"). \
            require("TurnKeyword").require("RadioKeyword").require("OnKeyword").build()
        self.register_intent(random_intent, self.handle_random_intent)

        dlf_intent = IntentBuilder("DlfIntent").\
                     require("DlfKeyword").require("TurnKeyword").require("RadioKeyword").require("OnKeyword").build()
        self.register_intent(dlf_intent, self.handle_dlf_intent)

        dradio_intent = IntentBuilder("DradioIntent").\
                        require("DradioKeyword").require("TurnKeyword").require("RadioKeyword").require("OnKeyword").build()
        self.register_intent(dradio_intent, self.handle_dradio_intent)

        nova_intent = IntentBuilder("NovaIntent").\
                      require("NovaKeyword").require("TurnKeyword").require("RadioKeyword").require("OnKeyword").build()
        self.register_intent(nova_intent, self.handle_nova_intent)

        energyhh_intent = IntentBuilder("EnergyHHIntent"). \
            require("EnergyHHKeyword").require("TurnKeyword").require("RadioKeyword").require("OnKeyword").build()
        self.register_intent(energyhh_intent, self.handle_energyhh_intent)

        change_intent = IntentBuilder("ChangeIntent"). \
            require("ChangeKeyword").build()
        self.register_intent(change_intent, self.handle_change_intent)

    def handle_random_intent(self, message):
        nr = random.randint(0, 3)
        self.speak_dialog("currently", {"station": NAME[nr]})
        time.sleep(2)
        if self.audioservice:
            self.audioservice.play(URLS[nr], message.data['utterance'])
            global POSITION
            POSITION = nr
        else:
            self.process = play_mp3(URLS[nr])
            POSITION = nr


    def handle_dlf_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[0], message.data['utterance'])
            global POSITION
            POSITION = 0
        else:
            self.process = play_mp3(URLS[0])
            POSITION = 0

    def handle_dradio_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[1], message.data['utterance'])
            global POSITION
            POSITION = 1
        else:
            self.process = play_mp3(URLS[1])
            POSITION = 1

    def handle_nova_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[2], message.data['utterance'])
            global POSITION
            POSITION = 2
        else:
            self.process = play_mp3(URLS[2])
            POSITION = 2

    def handle_energyhh_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[3], message.data['utterance'])
            global POSITION
            POSITION = 3
        else:
            self.process = play_mp3(URLS[3])
            POSITION = 3

    def handle_change_intent(self, message):
        global POSITION
        self.speak_dialog("currently", {"station": NAME[POSITION+1]})
        mixer = Mixer()
        mixer.setvolume(2)
        time.sleep(2)
        mixer.setvolume(8)
        if self.audioservice:
            if POSITION < 3:
                self.audioservice.play(URLS[POSITION+1], message.data['utterance'])
                POSITION = POSITION + 1
            else:
                self.audioservice.play(URLS[0], message.data['utterance'])
                POSITION = 0
        else:
            if POSITION < 3:
                self.process = play_mp3(URLS[POSITION+1])
            else:
                self.process = play_mp3(URLS[0])


    def stop(self):
        pass


def create_skill():
    return RadioChannelSkill()
