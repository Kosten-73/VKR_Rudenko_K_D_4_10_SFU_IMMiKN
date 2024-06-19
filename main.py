import telebot, subprocess
from telebot.types import Message
from googletrans import Translator
from telebot import types
import time


with open('token.txt', 'r') as file:
    token = file.read()


bot = telebot.TeleBot(token)


def trans_later(eng_text):
    translator = Translator()
    tr = translator.translate(eng_text, dest="ru")
    return tr.text


def analiz(src1):
    return (subprocess.run(
        f"pmd.bat check -d {src1} -R rulesets/java/quickstart.xml -f text",
        shell=True, capture_output=True, text=True, encoding='cp866').stdout)


def analiz_itog(message):
    with open('file.java', 'w', encoding='utf-8') as file:
        file.write(message.text)
    analizator_text = analiz() + '\n'
    analizator_text += "Перевод на русский язык:" + '\n' + trans_later(analizator_text)
    bot.reply_to(message, analizator_text)


def print_file(f_name):
    with open(f_name, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Методы рефакторинга")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот который разбирается в java, могу рассказать о методах рефакторинга \n \n"
                          "Если хочешь чтобы я проанализировал твой код то просто пришли мне его текстом скопировав его из своего редактора или пришли мне файл".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['document'])
def get_text_messages(message: Message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if message.document.file_name[-5:] == '.java':
        # src = f"file_{int(time.time())}.java"
        src = f"{message.document.file_name}"
        # src = f'C:/Users/korudenko/PycharmProjects/telegram_bot/{unique_filename}'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        analizator_text = analiz(src) + '\n'
        analizator_text += "Перевод на русский язык:" + '\n' + trans_later(analizator_text)
        if len(analizator_text) > 4096:
            name_file2 = message.document.file_name[:-5] + "_анализ.txt"
            with open(name_file2, 'w', encoding='utf-8') as new_file1:
                new_file1.write(analizator_text)
            with open(name_file2, 'rb') as file3:
                bot.send_document(message.chat.id, file3, caption='Ответ '
                  'анализа вашего файла больше 4096 символом, поэтому отправляю Вам файл с даннными')
        else:
            bot.reply_to(message, "Имя проанализированного файла: " + message.document.file_name + '\n' + '\n' + analizator_text)
    else:
        bot.reply_to(message, "Файл не проанализирован, я понимаю только файлы на ЯП java")


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def get_text_messeges(message: Message):
    if (message.text == "Методы рефакторинга") or (message.text == "🔙 Назад к методом рефакторинга"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выделение метода")
        btn2 = types.KeyboardButton("Выделение класса")
        btn3 = types.KeyboardButton("Объединение условных выражений")
        btn4 = types.KeyboardButton("Передача всего объекта")
        back = types.KeyboardButton("🔙 Назад в основное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="О каком методе {0.first_name} хочет узнать?".format(message.from_user),
                         reply_markup=markup)
    elif (message.text == "Выделение метода"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        btn1 = types.KeyboardButton("Достоинства - выделение метода")
        btn2 = types.KeyboardButton("Порядок рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, btn5, back)
        str_out_false = print_file("method_selection_false.java")
        str_out = print_file("method_selection.java")
        bot.send_message(message.chat.id,
                         f"Выделение метода \\- это разделиние сложных методов на более мелкие, каждый из которых выполняет отдельную задачу\\. \n \n"
                         f"Пример с плохим кодом\\:"
                         f"```java\n{str_out_false}\n```"
                         f"Пример с правильным кодом\\:"
                         f"```java\n{str_out}\n```", parse_mode='MarkdownV2', reply_markup=markup)
    elif (message.text == "Порядок рефакторинга - выделение метода"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Порядок рефакторинга\\: \n"
                                          f"1\\) Создайте новый метод и назовите его так, чтобы название отражало суть того, что будет делать этот метод\\. \n \n"
                                          f"2\\) Скопируйте беспокоящий вас фрагмент кода в новый метод\\. Удалите этот фрагмент из старого места и замените вызовом вашего нового метода\\. \n"
                                          f"Найдите все переменные, которые использовались в этом фрагменте кода\\. Если они были объявлены внутри этого фрагмента и не используются вне его, просто оставьте их без изменений \\- они станут локальными переменными нового метода\\. \n \n"
                                          f"3\\) Если переменные объявлены перед интересующим вас участком кода, значит, их следует передать в параметры вашего нового метода, чтобы использовать значения, которые в них находились ранее\\. Иногда от таких переменных проще избавиться с помощью замены переменных вызовом метода\\. \n \n"
                                          f"4\\) Если вы видите, что локальная переменная как\\-то изменяется в вашем участке кода, это может означать, что её изменённое значение понадобится дальше в основном методе\\. Проверьте это\\. Если подозрение подтвердилось, значение этой переменной следует возвратить в основной метод, чтобы ничего не сломать\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга - выделение метода"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - выделение метода")
        btn2 = types.KeyboardButton("Порядок рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Причины рефакторинга\\: \n"
                                          f"Чем больше строк кода в методе, тем сложнее разобраться в том, что он делает\\. Это основная проблема, которую решает этот рефакторинг\\. \n \n"
                                          f"Извлечение метода не только убивает множество запашков в коде, но и является одним из этапов множества других рефакторингов\\. \n",
                         parse_mode='MarkdownV2', reply_markup=markup)


    elif (message.text == "Достоинства - выделение метода"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга - выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
                                          f"1\\) Улучшает читабельность кода\\. Постарайтесь дать новому методу название, которое бы отражало суть того, что он делает\\. Например, createOrder\\(\\), renderCustomerInfo\\(\\) и т\\. д\\. \n"
                                          f"2\\) Убирает дублирование кода\\. Иногда код, вынесенный в метод, можно найти и в других местах программы\\. В таком случае, имеет смысл заменить найденные участки кода вызовом вашего нового метода\\. \n"
                                          f"3\\) Изолирует независимые части кода, уменьшая вероятность ошибок \\(например, по вине переопределения не той переменной\\)\\. \n \n ",
                         parse_mode='MarkdownV2', reply_markup=markup)
    elif (message.text == "🔙 Назад в основное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Методы рефакторинга")
        btn2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="{0.first_name} сново в основном меню! Напоминаю я бот который разбирается в java, могу рассказать о методах рефакторинга".format(
                             message.from_user), reply_markup=markup)

    elif (message.text == "Выделение класса"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = types.KeyboardButton("Причины рефакторинга - выделение класса")
        btn1 = types.KeyboardButton("Достоинства и недостатки - выделение класса")
        btn2 = types.KeyboardButton("Порядок рефакторинга - выделение класса")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, btn5, back)
        photo_false = open('Class_Extraction_False.jpg', 'rb')
        photo = open('Class_Extraction.jpg', 'rb')
        bot.send_message(message.chat.id,
                         f"Выделение класса \\(Class Extraction\\) \\- это процесс рефакторинга кода, в ходе которого часть функциональности или данных из одного класса выносится в отдельный класс\\. "
                         f"Это делается для того, чтобы каждый класс имел четко определенную ответственность и был легче понять, использовать и поддерживать\\. \n \n"
                         f"Пример с неправильной реализацией\\:", parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo_false)
        bot.send_message(message.chat.id,
                         f"Пример с правильной реализацией\\:", parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo)

    elif (message.text == "Порядок рефакторинга - выделение класса"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Порядок рефакторинга\\: \n"
                                          f"Перед началом рефакторинга обязательно определите, как именно следует разделить обязанности класса\\."
                                          f"1\\) Создайте новый класс, который будет содержать выделенную функциональность\\. \n \n"
                                          f"2\\) Создайте связь между старым и новым классом\\. Лучше всего, если эта связь будет односторонней\\; при этом второй класс можно будет без проблем использовать повторно\\. С другой стороны\\, если вы считаете\\, что это необходимо\\, всегда можно создать двустороннюю связь\\. \n"
                                          f"3\\) Используйте перемещение поля и перемещение метода для каждого поля и метода, которые вы решили переместить в новый класс\\. Для методов имеет смысл начинать с приватных\\, таким образом вы снижаете вероятность допустить массу ошибок\\. Старайтесь двигаться понемногу и тестировать результат после каждого перемещения\\, это избавит вас от необходимости исправлять большое число ошибок в самом конце\\. \n \n"
                                          f"После того как с перемещением покончено\\, пересмотрите ещё раз на получившиеся классы\\. Возможно\\, старый класс теперь имеет смысл назвать по\\-другому ввиду его изменившихся обязанностей\\. Проверьте ещё раз\\, можно ли избавиться от двусторонней связи между классами\\, если она возникла\\."
                                          f"4\\) Ещё одним нюансом является доступность нового класса извне\\. Вы можете полностью спрятать его от клиента\\, сделав приватным\\, управляя при этом его полями из старого класса\\. Либо сделать его публичным\\, предоставив клиенту возможность напрямую менять значения\\. Решение зависит от того\\, насколько безопасны для поведения старого класса будут неожиданные прямые изменения значений в новом классе\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга - выделение класса"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - выделение метода")
        btn2 = types.KeyboardButton("Порядок рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Причины рефакторинга\\: \n"
                                          f"Классы всегда изначально выглядят чёткими и понятными\\. Они выполняют свою работу и не лезут в обязанности других классов\\. "
                                          f"Однако, с течением жизни программы добавляется один метод  \\- тут, одно поле  \\- там\\. В результате некоторые классы получают массу дополнительных обязанностей\\. \n \n",
                         parse_mode='MarkdownV2', reply_markup=markup)


    elif (message.text == "Достоинства и недостатки - выделение класса"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга - выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
                                          f"1\\) Этот рефакторинг призван помочь в соблюдении принципа единственной обязанности класса\\. Это делает код ваших классов очевиднее и понятнее\\. \n"
                                          f"2\\) Классы с единственной обязанностью более надёжны и устойчивы к изменениям\\. Например, у вас есть класс, отвечающий за десять разных вещей\\. И когда вам придётся вносить в него изменения, вы рискуете при корректировках одной вещи сломать другие\\. \n\n"
                                          f"Недостатки\\: \n"
                                          f"1\\) Если при проведении этого рефакторинга вы перестараетесь, придётся прибегнуть к встраиванию класса\\. \n",
                         parse_mode='MarkdownV2', reply_markup=markup)


    # Объединение условных выражений
    elif (message.text == "Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = types.KeyboardButton("Причины рефакторинга - Объединение условных выражений")
        btn1 = types.KeyboardButton("Достоинства - Объединение условных выражений")
        btn2 = types.KeyboardButton("Порядок рефакторинга - Объединение условных выражений")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, btn5, back)
        str_out_false1 = print_file("Consolidate_Conditional_Expression.java")
        str_out1 = print_file("Consolidate_Conditional_Expression_false.java")
        bot.send_message(message.chat.id,
                         f"Объединение условных операторов \\- это способ комбинировать несколько условий в одном выражении для более сложной логики управления потоком программы\\."
                         f" В основном это происходит с использованием логических операторов\\. \n \n"
                         f"Пример с плохим кодом\\:"
                         f"```java\n{str_out1}\n```"
                         f"Пример с правильным кодом\\:"
                         f"```java\n{str_out_false1}\n```", parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга - Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга - Объединение условных выражений")
        btn2 = types.KeyboardButton("Достоинства - Объединение условных выражений")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Причины рефакторинга\\: \n"
                                          f"Код содержит множество чередующихся операторов, которые выполняют одинаковые действия\\. Причина разделения операторов неочевидна\\. \n \n"
                                          f"Главная цель объединения операторов — извлечь условие оператора  в отдельный метод или только в один условный оператор, упростив его понимание\\. \n",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Достоинства - Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга - Объединение условных выражений")
        btn2 = types.KeyboardButton("Причины рефакторинга - Объединение условных выражений")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn2, btn1, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
                                          f"1\\) Убирает дублирование управляющего кода\\. Объединение множества условных операторов, ведущих к одной цели, помогает показать, что на самом деле вы делаете только одну сложную проверку, ведущую к одному общему действию\\. \n"
                                          f"2\\) Объединив все операторы в одном, вы позволяете выделить это сложное условие в новый метод с названием, отражающим суть этого выражения\\. \n",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Порядок рефакторинга - Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - Объединение условных выражений")
        btn2 = types.KeyboardButton("Причины рефакторинга - Объединение условных выражений")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn2, btn1, back)
        bot.send_message(message.chat.id, f"Порядок рефакторинга\\: \n"
                                          f"Перед тем как осуществлять рефакторинг, убедитесь, что в условиях операторов нет «побочных эффектов», или, другими словами, они не модифицируют что\\-то, а только возвращают значения\\."
                                          f"Побочные эффекты могут быть и в коде, который выполняется внутри самого оператора\\. Например, по результатам условия, что\\-то добавляется к переменной\\."
                                          f"1\\) Объедините множество условий в одном с помощью операторов и и или\\. Объединение операторов обычно следует такому правилу\\: \n \n"
                                          f"\\-\\-\\-\\- Вложенные условия соединяются с помощью оператора и\\. \n"
                                          f"\\-\\-\\-\\- Условия, следующие друг за другом, соединяются с помощью оператора или\\. \n \n"
                                          f"4\\) Извлеките метод из условия оператора и назовите его так, чтобы он отражал суть проверяемого выражения\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Передача всего объекта"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = types.KeyboardButton("Причины рефакторинга - передача всего объекта")
        btn1 = types.KeyboardButton("Достоинства и недостатки - передача всего объекта")
        btn2 = types.KeyboardButton("Порядок рефакторинга - передача всего объекта")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, btn5, back)
        photo_false = open('Передача всего объекта не.jpg', 'rb')
        photo = open('Передача всего объекта да.jpg', 'rb')
        bot.send_message(message.chat.id,
                         f"Передача всего объекта \\(Pass an Entire Object\\) — это техника рефакторинга\\, "
                         f"при которой вместо передачи нескольких отдельных параметров в метод или"
                         f" функцию передаётся целый объект\\. \n \n"
                         f"Пример с неправильной реализацией\\:", parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo_false)
        bot.send_message(message.chat.id,
                         f"Пример с правильной реализацией\\:", parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo)

    elif (message.text == "Порядок рефакторинга - передача всего объекта"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - передача всего объекта")
        btn2 = types.KeyboardButton("Причины рефакторинга - передача всего объекта")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Порядок рефакторинга\\: \n"
                                          f"Перед началом рефакторинга обязательно определите, какие объекты передавать целиком\\. \n \n"
                                          f"1\\) Идентификация параметров: найдите методы\\, которые принимают множество связанных параметров\\. \n \n"
                                          f"2\\) Создание или использование существующего класса\\: создайте класс\\, который объединяет эти параметры в один объект\\, или используйте уже существующий класс\\. \n \n"
                                          f"3\\) Изменение сигнатуры метода\\: обновите сигнатуры методов\\, чтобы они принимали объект вместо множества параметров\\. \n \n"
                                          f"4\\) Обновление вызовов метода\\: измените все места\\, где вызывается этот метод\\, чтобы передавать объект вместо отдельных параметров\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга - передача всего объекта"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства - передача всего объекта")
        btn2 = types.KeyboardButton("Порядок рефакторинга - передача всего объекта")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Причины рефакторинга\\: \n"
                                          f"Сложные и длинные сигнатуры методов\\: уменьшение количества параметров делает методы более читаемыми и удобными в использовании\\. \n "
                                          f"Изменение требований\\: потребность в добавлении новых параметров в методы без изменения их сигнатур\\. \n \n",
                         parse_mode='MarkdownV2', reply_markup=markup)


    elif (message.text == "Достоинства и недостатки - передача всего объекта"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга - передача всего объекта")
        btn2 = types.KeyboardButton("Причины рефакторинга - передача всего объекта")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
                                          f"1\\) Упрощение кода: снижается количество параметров в методах\\, что делает код более читаемым и поддерживаемым\\. \n"
                                          f"2\\) Повышение гибкости\\: легче добавлять новые параметры в объект без необходимости изменять сигнатуры методов\\. \n\n"
                                          f"Недостатки\\: \n"
                                          f"1\\) Увеличение связности: может возникнуть чрезмерная зависимость между объектами\\, что усложняет изменение кода\\. \n"
                                          f"2\\) Повышенная сложность: введение новых классов или объектов может усложнить структуру кода и его понимание",
                         parse_mode='MarkdownV2', reply_markup=markup)

    else:
        analiz_itog(message)


bot.polling()
