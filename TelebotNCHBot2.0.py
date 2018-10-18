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
global justVoted
justVoted = False

# Create a string list and build it with append calls.
allQuestions = list()
allQuestions.append(" Se eu fosse presidente, o meu primeiro feito seria ___")
allQuestions.append("Minha manhã não está completa sem um belo copo de ___")
allQuestions.append("Minha filha, tome cuidado, os garotos de hoje em dia só pensam em ___")
allQuestions.append("Eu bebo para esquecer ___")
allQuestions.append("Pai, porque a mamãe ta chorado? ___")
allQuestions.append("Ei gatinha, vamos pra minha casa que eu te mostro ___")
allQuestions.append("Com grandes poderes vem grandes ___")
allQuestions.append("___ + ___ = ___")
allQuestions.append("___, ___ e ___ esses são os ingredientes para criar as garotinhas perfeitas")
allQuestions.append("Garçom, tem ___ na minha sopa")
allQuestions.append("Você sabia que ___ é gay?")
allQuestions.append("""no inicio havia ___, e então Deus falou "que se faça ___""")
allQuestions.append("Tem ___ na minha bota!")
allQuestions.append("#___ Não!")
allQuestions.append("Mais de 4 milhões de pessoas se juntaram ao centro do Rio em protesto para gritar: Fora ___!")
allQuestions.append("Toda vez que eu chego em casa, ___ da vizinha ta na minha cama")
allQuestions.append("Eu voto em ___, ___ vice!")
allQuestions.append("Lista de confirmados pra próxima São Pedro: 1 - ___ 2 - ___ 3 - ___")
allQuestions.append("Não fala comigo não, que hoje eu to me sentindo meio ___")


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
allAnswers.append("a mulher de branco")
allAnswers.append("a insustentável leveza do ser")
allAnswers.append("seu tio bolsominion")
allAnswers.append("contra-ataque fulminante pela esquerda")
allAnswers.append("Arnaldo César Coelho")
allAnswers.append("o macaco do Latino")
allAnswers.append("uma legging roxa")
allAnswers.append("Kit Gay")
allAnswers.append("a tampa do seu cu")
allAnswers.append("flora intestinal")
allAnswers.append("pacu assado")
allAnswers.append("Ace Ventura, o detetive animal")
allAnswers.append("a inquisição espanhola")
allAnswers.append("Renanzinho")
allAnswers.append("honra e glória de nosso senhor Jesus Cristo")
allAnswers.append("cuecas do Jimmy Neutron")
allAnswers.append("móveis coloniais de acaju")
allAnswers.append("Zé Gotinha")
allAnswers.append("um ano só de sexo anal")
allAnswers.append("sexo dos elefantes")
allAnswers.append("fanta-guaraná sabor laranja")
allAnswers.append("inseminação artifical de pandas")
allAnswers.append("mordidinhas na orelha")



# Answers given to a question
givenAnswers = list()
myAnswers = list()
gameQuestions = list()

#Handlers

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Bot para jogar "Cards Against Humanity" mas com um nome menos agressivo.""")
    bot.send_message(message.chat.id, "by: Mateus Villas Boas")

@bot.message_handler(commands=['banco_perguntas'])
def send_welcome(message):
    if len(gameQuestions) != len(allQuestions):
        bot.send_message(message.chat.id, "Inicializando Banco de Perguntas!")
        inicialize_gameQuestions()
        inicialize_my_answers()
    else:
        bot.send_message(message.chat.id, "Banco de Perguntas já está cheio!")


@bot.message_handler(commands=['pergunta'])
def send_question(message):
    global questioning
    global currentQuestion
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

    markup = types.ReplyKeyboardMarkup(row_width=1)
    for answer in myAnswers:
        markup.add(types.KeyboardButton(answer))
    bot.send_message(message.chat.id, "Quantidade de cartas de perguntas restantes: " + str(len(gameQuestions)))
    bot.send_message(message.chat.id, "<b>Escolha sua resposta:</b>", reply_markup=markup, parse_mode= 'HTML')



@bot.message_handler(content_types=['text'])
def handle_texts(message):
    global questioning, voting
    global currentQuestion
    global justVoted

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
            if message.text in myAnswers:
                bot.send_message(message.chat.id, currentQuestion.replace("___","<b>" + message.text + "</b>"), parse_mode= 'HTML')
                myAnswers.remove(message.text) #tira a resposta dada
                add_one_answer() #pega mais uma carta de resposta
                givenAnswers.append(message.text)
                questioning = False
                #voting = True
                voting_mode()
            else:
                bot.send_message(message.chat.id, "Desculpe mas sua resposta não é uma resposta válida")
                bot.send_message(message.chat.id, message.chat.first_name)
        else:
            bot.send_message(message.chat.id, "Calma jovem! Espere a pergunta!")

#functions

#inicializa e enche a lista de perguntas
def inicialize_gameQuestions():
    for question in allQuestions:
        if question not in gameQuestions:
            gameQuestions.append(question)

def inicialize_my_answers():
    for i in range(0, 2):
        add_one_answer()

def add_one_answer():
    answer = allAnswers[random.randint(0, len(allAnswers)-1)]
    myAnswers.append(answer)



bot.polling()




def main():
    #keyboard = build_keyboard(allAnswers)
    while(True):
        #keyboard = build_keyboard(allAnswers)
        #send_question(126943320)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
