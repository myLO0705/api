import logging
import sys
import asyncio

import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Filters import qilinadi

# Instaloader media olish funksiyasi
def download_instagram_media(url):
    L = instaloader.Instaloader()

    # Extract the shortcode (unique ID for the post)
    shortcode = url.split('/')[-2]  # Getting shortcode from URL

    try:
        # Fetch media information
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Check if the post is a video
        if post.is_video:
            media_url = post.video_url
            media_type = 'video'
        else:
            media_url = post.url
            media_type = 'image'

        # Return the media information
        return {'type': media_type, 'url': media_url}

    except Exception as e:
        return {'error': str(e)}

# Telegram botning start komandi
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Salom! Instagram postining linkini yuboring.')

# Instagram linkini qayta ishlash va media yuborish
async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text  # Foydalanuvchidan linkni olish
    result = download_instagram_media(url)

    if 'error' in result:
        await update.message.reply_text("Bu bot faqat Instagram video va rasm yuklab bera oladi")
    else:
        if result['type'] == 'image':
            # Rasm bo'lsa
            await update.message.reply_photo(result['url'])
        elif result['type'] == 'video':
            # Video bo'lsa
            await update.message.reply_video(result['url'])

# Botni ishga tushirish
def main():
    # Telegram bot tokenini kiritish
    token = "7017043784:AAGXrehVp5qW14Ld3NSyHHydsMgys87qDqc"

    # Application yaratish (v20 va yuqori versiya uchun)
    application = Application.builder().token(token).build()

    # Handlerlar: /start komandi va linkni tekshirish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushurish
    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
    asyncio.run(main())
