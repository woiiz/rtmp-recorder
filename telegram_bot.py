import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from subprocess import Popen, PIPE

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your bot token
BOT_TOKEN = os.getenv('7298524055:AAGo5RL3QQurgUOsXN6kHESAr7jSgs4KeX8')

# Process to handle recording
process = None

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Use /record <RTMP_URL> to start recording and /stop to stop recording.')

def record(update, context):
    """Start recording."""
    global process
    rtmp_url = context.args[0] if context.args else None
    if not rtmp_url:
        update.message.reply_text('Please provide an RTMP URL.')
        return

    if process and process.poll() is None:
        update.message.reply_text('Recording is already in progress.')
        return

    command = f'python recorder.py {rtmp_url}'
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    update.message.reply_text(f'Started recording {rtmp_url}')

def stop(update, context):
    """Stop recording."""
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        process = None
        update.message.reply_text('Stopped recording')
    else:
        update.message.reply_text('No recording in progress.')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("record", record))
    dp.add_handler(CommandHandler("stop", stop))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
