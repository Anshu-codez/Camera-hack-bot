import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext
import cv2

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Use /camera to get a snapshot from the camera.')

def camera(update: Update, context: CallbackContext) -> None:
    """Capture and send a camera snapshot."""
    # Open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        update.message.reply_text('Error: Could not open camera.')
        return

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        update.message.reply_text('Error: Could not capture image.')
        return

    # Save the frame as a JPEG file
    cv2.imwrite('camera_snapshot.jpg', frame)

    # Send the image to the user
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('camera_snapshot.jpg', 'rb'))

    # Release the camera
    cap.release()

def main() -> None:
    """Start the bot."""
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot's token
    updater = Updater("7916798453:AAFQWfmyJvNb625sbbDjgLbLtEpmsmuh7Xg", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("camera", camera))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
