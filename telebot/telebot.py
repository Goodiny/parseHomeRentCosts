import logging
from pyrogram import Client, filters

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Создайте сессию Pyrogram
api_id = "13041363"
api_hash = "f3d0238ae72f0e72c2693553d584fa70"

app = Client("MyBot", api_id=api_id, api_hash=api_hash)

# Обработчик текстовых сообщений
@app.on_message(filters.text & filters.private)
def handle_text_message(client, message):
    # Логируем полученное сообщение
    logging.info(f"Received message: {message.text}")

    # Отправляем обратно тоже самоее сообшеение
    message.reply_text(message.chat.id, message.text)


def main():
    app.run()


if __name__ == "__main__":
    main()