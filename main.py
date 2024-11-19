import telebot
import time, json
# import requests
# from parser import Client
from test import test
from utils import get_duration, get_formated_date

TOKEN = None
with open("token.txt") as f:
  TOKEN = f.read().strip()

IDs = list()
with open("admin_ids.txt") as f:
  ids = f.read().strip()
  ids = ids.split(',')
  for id in ids:
    IDs.append(int(id))

bot = telebot.TeleBot(TOKEN)

from telebot import types

def user_has_rights(message):
  if message.from_user.id not in IDs:
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')
    return False
  return True

def get_menu(user):
  markup = types.InlineKeyboardMarkup()
  # button_change = types.InlineKeyboardButton(text = 'Показать изменение цен', callback_data='change')
  # markup.add(button_change)
  button_info = types.InlineKeyboardButton(text = 'Показать товары в наличии', callback_data='info')
  markup.add(button_info)
  active = 'Выключить' if user['activate'] else 'Включить'
  button_activate = types.InlineKeyboardButton(text = active + ' оповещения', callback_data='off' if user['activate'] else 'on')
  markup.add(button_activate)
  button_discount = types.InlineKeyboardButton(text = 'Указать скидку', callback_data='discount')
  markup.add(button_discount)
  return markup

def get_alt_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('😸')
  btn2 = types.KeyboardButton('😻')
  btn3 = types.KeyboardButton('😹')
  markup.add(btn1, btn2, btn3)
  return markup

@bot.message_handler(commands=['start'])
def startBot(message):
  user = save_new_user(message.from_user, message.chat.id)[0]
  if not user_has_rights(message): return
  print(get_formated_date(time.localtime()))
  first_mess = f"<b>{message.from_user.first_name} </b>, привет!\nЭтот бот мониторит цены на определенные товары Яндекс.Маркета"
  bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=get_alt_menu())
  menu = get_menu(user)
  bot.send_message(message.chat.id, 'Выбери нужный пункт:', reply_markup=menu)
  # bot.send_message(message.chat.id, reply_markup=get_alt_menu())
  # bot.send_message(message.chat.id, reply_markup=types.ReplyKeyboardRemove(selective=True))

@bot.message_handler(commands=['run'])
def stopBot(message):
  if not user_has_rights(message): return
  subscribe(message.from_user, message.chat.id)
  bot.send_message(message.chat.id, 'Вы подписаны на рассылку!')

@bot.message_handler(commands=['stop'])
def stopBot(message):
  if not user_has_rights(message): return
  unsubscribe(message.from_user, message.chat.id)
  bot.send_message(message.chat.id, 'Бот больше не будет присылать вам сообщения')

@bot.message_handler(content_types=['text'])
def handle_message(message):
  print(message.text)
  if (message.text == '😹'):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKCwhnNdFJ1vn16N53-9gImKbXzoF-mgACSgADKA9qFNx0AAFHSNP1gjYE')
  elif (message.text == '😻'):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKCw5nNdHhAo04g-mhJMtKIuqv0KZ7rwAC6AoAAu6g8Ui8gw9lugYjxTYE')
  elif (message.text == '😸'):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKCxJnNdH-fSaVKdD6k4o7Da6njX7szQACIgADKA9qFBEx-ROlx0RXNgQ')
  else:
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKCzRnNdYLmQclGprAqJoCSeYNwRWRwgACY0kAAjfbeUsYskP-GAru1TYE')

@bot.message_handler(content_types=['sticker'])
def handle_message(message):
  bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKCzRnNdYLmQclGprAqJoCSeYNwRWRwgACY0kAAjfbeUsYskP-GAru1TYE')

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if not user_has_rights(function_call): return
  if function_call.message:
    message = bot.send_message(function_call.message.chat.id, text="секундочьку!..")
    if function_call.data == "change":
      # second_mess = "Тогда начинаю! Сообщу тебе, когда цена изменится. 
      # А пока можешь перейти на страницу мониторинга по ссылке."
      # markup = types.InlineKeyboardMarkup()
      # markup.add(types.InlineKeyboardButton("Перейти на сайт", url=url))
      # bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
      # bot.answer_callback_query(function_call.id)
      monitoring(function_call.message.chat.id, True)
    elif function_call.data == "info":
      monitoring(function_call.message.chat.id, False)
    elif function_call.data == "discount":
      # discount_input = bot.send_message(message.chat.id, 'Отправтье скидку (число) в процентах')
      # bot.reply_to(function_call.message, 'Отправтье скидку (число) в процентах')
      bot.send_message(function_call.message.chat.id, 'Отправтье скидку (число) в процентах')
      bot.register_next_step_handler(function_call.message, set_new_discount)
      # print(discount_input)
    elif function_call.data == "on":
      subscribe(function_call.from_user, function_call.message.chat.id)
      repaint_menu(function_call)
    elif function_call.data == "off":
      unsubscribe(function_call.from_user, function_call.message.chat.id)
      repaint_menu(function_call)
    bot.delete_message(message.chat.id, message.message_id)
    bot.answer_callback_query(function_call.id)

def repaint_menu(function_call):
    user = get_user_data(function_call.from_user.id)
    markup = get_menu(user)
    bot.edit_message_reply_markup(function_call.message.chat.id, function_call.message.id, reply_markup=markup)

# def delete_message(chat_id, message_id):
#     return bot.delete_message(chat_id, message_id)

def set_new_discount(message):
  # print(message)
  discount = message.text 
  if not discount.isdigit(): 
    message = bot.send_message(message.chat.id,'Скидка должна быть числом..\n Введите корректную скидку')             
    bot.register_next_step_handler(message, set_new_discount) 
    return
  edit_user_data(message.from_user, message.chat.id, [('discount', int(discount))])
  # bot.reply_to(message, 'Данные успешно обновлены')
  bot.reply_to(message, 'Данные успешно обновлены')
  return
  

