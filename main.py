import os
import requests
import telegram
import random
import shutil
from dotenv import load_dotenv


def get_comic(random_number_comic):
    comics_url = f'https://xkcd.com/{random_number_comic}/info.0.json'
    response = requests.get(comics_url)
    response.raise_for_status()
    comics_url = response.json()['img']
    comics_comment = response.json()['alt']
    return comics_url, comics_comment


def save_comic(comics_url, folder_name, random_number_comic):
    comics = requests.get(comics_url)
    comics.raise_for_status()
    with open(f'{folder_name}/comics{random_number_comic}.png', 'wb') as file:
        file.write(comics.content)


def publish_comic(bot, chat_id, folder_name, text_post, random_number_comic):
    with open(f'{folder_name}/comics{random_number_comic}.png', 'rb') as document:
        bot.send_document(chat_id=chat_id, document=document, caption=text_post)

def main():
    load_dotenv()
    folder_name = 'images'
    bot_token = os.environ['TELEGRAM_BOT_ID']
    chat_id = os.environ['CHAT_ID_TELEGRAM']
    random_number_comic = random.randint(1,2700)
    bot = telegram.Bot(bot_token)
    
    try:
        os.makedirs(folder_name, mode=0o777, exist_ok=True)
        comics_url, text_post = get_comic(random_number_comic)
        save_comic(comics_url, folder_name, random_number_comic)
        publish_comic(bot, chat_id, folder_name, text_post, random_number_comic)
    finally:
        shutil.rmtree(folder_name)


if __name__ == '__main__':
    main()