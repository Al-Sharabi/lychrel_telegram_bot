import telebot
import os
from dotenv import load_dotenv
from palindrome import palindrome
import re
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
welcome_message = "Hi, send me a natural number and I will tell you if it is a lychrel number or give you it's palindrome number that comes through the iterative process of repeatedly reversing its digits and adding the resulting numbers"




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, welcome_message)

@bot.message_handler(func= lambda msg: msg.text.isdigit())
def send_result(message):
    num_message = message.text
    result = palindrome(int(num_message))
    if result['solvable'] == True:
        #send if solvable
        bot.reply_to(message=message,
        text=result['text'],
        parse_mode='MarkdownV2')


    else:
        
        steps_button = telebot.types.InlineKeyboardButton('See all of the steps', callback_data="steps")
        long_num_button = telebot.types.InlineKeyboardButton('See the reached number in step 300', callback_data="num")
        result_markup = telebot.types.InlineKeyboardMarkup([[steps_button],[long_num_button]])
        
        bot.reply_to(message=message,
        text=f"``` The number {num_message} is probably a lychrel number. ```",
        parse_mode='MarkdownV2',
        reply_markup=result_markup)


@bot.callback_query_handler(func= lambda callback: callback.data in ['steps', 'num', 'back'])
def lychrel_callback_handler(callback):
    msg_id = callback.message.message_id
    msg_chat_id = callback.message.chat.id
    msg_text = callback.message.text
    num_ber = re.findall('\d+', msg_text)[0]
    result = palindrome(int(num_ber))
    back_button = telebot.types.InlineKeyboardButton(text='Back', callback_data='back')
    back_markup = telebot.types.InlineKeyboardMarkup([[back_button]]) 
    
    
    
    #buttons from previous message
    steps_button = telebot.types.InlineKeyboardButton('See all of the steps', callback_data="steps")
    long_num_button = telebot.types.InlineKeyboardButton('See the reached number in step 300', callback_data="num")
    result_markup = telebot.types.InlineKeyboardMarkup([[steps_button],[long_num_button]])
    #####


    if callback.data == 'num':
        bot.edit_message_text(text=f"The number that was reached for {num_ber}:\n ``` {result['reached_num']} ```",
        message_id=msg_id,
        chat_id=msg_chat_id,
        parse_mode='MarkdownV2',
        reply_markup=back_markup)
    if callback.data == 'steps':
        bot.edit_message_text(text=f"{result['text']}",
        message_id=msg_id,
        chat_id=msg_chat_id,
        parse_mode='MarkdownV2',
        reply_markup=back_markup)
    if callback.data == 'back':
        bot.edit_message_text(
        text=f"``` The number {num_ber} is probably a lychrel number. ```",
        message_id=msg_id,
        chat_id=msg_chat_id,
        parse_mode='MarkdownV2',
        reply_markup=result_markup)
    

bot.infinity_polling()