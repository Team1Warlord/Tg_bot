
# import os
import telebot
from SQlite import SQlite as SQ
from AbstractRepo import WordTransl as wt
from AbstractRepo import Websites as ws
from AbstractRepo import Lesson_data as ld
from datetime import datetime
import markdown
from aiogram.utils.markdown import link


bot = telebot.TeleBot("")

DB_FILE = 'database.db'


def bind_database():
    db_name = DB_FILE
    SQ.bind(db_name)

bind_database()
wordTranslation_repo = SQ[wt](wt, wt.__name__)
lesson_data_repo = SQ[ld](ld, ld.__name__)
websites_repo = SQ[ws](ws, ws.__name__)


text_welcome = link('Создатель ботa', 'https://vk.com/kot_bhe_3akoha')


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Приветствую *Вас* в боте по изучению _иностранных языков_." +text_welcome+ ". Данный бот имеет несколько функций, выбирать между которыми вы можете нажимая на кнопки ниже.", reply_markup = keyb_helping, parse_mode="Markdown")


button = []
button.append(telebot.types.InlineKeyboardButton('Добавление слова в словарь'))
button.append(telebot.types.InlineKeyboardButton('Добавление пройденного урока'))
button.append(telebot.types.InlineKeyboardButton('Вывод перевода ранее добавленного слова'))
button.append(telebot.types.InlineKeyboardButton('Вывод пройденных уроков в данную дату'))
button.append(telebot.types.InlineKeyboardButton('Вывод всех пройденных уроков'))
button.append(telebot.types.InlineKeyboardButton('Вывод всеx записанных слов'))
button.append(telebot.types.InlineKeyboardButton('Полезные ресурсы по изучению иностранных языков'))


keyb_helping =  telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

for i in button:
    keyb_helping.add(i)
    
    
