import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8744352264:AAGEWNK6AcrKKatWFnPhtACY2x070buKklM"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 اهلا بك\n\n"
        "ارسل رابط فيديو ليتم تحميله\n\n"
        "او استخدم:\n"
        "/audio رابط الفيديو لتحميل الصوت فقط"
    )


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, "rb"))

        os.remove(filename)

    except:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("❌ ارسل الرابط بعد الامر")
        return

    url = context.args[0]

    await update.message.reply_text("⏳ جاري تحميل الصوت...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_audio(audio=open("audio.mp3", "rb"))

        os.remove("audio.mp3")

    except:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, video))

print("🚀 BOT RUNNING")

app.run_polling()
