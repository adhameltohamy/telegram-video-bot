import yt_dlp
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8744352264:AAHHWUHRn2ECwbGP8mAzcpuTieEa-dw-C9o"

async def download(update, context):
url = update.message.text
await update.message.reply_text("جاري تحميل الفيديو...")

```
ydl_opts = {
    "format": "best",
    "outtmpl": "video.mp4"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

await update.message.reply_video(video=open("video.mp4","rb"))

os.remove("video.mp4")
```

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, download))

print("Bot is running...")

app.run_polling()
