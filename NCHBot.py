import json
import requests
import time
import urllib
import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot("651775329:AAGA5pCtTrlfbYnCalmhKUwGLrVrTjOWOxY")

global questioning
questioning = False
global voting
voting = False
global currentQuestion
currentQuestion = " "

# Create a string list and build it with append calls.
allQuestions = list()
allQuestions.append(" Se eu fosse presidente, o meu primeiro feito seria ___")
#allQuestions.append("Minha manhã não está completa sem um belo copo de ___")
#allQuestions.append("Minha filha, tome cuidado, os garotos de hoje em dia só pensam em ___")
#allQuestions.append("Eu bebo para esquecer ___")
#allQuestions.append("Pai, porque a mamãe ta chorado? ___")
#allQuestions.append("Ei gatinha, vamos pra minha casa que eu te mostro ___")
#allQuestions.append("Com grandes poderes vem grandes ___")
#allQuestions.append("___ + ___ = ___")
allQuestions.append("___, ___ e ___ esses são os ingredientes para criar as garotinhas perfeitas")
allQuestions.append("Garçom, tem ___ na minha sopa")
#allQuestions.append("Você sabia que ___ é gay?")
#allQuestions.append("""no inicio havia ___, e então Deus falou "que se faça ___""")
#allQuestions.append("Tem ___ na minha bota!")

# allAnswers
allAnswers = list()
allAnswers.append("Arroz com Feijão")
allAnswers.append("Eri Johnson")
allAnswers.append("KiDoguinho")
allAnswers.append("Um baita de um matusquela xarope")
allAnswers.append("Ronaldo")
allAnswers.append("Menstruação")
allAnswers.append("Mamilos de Sócrates")
allAnswers.append("Shrek 2")
allAnswers.append("Caldo de Carne")

# Answers given to a question
answersGiven = list()
gameQuestions = list()

#Handlers

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Howdy, how are you doing?")


@bot.message_handler(commands=['pergunta'])
def send_question(message):
    global questioning
    global currentQuestion
    questioning = True
    currentQuestion = allQuestions[random.randint(0, len(allQuestions)-1)]
    bot.send_message(message.chat.id, currentQuestion, parse_mode= 'HTML')

    markup = types.ReplyKeyboardMarkup(row_width=1)
    for answer in allAnswers:
        markup.add(types.KeyboardButton(answer))
    bot.send_message(message.chat.id, "Escolha sua resposta:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_texts(message):
    global questioning, voting
    global currentQuestion
    if questioning:
        if message.text in allAnswers:
            #str = allQuestions[random.randint(0, len(allQuestions)-1)]
            #str.replace("___", message.text)
            bot.send_message(message.chat.id, currentQuestion.replace("___","<b>" + message.text + "</b>"), parse_mode= 'HTML')
            allAnswers.remove(message.text)
            answersGiven.append(message.text)
            questioning = False
            voting = True
        else:
            bot.send_message(message.chat.id, "Desculpe mas sua resposta não é uma resposta válida")
            #bot.reply_to(message, "Desculpe mas sua resposta não é uma resposta válida")
    else:
        if voting:
            markup = types.ReplyKeyboardMarkup(row_width=1)
            for answer in answersGiven:
                markup.add(types.KeyboardButton(answer))
            bot.send_message(message.chat.id, "Qual a melhor resposta?", reply_markup=markup)

        else:
            bot.send_message(message.chat.id, "Calma jovem! Espere a pergunta!")

bot.polling()

#functions

#inicializa e enche a lista de perguntas
def inicialize_gameQuestions():
    for question in allQuestions
        gameQuestions.append(question)


def main():
    #keyboard = build_keyboard(allAnswers)
    while(True):
        #keyboard = build_keyboard(allAnswers)
        #send_question(126943320)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
