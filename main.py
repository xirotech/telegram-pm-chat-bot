import logging

from telegram.ext import Updater

from handlers import setup_dispatcher
from settings import CONFIG, setup_logging, save_data, save_preference, setup_commands


def setup_bot():
    updater = Updater(token=CONFIG['token'], use_context=True)
    dp = updater.dispatcher
    setup_dispatcher(dp)

    return updater


def main():
    # Set up logging
    setup_logging()

    # Set up bot
    updater = setup_bot()
    setup_commands()

    # Retrieve bot information
    me = updater.bot.get_me()
    CONFIG['id'] = me.id
    CONFIG['username'] = '@' + me.username

    # Start logging
    logging.info('Starting... (id: %s, username: %s)', CONFIG['id'], CONFIG['username'])

    # Start polling
    try:
        updater.start_polling()
        logging.info('Started')
        updater.idle()
    except Exception as e:
        logging.error('Exception occurred: %s', str(e))

    # Clean up and exit
    finally:
        save_data()
        logging.info('Data saved.')
        save_preference()
        logging.info('Stopped.')


if __name__ == '__main__':
    main()
