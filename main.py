import os
import requests
import telegram
import random
import shutil
from dotenv import load_dotenv


def get_comics(random_number):
    comics_url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(comics_url)
    response.raise_for_status()
    comics_url = response.json()['img']
    comics_comment = response.json()['alt']
    return comics_url, comics_comment


def save_comics(comics_url, folder_name, random_number):
    comics = requests.get(comics_url)
    comics.raise_for_status()
    with open(f'{folder_name}/comics{random_number}.png', 'wb') as file:
        file.write(comics.content)


def publish_photos(bot, chat_id, folder_name, text_post, random_number):
    with open(f'{folder_name}/comics{random_number}.png', 'rb') as document:
        bot.send_document(chat_id=chat_id, document=document, caption=text_post)

def main():
    load_dotenv()
    folder_name = 'images'
    bot_token = os.environ['TELEGRAM_BOT_ID']
    chat_id = os.environ['CHAT_ID_TELEGRAM']
    random_number = random.randint(1,2700)
    bot = telegram.Bot(bot_token)
    
    try:
        os.makedirs(folder_name, mode=0o777, exist_ok=True)
        comics_url, text_post = get_comics(random_number)
        save_comics(comics_url, folder_name, random_number)
        publish_photos(bot, chat_id, folder_name, text_post, random_number)
    finally:
        shutil.rmtree(folder_name)


if __name__ == '__main__':
    main()