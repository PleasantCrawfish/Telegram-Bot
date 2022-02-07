import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from reply_generator import classify_question
from questions import bitrix_start, news, tasks, new_bitrix24, chat, groups

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"""Здравствуйте, {first_name}, у нас уже есть ответы на 95% вопросов по «Битрикс24». Посмотрите, возможно здесь есть то, что вы ищете.

Вы можете использовать следующие команды:
*/help - для получения помощи*
*/topics - для просмотра всех доступных вопросов*

Или же сразу написать сюда интересующий вас вопрос.""",
        parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
    update.message.reply_text('Вы можете задать мне любой вопрос касательно Битрикс24. Если я не смогу дать вам ответ, '
                              'то вы можете связаться с оператором. Я уверен, он вам поможет!',
                              parse_mode=telegram.ParseMode.MARKDOWN)


def topics(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Новое в Битрикс24', callback_data='1'),
            InlineKeyboardButton('С чего начать?', callback_data='2'),
        ],
        [
            InlineKeyboardButton('Лента Новостей', callback_data='3'),
            InlineKeyboardButton('Задачи и проекты', callback_data='4'),
        ],
        [
            InlineKeyboardButton('Чат и звонки', callback_data='5'),
            InlineKeyboardButton('Группы', callback_data='6'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите интересующую вас тему:', reply_markup=reply_markup)


def button(update, _):
    query = update.callback_query
    variant = query.data
    if variant == '1':
        text = 'В категории "Новое в Битрикс24" доступны следующие вопросы: \n\n'
        keys = new_bitrix24.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)
    elif variant == '2':
        text = 'В категории "С чего начать?" доступны следующие вопросы: \n\n'
        keys = bitrix_start.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)

    elif variant == '3':
        text = 'В категории "Лента Новостей" доступны следующие вопросы: \n\n'
        keys = news.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)

    elif variant == '4':
        text = 'В категории "Задачи и проекты" доступны следующие вопросы: \n\n'
        keys = tasks.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)

    elif variant == '5':
        text = 'В категории "Чат и звонки" доступны следующие вопросы: \n\n'
        keys = chat.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)

    elif variant == '6':
        text = 'В категории "Группы" доступны следующие вопросы: \n\n'
        keys = groups.keys()
        list_of_questions = []
        for key in keys:
            list_of_questions.append(key)
        for question in list_of_questions:
            text = text + f'-{question}\n'
        query.answer()
        query.edit_message_text(text=text)


def echo(update, context):
    answer = classify_question(update.message.text)
    update.message.reply_text(answer)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_answer():
    updater = Updater("TOKEN, use_context=True)
    dp = updater.dispatcher

    # реагирование на команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("topics", topics))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Логи
    dp.add_error_handler(error)

    # Старт бота
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    get_answer()
