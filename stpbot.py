import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Set your Telegram Bot API token here
TELEGRAM_TOKEN = '6197971351:AAFwt2SUnsoRHy2BYaw4DwayZnNjuAFutr0'
# Set your OpenAI API Key here
openai.api_key = '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'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. You can start typing and I will respond!')

def echo(update: Update, context: CallbackContext) -> None:
    # We use OpenAI's GPT-3 to generate a response
    user_input = update.message.text
    # Here we add our fixed instruction. This will depend on your use case.
    prompt = f"A user asks: '{user_input}'. Please give essay a score and feedback as if you are an Academic IELTS instructor:"

    # We make the API request to GPT-3
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)

    # We take the generated text and send it back to the user
    update.message.reply_text(response.choices[0].text.strip())

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    updater = Updater(token=TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
