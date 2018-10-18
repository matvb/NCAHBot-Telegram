# Create a string list and build it with append calls.
#questions = list()
#questions.append("Se eu fosse presidente, o meu primeiro feito seria ___")
#questions.append("Minha manhã não está completa sem um belo como de ___")
#questions.append("Minha filha, tome cuidado, os garotos de hoje em dia só pensam em ___")

# Display individual strings.
#for question in questions:
#    print(question)

#def send_question(chat_id):
#    text = questions[random.randint(0, 2)]
#    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
#    get_url(url)



import json
import requests
import time
import urllib

import config
import random

TOKEN = "651775329:AAGA5pCtTrlfbYnCalmhKUwGLrVrTjOWOxY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#NEW

# Create a string list and build it with append calls.
questions = list()
questions.append("Se eu fosse presidente, o meu primeiro feito seria ___")
questions.append("Minha manhã não está completa sem um belo como de ___")
questions.append("Minha filha, tome cuidado, os garotos de hoje em dia só pensam em ___")
questions.append("Eu bebo para esquecer ___")
questions.append("Pai, porque a mamãe ta chorado? ___")
questions.append("Ei gatinha, vamos pra minha casa que eu te mostro ___")
questions.append("Com grandes poderes vem grandes ___")

# ANSWERS
answers = list()
answers.append("Arroz com Feijão")
answers.append("Eri Johnson")
answers.append("KiDoguinho")
answers.append("Um baita de um matusquela xarope")
answers.append("Ronaldo")
answers.append("Menstruação")
answers.append("Mamilos de Sócrates")

Onoff = True

def send_question(chat_id):
    text = questions[random.randint(0, len(questions)-1)]
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def build_keyboard(answers):
    keyboard = [[answer] for answer in answers]
    #reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    #return json.dumps(reply_markup)

#OLD

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def start(bot, update):
    kb = [[telegram.KeyboardButton("Option 1")], [telegram.KeyboardButton("Option 2")]]
    kb_markup = telegram(chat_id=update.message.chat_id, text="your message", reply_markup=kb_markup)

    start_handler = RegexHandler('some-regex-here', start)
    dispatcher.add_handler(start_handler)

def teclad():
    send_question(126943320)
    send_question(126943320)

def main():
    #keyboard = build_keyboard(answers)
    while(True):
        #keyboard = build_keyboard(answers)
        #send_question(126943320)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
