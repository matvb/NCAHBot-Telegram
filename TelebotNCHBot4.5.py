import json
import requests
import time
import urllib
import telebot
import config
import random
from telebot import types


bot = telebot.TeleBot("651775329:AAGA5pCtTrlfbYnCalmhKUwGLrVrTjOWOxY")

#global variables

global questioning
questioning = False
global voting
voting = False
global currentQuestion
currentQuestion = " "
global justVoted
justVoted = False
global gameOn
gameOn = False
sizeOfHand = 5 #quantidade de cartas que se pode ter na mão
global markup
#lists
global choosenPhrase

# Answers given to a question
givenAnswers = list()
myAnswers = list()
gameQuestions = list()
joinedPeople = list()


# Create a string list and build it with append calls.
allQuestions = list()
with open("questions.txt") as myfile:
    for line in myfile:
        allQuestions.append(line)
myfile.close()

#OLD WAY
#allQuestions.append(" Se eu fosse presidente, o meu primeiro feito seria ___")


# allAnswers
allAnswers = list()
with open("answers.txt") as myfile2:
    for line in myfile2:
        allAnswers.append(line.replace("\n",""))
myfile2.close()
#OLD WAY
#allAnswers.append("Arroz com Feijão")



class joinedPerson():
    def __init__(self, name, id):
        self.name = name
        self.id = id


#Handlers

@bot.message_handler(commands=['join'])
def send_join(message):
    if (message.chat.first_name, message.chat.id) not in joinedPeople:   #erro
        joinedPeople.append(joinedPerson(message.chat.first_name, message.chat.id))
        bot.send_message(message.chat.id, message.chat.first_name + " entrou na brincadeira!")
    else:
        bot.send_message(message.chat.id, "Tu já tá, fera!")


@bot.message_handler(commands=['showJoined'])
def send_show_joined(message):
    bot.send_message(message.chat.id, "Lista de jogadores:")
    for person in joinedPeople:
        bot.send_message(message.chat.id, "Nome: " + person.name + " ID: " + str(person.id))


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, """Bot para jogar "Cards Against Humanity" mas com um nome menos agressivo.""")
    bot.send_message(message.chat.id, "by: Mateus Villas Boas")

@bot.message_handler(commands=['start'])
def send_start(message):
    global gameOn
    gameOn = True
    bot.send_message(message.chat.id, "Prontos ou não, começou o jogo!")

@bot.message_handler(commands=['stop'])
def send_stop(message):
    global gameOn
    global markup
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,"Xau" , reply_markup=markup)
    if gameOn:
        markup = types.ReplyKeyboardRemove()
        gameOn = False
        bot.send_sticker(message.chat.id, "CAADAQADDQADWAABkQe3VH-Hf1l1DAI")
    else:
        bot.send_message(message.chat.id, "Já nem tinha começado, otário!")

@bot.message_handler(commands=['banco_perguntas'])
def send_banco_perguntas(message):
    if len(gameQuestions) != len(allQuestions):
        bot.send_message(message.chat.id, "Inicializando Banco de Perguntas!")
        inicialize_gameQuestions()
        inicialize_my_answers()
    else:
        bot.send_message(message.chat.id, "Banco de Perguntas já está cheio!")


@bot.message_handler(func=lambda message: gameOn, commands=['pergunta'])
def send_question(message):
    global questioning
    global currentQuestion
    global markup
    questioning = True
    if len(gameQuestions) == 0:
        bot.send_message(message.chat.id, "<b>Embaralhando cartas de perguntas.</b>", parse_mode= 'HTML')
        inicialize_gameQuestions()
    if len(myAnswers) == 0:
        inicialize_my_answers()
    currentQuestion = gameQuestions[random.randint(0, len(gameQuestions)-1)]
    gameQuestions.remove(currentQuestion)
    bot.send_message(message.chat.id, "<b>Pergunta:</b>", parse_mode= 'HTML')
    bot.send_message(message.chat.id, currentQuestion, parse_mode= 'HTML')

    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    update_keyboard()
    bot.send_message(message.chat.id, "Cartas de perguntas restantes: " + str(len(gameQuestions)))
    bot.send_message(message.chat.id, "<b>Escolha sua resposta:</b>", reply_markup=markup, parse_mode= 'HTML')


@bot.message_handler(func=lambda message: gameOn, content_types=['text'])
def handle_texts(message):
    global questioning, voting
    global currentQuestion
    global justVoted
    global choosenPhrase

    def voting_mode():
        global justVoted
        justVoted = True
        markup = types.ReplyKeyboardMarkup(row_width=1)
        for answer in givenAnswers:
            markup.add(types.KeyboardButton(answer))
            givenAnswers.remove(answer)
        bot.send_message(message.chat.id, "<b>Qual a melhor resposta?</b>", reply_markup=markup, parse_mode= 'HTML')

    if justVoted:
        justVoted = False
        bot.send_message(message.chat.id, "<b>Tu votou!</b>", parse_mode= 'HTML')
        send_question(message)
    else:
        if questioning:
            if (message.text) in myAnswers:
                currentQuestion = currentQuestion.replace("___","<b>" + message.text + "</b>", 1)
                myAnswers.remove(message.text) #tira a resposta dada
                add_one_answer() #pega mais uma carta de resposta
                givenAnswers.append(message.text)
                if "___" in currentQuestion:
                    bot.send_message(message.chat.id, currentQuestion, parse_mode= 'HTML')
                    update_keyboard()
                    bot.send_message(message.chat.id, "<b>Escolha mais uma resposta:</b>", reply_markup=markup, parse_mode= 'HTML')
                else:
                    bot.send_message(message.chat.id, "Frase completa:", parse_mode= 'HTML')
                    bot.send_message(message.chat.id, currentQuestion, parse_mode= 'HTML')
                    questioning = False

                #voting = True
                #voting_mode()
#            else:
#                bot.send_message(message.chat.id, "Desculpe mas sua resposta não é uma resposta válida")
#                bot.send_message(message.chat.id, message.chat.first_name)
#        else:
#            bot.send_message(message.chat.id, "Calma jovem! Espere a pergunta!")

#functions

def update_keyboard():
    for answer in myAnswers:
        markup.add(types.KeyboardButton(answer))

#inicializa e enche a lista de perguntas
def inicialize_gameQuestions():
    for question in allQuestions:
        if question not in gameQuestions:
            gameQuestions.append(question)

def inicialize_my_answers():
    for i in range(0, sizeOfHand):
        add_one_answer()

def add_one_answer():
    answer = allAnswers[random.randint(0, len(allAnswers)-1)]
    myAnswers.append(answer)



bot.polling()
