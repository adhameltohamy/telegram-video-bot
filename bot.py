import yt_dlp
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, CommandHandler, filters, ContextTypes

TOKEN = "8744352264:AAGEWNK6AcrKKatWFnPhtACY2x070buKklM"

links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 اهلا بك في بوت تحميل الفيديو\n\n"
        "ارسل رابط الفيديو وسيظهر لك خيارات التحميل"
    )

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("❌ ارسل رابط صحيح")
        return

    links[update.message.chat_id] = url

    keyboard = [
        [
            InlineKeyboardButton("🎬 فيديو 360p", callback_data="360"),
            InlineKeyboardButton("🎬 فيديو 720p", callback_data="720")
        ],
        [
            InlineKeyboardButton("🎵 صوت MP3", callback_data="audio")
        ]
    ]

    await update.message.reply_text(
        "اختر نوع التحميل",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    url = links.get(query.message.chat_id)

    if not url:
        await query.message.reply_text("ارسل الرابط مرة اخرى")
        return

    if query.data == "360":

        await query.message.reply_text("⏳ جاري تحميل الفيديو 360p")

        ydl_opts = {
            "format": "best[height<=360]",
            "outtmpl": "video.mp4"
        }

    elif query.data == "720":

        await query.message.reply_text("⏳ جاري تحميل الفيديو 720p")

        ydl_opts = {
            "format": "best[height<=720]",
            "outtmpl": "video.mp4"
        }

    elif query.data == "audio":

        await query.message.reply_text("⏳ جاري استخراج الصوت")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await query.message.reply_audio(audio=open("audio.mp3","rb"))

        os.remove("audio.mp3")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await query.message.reply_video(video=open("video.mp4","rb"))

    os.remove("video.mp4")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_link))
app.add_handler(CallbackQueryHandler(buttons))

print("🚀 BOT RUNNING")

app.run_polling()
