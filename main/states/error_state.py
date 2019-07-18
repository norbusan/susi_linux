"""Class to represent Error State
"""
import logging
import os
import json_config
from .base_state import State
from .lights import lights
from ..player import player

config = json_config.connect('config.json')
logger = logging.getLogger(__name__)


class ErrorState(State):
    """Error State inherits from the State class. If any error is encountered in any state, it should transition to
    error mentioning the error in the payload.
    """

    def on_enter(self, payload=None):
        """Method executed on entry to Error State. Relevant error message is spoken.
        :param payload: String mentioning the error encountered.
        :return: None
        """
        if payload == 'RecognitionError':
            self.notify_renderer('error', 'recognition')
            lights.speak()
            player.say(os.path.abspath(os.path.join(self.components.config['data_base_dir'],
                                                    self.components.config['recognition_error_sound'])),
                       mode = 'direct')
            lights.off()
        elif payload == 'ConnectionError':
            self.notify_renderer('error', 'connection')
            config['default_tts'] = 'flite'
            config['default_stt'] = 'pocket_sphinx'
            print("Internet Connection not available")
            lights.speak()
            lights.off()
            logger.info("Changed to offline providers")
        else:
            print("Error: {} \n".format(payload))
            self.notify_renderer('error')
            lights.speak()
            player.say(os.path.abspath(os.path.join(self.components.config['data_base_dir'],
                                                    self.components.config['problem_sound'])),
                       mode = 'direct')
            lights.off()

        self.transition(self.allowedStateTransitions.get('idle'))

    def on_exit(self):
        """Method executed on exit from the Error State.
        :return: None
        """
        pass
