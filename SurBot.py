#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import subprocess
import os
import time
from telebot import types

######### VARIABLES ##########

global motion_started
motion_started = False
global process
msg_id = 0 # Set your own msg id

TOKEN='x' # Set you own token
bot = telebot.TeleBot(TOKEN)

######### COMMANDS ###########

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == "private" and message.from_user.id == 174335612:
       cid = message.chat.id
       bot.send_message(message.chat.id, "Welcome. Use /help for a list of commands")
    else:
       bot.send_message(message.chat.id, "Private bot")

@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, "TODO")

@bot.message_handler(commands=['get_feed'])
def command_feed(message):
    words = message.text.split()
    if len(words) < 2 or int(words[1]) < 10:
       l = 10
    else:
       l = int(words[1])
    bot.send_message(message.chat.id, "Capturing " + str(l) + " seconds video...")
    if not motion_started:
	process = subprocess.Popen('sudo motion -c /etc/motion/motion_record.conf', shell=True)
	time.sleep(l)
	os.system('sudo kill ' + str(process.pid + 1))
        process.kill()
    else:
	    bot.send_message(message.chat.id, "Surveilance is up")

@bot.message_handler(commands=['start_surveilance'])
def command_start_surv(message):
    global motion_started
    global process
    if not motion_started:
        motion_started = True
	process = subprocess.Popen('sudo motion', shell=True)
        bot.send_message(message.chat.id, "Starting sureveilance")
    else:
        bot.send_message(message.chat.id, "Surveillance already up")

@bot.message_handler(commands=['stop_surveilance'])
def command_stop_surv(message):
    global motion_started
    global process
    if motion_started:
        bot.send_message(message.chat.id, "Stoping surveilance")
        motion_started = False
	os.system('sudo kill ' + str(process.pid + 1))
	process.kill()
    else:
        bot.send_message(message.chat.id, "Surveillance already down")

@bot.message_handler(commands=['clear_files'])
def command_clear(message):
    os.system('sudo rm -f /var/lib/motion/*')
    bot.send_message(message.chat.id, "Temporal files deleted")

bot.polling()