@bot.message_handler(content_types=['text'])
def replying(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Выберите нужный вариант.", reply_markup=keyb_helping)
        # bot.send_message(message.from_user.id, "/addword добавит слово в словарь. /addlesson добавит урок в список пройденных. /translate переведет слово если оно есть в словаре. /lessons выведет уроки проведенные в данную дату.")
    elif message.text == "Добавление слова в словарь":
        bot.send_message(message.from_user.id, "Напиши слово для которого ты хочешь добавить перевод")
        bot.register_next_step_handler(message, get_word)
    elif message.text == "Добавление пройденного урока":
        bot.send_message(message.from_user.id, "Введите дату пройденного урока в формате дд.мм.гггг.")
        bot.register_next_step_handler(message, get_date_of_lesson)
    elif message.text == "Вывод перевода ранее добавленного слова":
        bot.send_message(message.from_user.id, "Напиши слово для которого ты хочешь получить перевод")
        bot.register_next_step_handler(message, give_translate)
    elif message.text == "Вывод пройденных уроков в данную дату":
        bot.send_message(message.from_user.id, "Напиши дату *проведенного* урока", parse_mode="Markdown")
        bot.register_next_step_handler(message, give_lessons)
    elif message.text == "Вывод всех пройденных уроков":
        givelesson = lesson_data_repo.get_all()
        give_lesson = 'Сохраненные в базе данных уроки:\n\n'
        for i in givelesson:
            give_lesson = give_lesson + f"{i.date}  -  {i.theme}  -  {i.difficulty}\n"
        bot.send_message(message.from_user.id, give_lesson, reply_markup=keyb_helping)
    elif message.text == "Вывод всеx записанных слов":
        giveword = wordTranslation_repo.get_all()
        give_word = 'Сохраненные в базе данных слова:\n\n'
        for i in giveword:
            give_word = give_word + f"{i.word}  =  {i.translation}\n"
        bot.send_message(message.from_user.id, give_word, reply_markup=keyb_helping)
    elif message.text == 'Полезные ресурсы по изучению иностранных языков':
        # link1 = link('Moodle\n\n', 'https://moodle.phystech.edu/')
        # link2 = link('Англo английский словарь\n\n', 'https://dictionary.cambridge.org/')
        # link3 = link('Техническая библиотека с статьями на английском\n\n', 'https://www.ieee.org/')
        # text = link1 + link2 + link3
        givewebsite = websites_repo.get_all()
        give_website = 'Сохраненные в базе данных полезные вебсайты:\n\n'
        for i in givewebsite:
            text_link = link(f'{i.website_name}', f'{i.link}')
            give_website = give_website + text_link + "\n\n"
        bot.send_message(message.from_user.id, give_website, parse_mode="Markdown")
        bot.send_message(message.from_user.id, "_Не хотите ли добавить полезный ресурс?_", reply_markup=keyb_func('web_add'), parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Мая твая не паниматб. Напиши /help.")


word = ''
Translation = ''



def keyb_func(operation: str): 
    AgreementKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data=f"{operation}|yes") #кнопка «Да»
    AgreementKeyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= telebot.types.InlineKeyboardButton(text='Нет', callback_data=f"{operation}|no")
    AgreementKeyboard.add(key_no)
    return AgreementKeyboard

def get_word(message):
    global word
    word = message.text
    bot.send_message(message.from_user.id, 'Какой перевод у этого слова?')
    bot.register_next_step_handler(message, get_wordTransl)

def get_wordTransl(message):
    global Translation
    Translation = message.text
    question = 'Слово "'+word+'" переводится как "'+Translation+'"?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyb_func('translation'))
    # bot.register_callback_query_handler(replyer_to_addTrans, lambda call: call.data == 'word_yes' or 'word_no')
    
def give_translate(message):
    getword = message.text
    compr = wordTranslation_repo.get_all({'word':getword})
    if compr == []:
        bot.send_message(message.from_user.id, "Такого слова в словаре нема, занесите его в словарь", reply_markup=keyb_helping)
    else:
        bot.send_message(message.from_user.id, 'Перевод "'+getword+'" --- "'+compr[0].translation+'".', reply_markup=keyb_helping)
    
def get_date_of_lesson(message):
    global date
    global date_text
    date_text = message.text
    try:
        date = datetime.strptime(date_text, '%d.%m.%Y')
        bot.send_message(message.from_user.id, 'Какова тема пройденного урока?')
        bot.register_next_step_handler(message, get_theme_of_lesson)
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный формат даты, попробуйте снова', reply_markup=keyb_helping)

def get_theme_of_lesson(message):
    global theme
    theme = message.text
    bot.send_message(message.from_user.id, 'Какая сложность пройденного урока? Оценивайте по шкале от 1 до 10')
    bot.register_next_step_handler(message, get_difficulty_of_lesson)

def get_difficulty_of_lesson(message):
    global difficulty
    global difficulty_str
    difficulty_str = message.text
    try:
        difficulty = int(difficulty_str)
        question = 'Урок по теме '+theme+' прошел '+date_text+', по сложности был оценен на '+difficulty_str+', все верно?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyb_func('add_lesson'))
        # bot.register_callback_query_handler(replyer_to_addlesson, lambda call: call.data == 'lesson_yes' or 'lesson_no')
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный формат сложности, попробуйте снова', reply_markup=keyb_helping)
        
def give_lessons(message):
    getdate = message.text
    compr = lesson_data_repo.get_all({'date':getdate})
    if compr == []:
        bot.send_message(message.from_user.id, "Такого урока в базе данных нет, занесите его", reply_markup=keyb_helping)
    else:
        bot.send_message(message.from_user.id, 'Урок по теме "'+compr[0].theme+'" прошел "'+compr[0].date+'" и был оценен по сложности на '+str(compr[0].difficulty)+'', reply_markup=keyb_helping)

def get_website_name(message):
    global get_web_name
    get_web_name = message.text
    bot.send_message(message.from_user.id, 'Вставьте ссылку на этот сайт')
    bot.register_next_step_handler(message, get_website_link)
    
def get_website_link(message):
    global get_web_link
    get_web_link = message.text
    web_name_with_link = link(f'{get_web_name}', f'{get_web_link}')
    bot.send_message(message.from_user.id, 'Верно ли введены название и ссылка на ресурс ' +web_name_with_link+'?', reply_markup=keyb_func('add_web_last'), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def replyer(call):
    if call.data == "translation|yes":
        word_translation = wt(word, Translation)
        wordTranslation_repo.add(word_translation)
        bot.send_message(call.message.chat.id, 'Запомню', reply_markup=keyb_helping)
        bot.register_next_step_handler(call.message, replying)
    elif call.data == "translation|no":
        bot.send_message(call.message.chat.id, 'Ошиблись? Попробуйте еще раз', reply_markup=keyb_helping)
        bot.register_next_step_handler(call.message, replying)
    elif call.data == "add_lesson|yes":
        lesson_data = ld(date_text, theme, difficulty)
        lesson_data_repo.add(lesson_data)
        bot.send_message(call.message.chat.id, 'Запомню', reply_markup=keyb_helping)
        bot.register_next_step_handler(call.message, replying)
    elif call.data == "add_lesson|no":
        bot.send_message(call.message.chat.id, 'Ошиблись? Попробуйте еще раз', reply_markup=keyb_helping)
        bot.register_next_step_handler(call.message, replying)
    elif call.data == "web_add|yes":
        bot.send_message(call.message.chat.id, 'Введите наименование вебсайта')
        bot.register_next_step_handler(call.message, get_website_name)
    elif call.data == "web_add|no":
        bot.send_message(call.message.chat.id, 'Хорошо', reply_markup=keyb_helping)
    elif call.data == "add_web_last|yes":
        website = ws(get_web_name, get_web_link)
        websites_repo.add(website)
        bot.send_message(call.message.chat.id, 'Запомню', reply_markup=keyb_helping)
        bot.register_next_step_handler(call.message, replying)
    elif call.data == "add_web_last|no":
        bot.send_message(call.message.chat.id, 'Ошиблись? Попробуйте еще раз')
        bot.send_message(call.message.chat.id, 'Введите наименование вебсайта')
        bot.register_next_step_handler(call.message, get_website_name)
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)




# @bot.callback_query_handler(func=lambda call: call.data == 'lesson_yes' or 'lesson_no')
# def replyer_to_addlesson(call):
#     if call.data == "yes":
#         lesson_data = ld(date_text, theme, difficulty)
#         lesson_data_repo.add(lesson_data)
#         bot.send_message(call.message.chat.id, 'Запомню', reply_markup=keyb_helping)
#         bot.register_next_step_handler(call.message, replying)
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Урок по теме '+theme+' прошел '+date_text+', по сложности был оценен на '+difficulty_str+', все верно?', reply_markup=None)
#     elif call.data == "no":
#         bot.send_message(call.message.chat.id, 'Ошиблись? Попробуйте еще раз', reply_markup=keyb_helping)
#         bot.register_next_step_handler(call.message, replying)
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Урок по теме '+theme+' прошел '+date_text+', по сложности был оценен на '+difficulty_str+', все верно?', reply_markup=None)
    
    
    
# @bot.message_handler(commands=['help'])
# def send_help(message):
#  	bot.reply_to(message, "Тут будет описание команд.")

bot.infinity_polling()
