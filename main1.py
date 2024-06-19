import subprocess
from googletrans import Translator

def run_pmd(file_path):
    result = subprocess.run(['pmd.bat', 'check', '-d', file_path, '-R', 'rulesets/java/quickstart.xml', '-f', 'text'], capture_output=True, text=True)
    return result.stdout

# def process_pmd_output(output):
#     # Парсинг вывода PMD и извлечение предупреждений и ошибок
#     # Например, можно разбить вывод на строки и обработать каждую строку, чтобы извлечь нужную информацию
#
# def send_message_to_user(message):
#     # Отправка сообщения обратно пользователю через телеграм-бота
#     # Используйте библиотеку python-telegram-bot для отправки сообщений

if __name__ == "__main__":
    # file_path = "C:/Users/korudenko/PycharmProjects/telegram_bot/file.java"
    # print(file_path)
    # with open('C:/Users/korudenko/PycharmProjects/telegram_bot/file.java', 'r', encoding='utf-8') as file:
    #     output = run_pmd(file)
    # print(subprocess.run("pmd.bat check -d C:/Users/korudenko/PycharmProjects/telegram_bot/file.java -R rulesets/java/quickstart.xml -f text", shell=True, capture_output=True, text=True, encoding='cp866').stdout)

    translator = Translator()
    english_text = "Your English text here."
    translation = translator.translate(text=english_text, src='en', dest='ru')
    print(translation.text)