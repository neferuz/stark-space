from telethon import TelegramClient, events
from flask import Flask
import threading

# --- Flask сервер для wake-up (cron ping) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot for *2589 is alive ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Telegram API credentials ---
api_id = 22748776
api_hash = '55151aab140082edf288767069a4f3de'

# Сохраняем сессию отдельно
client = TelegramClient('forwarder_session_2589', api_id, api_hash)

# Группа, куда отправляем
target_group_id = -4691714145

# Храним уже обработанные сообщения по хэшу текста
handled_messages = set()

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    text = event.raw_text.strip()
    message_hash = hash(text)

    if message_hash not in handled_messages and '🎉 Пополнение' in text and '💳 HUMOCARD *2589' in text:
        handled_messages.add(message_hash)

        # Выделяем жирным ключевые строки
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if '🎉 Пополнение' in line or '➕' in line:
                line = f"<b>{line}</b>"
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)
        custom_message = f"<b>Bar</b>\n{formatted_text}"

        await client.send_message(target_group_id, custom_message, parse_mode='html')

# --- Запускаем Flask + Telegram клиента ---
threading.Thread(target=run_flask).start()

client.start()
print("Userbot for *2589 is running ✅")
client.run_until_disconnected()
