from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
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

POSITION = 0


class RadioChannelSkill(MycroftSkill):
    def __init__(self):
        super(RadioChannelSkill, self).__init__(name="DlfSkill")
        self.audioservice = None

    def initialize(self):
        if AudioService:
            self.audioservice = AudioService(self.emitter)
        '''
        whatson_dlf_intent = IntentBuilder("WhatsonDlfIntent").\
                         require("WhatsonKeyword").\
                         require("DlfKeyword").build()
        self.register_intent(whatson_dlf_intent, self.handle_whatson_dlf_intent)

        whatson_dradio_intent = IntentBuilder("WhatsonDradioIntent").\
                                require("WhatsonKeyword").\
                                require("DradioKeyword").build()
        self.register_intent(whatson_dradio_intent,
                             self.handle_whatson_dradio_intent)

        whatson_nova_intent = IntentBuilder("WhatsonNovaIntent").\
                              require("WhatsonKeyword").\
                              require("NovaKeyword").build()
        self.register_intent(whatson_nova_intent,
                             self.handle_whatson_nova_intent)
        '''
        dlf_intent = IntentBuilder("DlfIntent").\
                     require("DlfKeyword").require("PlayKeyword").build()
        self.register_intent(dlf_intent, self.handle_dlf_intent)

        dradio_intent = IntentBuilder("DradioIntent").\
                        require("DradioKeyword").require("PlayKeyword").build()
        self.register_intent(dradio_intent, self.handle_dradio_intent)

        nova_intent = IntentBuilder("NovaIntent").\
                      require("NovaKeyword").require("PlayKeyword").build()
        self.register_intent(nova_intent, self.handle_nova_intent)

        energyhh_intent = IntentBuilder("EnergyHHIntent"). \
            require("EnergyHHKeyword").require("PlayKeyword").build()
        self.register_intent(energyhh_intent, self.handle_energyhh_intent)

        next_intent = IntentBuilder("NextIntent"). \
            require("NextKeyword").build()
        self.register_intent(next_intent, self.handle_next_intent)

    '''
    
    def handle_whatson_dlf_intent(self, message):
        r = requests.get('http://www.deutschlandfunk.de')
        soup = BeautifulSoup(r.text)
        for el in soup.find_all(id='dlf-player-jetzt-im-radio'):
            for a_el in el.find_all('a'):
                self.speak_dialog("currently",
                                  { "station": "dlf", "title": a_el.string})

    def handle_whatson_dradio_intent(self, message):
        r = requests.get('http://www.deutschlandfunkkultur.de/')
        soup = BeautifulSoup(r.text)
        for el in soup.find_all(id='drk-player-jetzt-im-radio'):
            for a_el in el.find_all('a'):
                self.speak_dialog("currently",
                                  { "station": "dlf culture", "title": a_el.string})

    def handle_whatson_nova_intent(self, message):
        r = requests.get('https://www.deutschlandfunknova.de/actions/dradio/playlist/onair')
        j = r.json() 
        
        self.speak_dialog("currently",
                          {"station": "dlf nova", "title": j['show']['title']})

    '''

    def handle_dlf_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[0], message.data['utterance'])
            global POSITION
            POSITION = 0
        else:
            self.process = play_mp3(URLS[0])

    def handle_dradio_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[1], message.data['utterance'])
            global POSITION
            POSITION = 1
        else:
            self.process = play_mp3(URLS[1])

    def handle_nova_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[2], message.data['utterance'])
            global POSITION
            POSITION = 2
        else:
            self.process = play_mp3(URLS[2])

    def handle_energyhh_intent(self, message):
        if self.audioservice:
            self.audioservice.play(URLS[3], message.data['utterance'])
            global POSITION
            POSITION = 3
        else:
            self.process = play_mp3(URLS[3])

    def handle_next_intent(self, message):
        global POSITION
        if self.audioservice:
            self.audioservice.play(URLS[POSITION+1], message.data['utterance'])
            POSITION = POSITION + 1
        else:
            self.process = play_mp3(URLS[POSITION+1])

    def stop(self):
        pass


def create_skill():
    return RadioChannelSkill()
