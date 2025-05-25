from telethon import TelegramClient, events
from flask import Flask
import threading

# --- Flask сервер ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Multi-card bot is alive ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Telegram API credentials ---
api_id = 21656727
api_hash = '561e1c275ae2a89cc2b8670bb1a3a178'

client = TelegramClient('forwarder_session_allcards', api_id, api_hash)

# --- Настройки карт и чатов ---
CARD_TO_CHAT = {
    '***3804': -4691714145,  # в группу
    '***8628': -4720268824   # в другую группу
}

# Защита от повторов
handled_messages = set()

@client.on(events.NewMessage(from_users='CardXabarBot'))
async def handler(event):
    print("🔔 Получено новое сообщение от CardXabarBot!")

    text = event.raw_text.strip()
    print("📩 Текст сообщения:", repr(text))

    # Удаление невидимых символов
    cleaned_text = text.replace('\u202a', '').replace('\u200e', '').replace('*', '')
    message_hash = hash(cleaned_text)

    if message_hash in handled_messages:
        print("⏸ Повторное сообщение. Пропускаем.")
        return

    if '🟢 Perevod na kartu' not in cleaned_text:
        print("⏸ Нет ключевого слова. Пропускаем.")
        return

    for card_number, chat_id in CARD_TO_CHAT.items():
        if card_number.replace('*', '') in cleaned_text:
            print(f"✅ Найдена карта {card_number}. Отправляем в чат {chat_id}")
            handled_messages.add(message_hash)

            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                if any(key in line for key in ['🟢 Perevod na kartu', '➕', '💳']):
                    line = f"<b>{line}</b>"
                formatted_lines.append(line)

            formatted_text = "\n".join(formatted_lines)

            try:
                await client.send_message(chat_id, formatted_text, parse_mode='html')
                print("📤 Сообщение успешно отправлено.")
            except Exception as e:
                print("❌ Ошибка при отправке:", e)

            break

# --- Запуск ---
threading.Thread(target=run_flask).start()

client.start()
print("Userbot for 8628 & 3804 is running ✅")
client.run_until_disconnected()
