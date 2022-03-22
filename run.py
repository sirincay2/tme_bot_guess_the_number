#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import traceback
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

from datetime import datetime

"""
$ python3.5 guess.py <token>
Guess a number:
1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a guess.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until guess is correct.
"""

class Player(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._answer = random.randint(0,99)
        self.start_time = datetime.utcnow()
        print(self._answer)

    def _hint(self, answer, guess):
        if answer > guess:
            return 'Больше'
        else:
            return 'Меньше'

    def open(self, initial_msg, seed):
        self.sender.sendMessage('Привет, {} ! Угадай число от 1 до 99'.format(initial_msg["from"]["first_name"]))
        return True  # prevent on_message() from being called on the initial message

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.sender.sendMessage('Надо ответить числом.')
            return

        try:
           guess = int(msg['text'])
        except ValueError:
            self.sender.sendMessage('Надо ответить числом.')
            return

        # check the guess against the answer ...
        if guess != self._answer:
            # give a descriptive hint
            hint = self._hint(self._answer, guess)
            self.sender.sendMessage(hint)
        else:
            delta = datetime.utcnow() - self.start_time
            self.sender.sendMessage(
                'Угадал !!! Время {} секунд'.format(
                    delta.total_seconds()
                )
            )
            self.close()

    def on__idle(self, event):
        self.sender.sendMessage('Хорошая попытка. Время вышло. Правильный ответ %d' % self._answer)
        self.close()


TOKEN = "1825127997:AAGsCaKlDqls_ivyqE3XvZmEdLl6nDkEACg"

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=30),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
