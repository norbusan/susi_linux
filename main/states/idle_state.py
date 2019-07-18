"""Class to represent Idle State
"""

import logging
import os
import signal

from .base_state import State
from .lights import lights
from ..player import player

logger = logging.getLogger(__name__)


class IdleState(State):
    """Idle State inherits from the base state. In this state, app is actively listening for Hotword Input or Push
    Button Input. It transitions to Recognizing State upon successful detection.
    """

    def __init__(self, components):
        super().__init__(components)
        self.isActive = False
        self.components.hotword_detector.start()
        if self.components.hotword_detector is not None:
            self.components.hotword_detector.subject.subscribe(
                on_next=lambda x: self.__detected())
        if self.components.wake_button is not None:
            self.components.wake_button.subject.subscribe(
                on_next=lambda x: self.__detected())
        if self.components.renderer is not None:
            self.components.renderer.subject.subscribe(
                on_next=lambda x: self.__detected())

    def on_enter(self, payload=None):
        """Method to be executed on entry to Idle State. Detection is set to active.
        :param payload: Nothing is expected
        :return: None
        """
        lights.off()
        logger.debug('Idle state')
        self.isActive = True
        lights.wakeup()
        self.notify_renderer('idle')

    def __detected(self):
        if (self.isActive):
            player.beep(os.path.abspath(os.path.join(self.components.config['data_base_dir'],
                                                     self.components.config['detection_bell_sound'])),
                        mode = 'direct')
            self.transition(state=self.allowedStateTransitions.get(
                'recognizing'), payload=None)

    def on_exit(self):
        """Method to be executed on exit from Idle State. Detection of Hotword and Wake Button is paused.
        :return: None
        """
        self.isActive = False
        lights.off()
