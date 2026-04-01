import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr

API_ID = int(input("38875864: "))
API_HASH = input("ca89d648b16d7dbb66ab93b82653e61b: ")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH)

autoresponder = {"status": False, "text": ""}

# 🎤 Голос → текст (.gs)
@app.on_message(filters.command("gs", ".") & filters.reply)
async def voice_to_text(_, message: Message):
    if not message.reply_to_message.voice:
        return await message.edit("❌ Ответь на голосовое")
    file = await message.reply_to_message.download()
    audio = AudioSegment.from_file(file)
    audio.export("voice.wav", format="wav")

    r = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="ru-RU")
        except:
            text = "Не удалось распознать"

    await message.edit(f"🧠 {text}")

# 🔊 Текст → голос (.voice текст boys/girl)
@app.on_message(filters.command("voice", "."))
async def voice(_, message: Message):
    try:
        args = message.text.split(" ", 2)
        text = args[1]
        gender = args[2]
    except:
        return await message.edit(".voice текст boys/girl")

    tts = gTTS(text, lang="ru")
    tts.save("voice.mp3")
    sound = AudioSegment.from_mp3("voice.mp3")

    if gender == "boys":
        sound = sound.speedup(playback_speed=1.2)
    elif gender == "girl":
        sound = sound.speedup(playback_speed=1.5)

    sound.export("out.ogg", format="ogg")
    await message.reply_voice("out.ogg")
    await message.delete()

# 🤖 Автоответчик
@app.on_message(filters.command("autoresponder", "."))
async def auto(_, message: Message):
    global autoresponder
    if "on" in message.text:
        text = message.text.split("on", 1)[1].strip()
        autoresponder["status"] = True
        autoresponder["text"] = text
        await message.edit("✅ Автоответ включён")
    elif "off" in message.text:
        autoresponder["status"] = False
        await message.edit("❌ Автоответ выключен")

@app.on_message(filters.text & ~filters.me)
async def auto_reply(_, message: Message):
    if autoresponder["status"]:
        await message.reply(autoresponder["text"])

# 🧠 Джарвис
@app.on_message(filters.text & filters.me)
async def jarvis(_, message: Message):
    if message.text.lower().startswith("джарвис"):
        query = message.text.replace("джарвис", "").strip()

        try:
            result = eval(query)
            return await message.reply(f"{query} будет {result}")
        except:
            pass

        if "привет" in query:
            return await message.reply("Здравствуйте, сэр.")

        await message.reply("Я пока не знаю ответа, сэр.")

print("Юзербот запущен...")
app.run()
