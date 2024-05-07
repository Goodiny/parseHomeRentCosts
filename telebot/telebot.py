import logging
from pyrogram import Client, filters
from parseHome import ParseHome

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

    # Парсим сообщение
    parse_home = ParseHome()
    parse_home.get_source_code()
    print(parse_home.data)
    client.send_message(message.chat.id, "\n\n".join([", ".join([data["date"], data["title"], data["price"], data["area"]])
                                                    for data in parse_home.data]))

    # with open('source_code.txt', 'r') as sc:
    #     text = sc.read()
    #     data = []
    #     data_item = {}
    #     for i, line in enumerate(text.split('\n')):
    #         if 'm²' in line:
    #             data_item['square'] = line
    #         if '$' in line:
    #             data_item['price'] = line
    #         if '2024' in line or 'час назад' in line:
    #             data.append(data_item) if data_item else None
    #             data_item = {}
    #             data_item['date'] = line
    #     print(parse_home.data)
    #     client.send_message(message.chat.id, text)

    # Отправляем обратно тоже самоее сообшеение
    message.reply_text(message.chat.id, message.text)


def main():
    app.run()


if __name__ == "__main__":
    main()