def get_result_text(res, user):
  text = ''
  discount = user['discount'] 
  discount = 1-discount/100
  for item in res["data"]: 
    if item["old_price"] is None:
      text += f'{"ПОЯВИЛОСЬ: "} {str(item["new_price"]*discount)} - {str(item["size"])} - {item["url"]}\n'
    else:
      resolution = 'ПОДЕШЕВЕЛО: ' if item["old_price"] > item["new_price"] else 'Подорожало: '
      text += f'{resolution}{str(item["old_price"]*discount)} -> {str(item["new_price"]*discount)} - {str(item["size"])} - {item["url"]}\n'
  return text

def monitoring(chat_id, flag):
    try:
      products_data = test(flag)
      if flag:
        text = ''
        # text = f'Предыдущий просмотр: {products_data["last_update_alt"]} ({get_duration(time.time() - products_data["last_update"])} назад)\n\n'
        if len(products_data["data"]) == 0:
          text += 'Цены не менялись с предыдущего просмотра'
        else:
          text += get_result_text(products_data)
        bot.send_message(chat_id, text=text)
      else:
        if len(products_data) == 0:
          text = 'Товаров нет в наличии'
        else:
          text = 'Доступно сейчас:\n\n'
          for item in products_data: 
              user = get_user_data(chat_id)
              discount = user['discount'] | 0
              discount = 1-discount/100
              text += f'{str(item["size"])} - {str(item["price"]*discount)} - {item["url"]}\n'
        bot.send_message(chat_id, text=text)
    except Exception as err:
      bot.send_message(chat_id, text="Что-то пошло не так ;(")
      print(f"Unexpected {err=}, {type(err)=}")

def send_new_price_for_all(products_data):
  users_data_base = None
  try:
    with open('db/users_data.txt', "r", encoding='utf-8') as file_data:
      users_data_base = file_data.read()
      users_data_base = json.loads(users_data_base)
      users_data_base = users_data_base.get('data')
  except Exception as err:
    print('ERROR WITH READING USERS_DATA FILE', err)
    return

  if users_data_base:
    for user in users_data_base:
      if user['activate']: 
        text = get_result_text(products_data, user)
        bot.send_message(user['chat_id'], text)
  else:
    print('NO USERS DATA')
  
def start_auto_monitoring():
  print('START AUTO MONITORING')
  while True:
    try:
      products_data = test(True)
      if len(products_data["data"]) == 0:
        pass
      else:
        # text = get_result_text(products_data)
        send_new_price_for_all(products_data)
    except Exception as ex:
      print('auto monitoring failed', ex)
    time.sleep(30)

def save_new_user(new_user_data, chat_id): # -> (object, bool)
  users_data_base = get_users_data_base()
  users_data = users_data_base.get('data') if users_data_base else []
  user_data = get_user_data(new_user_data.id, users_data_base) if users_data_base else None

  if user_data:
    # print("USER ALREADY EXISTS")
    return (user_data, False)
  else:
    print("SAVE NEW USER. id = ", new_user_data.id)
    user_data = {
      'id': new_user_data.id,
      'chat_id': chat_id,
      'activate': False,
      'discount': 0,
      'registration_date': time.localtime(),
      'last_update': time.localtime(),
  }
    users_data.append(user_data)
    res = {
      'last_update': time.localtime(),
      'data': users_data
    }
      
    with open('db/users_data.txt', "w+", encoding='utf-8') as file_data:
      json.dump(res, file_data)

    return (user_data, True) 

def get_users_data_base():
  try:
    with open('db/users_data.txt', "r", encoding='utf-8') as file_data:
      users_data_base = file_data.read()
      users_data_base = json.loads(users_data_base)
      return users_data_base if users_data_base else None
  except Exception as err:
    print('ERROR WITH READING USERS_DATA FILE', err)
    return None

def get_user_data(user_id, users_data_base=None):
  users_data_base = users_data_base if users_data_base else get_users_data_base()
  if users_data_base:
    users_data_base = users_data_base.get('data')
    user_data = [x for x in users_data_base if x["id"] == user_id]
    return user_data[0] if len(user_data) > 0 else None
  else: return None

def edit_user_data(user, chat_id, new_params):
  # print(user)
  users_data_base = get_users_data_base()
  user_data = get_user_data(user.id, users_data_base)
  users_data = users_data_base.get('data')
  
  if user_data is None:
    new_user_data = save_new_user(user, chat_id)
    user_data = new_user_data[0]
    users_data.append(user_data)

  for param in new_params:
    user_data[param[0]] = param[1]
  
  res = {
    'last_update': time.localtime(),
    'last_update_alt': get_formated_date(time.localtime()),
    'data': users_data
  }
    
  with open('db/users_data.txt', "w+", encoding='utf-8') as file_data:
    json.dump(res, file_data)

def subscribe(user, chat_id):
  edit_user_data(user, chat_id, [('activate', True)])

def unsubscribe(user, chat_id):
  edit_user_data(user, chat_id, [('activate', False)])

# import multiprocessing

# process1 = multiprocessing.Process(target=start_monitoring)
# process2 = multiprocessing.Process(target=bot.infinity_polling)

# process1.start()
# process2.start()
# process1.join()
# process2.join()

import threading

thread1 = threading.Thread(target=start_auto_monitoring)
thread2 = threading.Thread(target=bot.infinity_polling)
thread1.start()
thread2.start()
thread1.join()
thread2.join()





