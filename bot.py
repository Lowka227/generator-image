import telebot
from config import TOKEN
from logic import FusionBrainAPI, convert_base64_to_jpg, API_IMAGE, SECRET_IMAGE

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Отправь мне описание изображения, и я сгенерирую его для тебя.😉👍😊')

@bot.message_handler(func=lambda message: True)
def generate_image(message):
    prompt = message.text
    bot.send_message(message.chat.id, 'Начинаю генерацию изображения...🖼️')
    bot.send_chat_action(message.chat.id, 'upload_photo')

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_IMAGE, SECRET_IMAGE)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)
    if files:
        base64_image = files[0]  
        output_path = f'image_{message.chat.id}.jpg'  
        convert_base64_to_jpg(base64_image, output_path)
        with open(output_path, 'rb') as img_file:
            bot.send_photo(message.chat.id, img_file)
    else:
        bot.send_message(message.chat.id, 'Не удалось сгенерировать изображение. Попробуйте еще раз.😓😓😭')

if __name__ == '__main__':
    bot.polling(none_stop=True)
