import logging

from pyrogram import Client, filters

import config
from parseHome import ParseHomeSSGE

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Создайте сессию Pyrogram
api_id = config.API_ID
api_hash = config.API_HASH

app = Client("MyBot", api_id=api_id, api_hash=api_hash)


# Обработчик текстовых сообщений
@app.on_message(filters.text & filters.private)
def handle_text_message(client, message):
    parse_home: ParseHomeSSGE = None

    if message.text.lower() == "аренда":
        # Логируем полученное сообщение
        logging.info(f"Received rent home: {message.text}")

        # Парсим сообщение
        parse_home = ParseHomeSSGE()
        parse_home.get_source_code(ParseHomeSSGE.RENT_URI)

    elif message.text.lower() == "продажа":
        # Логируем полученное сообщение
        logging.info(f"Received sale home: {message.text}")

        # Парсим сообщение
        parse_home = ParseHomeSSGE()
        parse_home.get_source_code(ParseHomeSSGE.SALE_URI)

    elif message.text.lower() == "посуточно":
        # Логируем полученное сообщение
        logging.info(f"Received parse home: {message.text}")

        # Парсим сообщение
        parse_home = ParseHomeSSGE()
        parse_home.get_source_code(ParseHomeSSGE.DAY_RENT_URI)

    # Отправляем обратно тоже самое сообшеение
    if parse_home and parse_home.data:
        print(parse_home.data)
        message.reply_text(f"{message.chat.id}\n\n{get_str_from_data(parse_home.data, ', ')}", message.text)
    else:
        message.reply_text(f"{message.chat.id}\n\nНе удалось спарсить данные", message.text)


def get_str_from_data(data: list, sep: str = ' | ') -> str:
    return "\n\n".join([sep.join([d["date"], d.get("title", ''), d["address"], d.get("price", ''), d["area"],
                                  d.get("price_per_metr", '') ]).rstrip(sep) for d in data])


def main():
    app.run()


if __name__ == "__main__":
    main()
