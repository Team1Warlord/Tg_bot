# import os
import telebot

bot = telebot.TeleBot("5996245674:AAHU7X6-6queXZEFLbYSmeM51foeMMx9Kuo");


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Приветствую Вас в боте по изучению иностранных языков. Для продолжения напишите /help")
    

button1 = telebot.types.InlineKeyboardButton('Добавление слова в словарь', callback_data = 'addw')
button2 = telebot.types.InlineKeyboardButton('Добавление пройденного урока', callback_data = 'addles')
button3 = telebot.types.InlineKeyboardButton('Вывод перевода ранее добавленного слова', callback_data = 'giveTr')
button4 = telebot.types.InlineKeyboardButton('Вывод пройденных уроков в данную дату', callback_data = 'giveLess')

keyb_helping =  telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(button1).add(button2).add(button3).add(button4)

@bot.message_handler(content_types=['text', 'document', 'audio'])
def replying(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Выберите нужный вариант.", reply_markup=keyb_helping)
        # bot.send_message(message.from_user.id, "/addword добавит слово в словарь. /addlesson добавит урок в список пройденных. /translate переведет слово если оно есть в словаре. /lessons выведет уроки проведенные в данную дату.");
    elif message.text == "/addword":
        bot.send_message(message.from_user.id, "Напиши слово для которого ты хочешь добавить перевод");
        bot.register_next_step_handler(message, get_word);
    # elif message.text == "/addlesson":
    #     bot.register_next_step_handler(message, get_lessons);
    # elif message.text == "/translate":
    #     bot.register_next_step_handler(message, give_translate);
    # elif message.text == "/lessons":
    #     bot.register_next_step_handler(message, give_lessons);
    else:
        bot.send_message(message.from_user.id, "Мая твая не паниматб. Напиши /help.")
     
word = '';
Translation = '';
  
def get_word(message):
    global word;
    word = message.text;
    bot.send_message(message.from_user.id, 'Какой перевод у этого слова?')
    bot.register_next_step_handler(message, get_wordTransl);

def get_wordTransl(message):
    global Translation;
    Translation = message.text;
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3);
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= telebot.types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Слово '+word+' переводится как '+Translation+'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def replyer_to_addTrans(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню');
    elif call.data == "no":
        bot.register_next_step_handler(call.message, get_word);
    
    
# @bot.message_handler(commands=['help'])
# def send_help(message):
# 	bot.reply_to(message, "Тут будет описание команд.")

bot.infinity_polling()
