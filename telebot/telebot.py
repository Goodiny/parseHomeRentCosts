import logging

from pyrogram import Client, filters

import config
from parseHome import ParseHome

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Создайте сессию Pyrogram
api_id = config.API_ID
api_hash = config.API_HASH

app = Client("MyBot", api_id=api_id, api_hash=api_hash)


# Обработчик текстовых сообщений
@app.on_message(filters.text & filters.private)
def handle_text_message(client, message):
    if message.text.lower() == "спарсить аренду":
        # Логируем полученное сообщение
        logging.info(f"Received rent home: {message.text}")

        # Парсим сообщение
        parse_home = ParseHome()
        parse_home.get_source_code(ParseHome.RENT_URI)
        print(parse_home.data)

        client.send_message(message.chat.id, "\n\n".join([", ".join([data["date"], data["title"], data["price"],
                                                                     data["area"]]) for data in parse_home.data]))
    elif message.text.lower() == "спарсить продажу":
        # Логируем полученное сообщение
        logging.info(f"Received sale home: {message.text}")

        # Парсим сообщение
        parse_home = ParseHome()
        parse_home.get_source_code(ParseHome.SALE_URI)
        print(parse_home.data)

        client.send_message(message.chat.id, "\n\n".join([", ".join([data["date"], data["title"], data["price"],
                                                                     data["area"], data.get("price_per_metr", '')])
                                                          for data in parse_home.data]))

    # Отправляем обратно тоже самоее сообшеение
    message.reply_text(message.chat.id, message.text)


def main():
    app.run()


if __name__ == "__main__":
    main()
