import telebot, subprocess
from telebot.types import Message
from googletrans import Translator
from telebot import types

token = '7172159834:AAHNKUv_v4Fjb12irpKvAuyipwtHn2B4AYw'

bot = telebot.TeleBot(token)


def trans_later(eng_text):
    translator = Translator()
    tr = translator.translate(eng_text, dest="ru")
    return tr.text


def analiz():
    return (subprocess.run(
        "pmd.bat check -d file.java -R rulesets/java/"
        "quickstart.xml -f text",
        shell=True, capture_output=True, text=True,
        encoding='cp866').stdout)


def analiz_itog(message):
    with open('file.java', 'w', encoding='utf-8') as file:
        file.write(message.text)
    analizator_text = analiz() + '\n'
    analizator_text += ("Перевод на русский язык:" + '\n' +
                        trans_later(analizator_text))
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
     text="Привет, {0.first_name}! Я бот который разбирается "
          "в java, могу рассказать о методах рефакторинга \n\n"
          "Если хочешь чтобы я проанализировал твой код то "
          "просто пришли мне его текстом скопировав его из "
          "своего редактора или пришли мне файл".format(
         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['document'])
def get_text_messages(message: Message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if message.document.file_name[-5:] == '.java':
        src = f"{message.document.file_name}"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        analizator_text = analiz(src) + '\n'
        analizator_text += ("Перевод на русский язык:" +
                    '\n' + trans_later(analizator_text))
        if len(analizator_text) > 4096:
            name_file2 = (message.document.file_name[:-5]
                        + "_анализ.txt")
            with open(name_file2, 'w',
                encoding='utf-8') as new_file1:
                new_file1.write(analizator_text)
            with open(name_file2, 'rb') as file3:
                bot.send_document(message.chat.id,
                        file3, caption='Ответ '
'анализа вашего файла больше 4096 символом,'
       ' поэтому отправляю Вам файл с даннными')
        else:
            bot.reply_to(message,
 "Имя проанализированного файла: "
+ message.document.file_name +
             '\n' + '\n' + analizator_text)
    else:
        bot.reply_to(message,
"Файл не проанализирован,"
" я понимаю только файлы на ЯП java")


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def get_text_messeges(message: Message):
    if ((message.text == "Методы рефакторинга") or
            (message.text == "🔙 Назад к методом рефакторинга")):
        markup = (types.ReplyKeyboardMarkup
                  (resize_keyboard=True))
        btn1 = types.KeyboardButton("Выделение метода")
        btn2 = types.KeyboardButton("Выделение класса")
        btn3 = types.KeyboardButton(""
                        "Объединение условных выражений")
        back = types.KeyboardButton("🔙 Назад в основное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id,
text="О каком методе {0.first_name} хочет узнать?".
     format(message.from_user),reply_markup=markup)
    elif (message.text == "Выделение метода"):
        markup = (types.ReplyKeyboardMarkup
                  (resize_keyboard=True))
        btn5 = (types.KeyboardButton
                ("Причины рефакторинга - выделение метода"))
        btn1 = (types.KeyboardButton
                ("Достоинства - выделение метода"))
        btn2 = (types.KeyboardButton
                ("Порядок рефакторинга - выделение метода"))
        back = (types.KeyboardButton
                ("🔙 Назад к методом рефакторинга"))
        markup.add(btn1, btn2, btn5, back)
        str_out_false = (print_file
                         ("method_selection_false.java"))
        str_out = print_file("method_selection.java")
        bot.send_message(message.chat.id,
f"Выделение метода \\- это разделиние сложных методов на"
f" более мелкие, каждый из которых выполняет отдельную задачу\\.\n\n"
 f"Пример с плохим кодом\\:"
 f"```java\n{str_out_false}\n```"
 f"Пример с правильным кодом\\:"
 f"```java\n{str_out}\n```", parse_mode='MarkdownV2',
                         reply_markup=markup)
    elif (message.text == "Порядок рефакторинга "
                          "- выделение метода"):
        markup = (types.ReplyKeyboardMarkup
                  (resize_keyboard=True))
        btn1 = types.KeyboardButton("Достоинства "
                                    "- выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад "
                                    "к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Порядок"
                              f" рефакторинга\\: \n"
f"1\\) Создайте новый метод и назовите его так, "
  f"чтобы название отражало суть того, что будет делать"
                                f" этот метод\\. \n \n"
f"2\\) Скопируйте беспокоящий вас фрагмент "
                      f"кода в новый метод\\. "
f"Удалите этот фрагмент из старого места и"
          f" замените вызовом вашего нового метода\\.\n"
f"Найдите все переменные, которые"
          f" использовались в этом фрагменте кода\\. "
f"Если они были объявлены внутри этого "
                          f"фрагмента и не используются вне "
f"его, просто оставьте их без изменений \\- они"
f" станут локальными переменными нового метода\\. \n \n"
f"3\\) Если переменные объявлены перед "
              f"интересующим вас участком кода,"
f" значит, их следует передать в"
          f" параметры вашего нового метода, чтобы"
f" использовать значения, которые в них "
                  f"находились ранее\\. "
f"Иногда от таких переменных проще"
              f" избавиться с помощью "
f"замены переменных вызовом метода\\. \n \n"
f"4\\) Если вы видите, что локальная "
                  f"переменная как\\-то изменяется "
f"в вашем участке кода, это может означать,"
              f" что её изменённое значение"
f" понадобится дальше в основном методе\\."
          f" Проверьте это\\. "
f"Если подозрение подтвердилось, "
              f"значение этой переменной следует "
f"возвратить в основной метод, "
              f"чтобы ничего не сломать\\.",
     parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга"
                          " - выделение метода"):
        markup = (types.ReplyKeyboardMarkup
                  (resize_keyboard=True))
        btn1 = types.KeyboardButton("Достоинства - "
                                    "выделение метода")
        btn2 = types.KeyboardButton("Порядок рефакторинга"
                                " - выделение метода")
        back = types.KeyboardButton("🔙 Назад "
                            "к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
                         f"Причины рефакторинга\\: \n"
f"Чем больше строк кода в методе, тем сложнее разобраться "
                     f"в том, что он делает\\."
f" Это основная проблема, которую решает этот рефакторинг\\. \n \n"
f"Извлечение метода не только убивает множество запашков в коде,"
f" но и является одним из этапов множества других рефакторингов\\. \n",
parse_mode='MarkdownV2', reply_markup=markup)


    elif (message.text == "Достоинства - выделение метода"):
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок рефакторинга"
                                    " - выделение метода")
        btn2 = types.KeyboardButton("Причины рефакторинга -"
                                    " выделение метода")
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
f"1\\) Улучшает читабельность кода\\. Постарайтесь дать новому"
f" методу название, которое бы отражало суть того, что "
f"он делает\\. Например, createOrder\\(\\), "
f"renderCustomerInfo\\(\\) и т\\. д\\. \n"
f"2\\) Убирает дублирование кода\\. Иногда код,"
f" вынесенный в метод, можно найти "
f"и в других местах программы\\. В таком случае, "
f"имеет смысл заменить найденные"
f" участки кода вызовом вашего нового метода\\. \n"
f"3\\) Изолирует независимые части кода, уменьшая "
f"вероятность ошибок \\(например,"
f" по вине переопределения не той переменной\\)\\. \n \n ",
     parse_mode='MarkdownV2', reply_markup=markup)
    elif (message.text == "🔙 Назад в основное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=
                                           True)
        btn1 = types.KeyboardButton("Методы рефакторинга")
        btn2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
text="{0.first_name} сново в основном меню! Напоминаю я"
" бот который разбирается в java, могу рассказать о "
"методах рефакторинга".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "Выделение класса"):
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        btn5 = types.KeyboardButton("Причины рефакторинга "
                        "- выделение класса")
        btn1 = types.KeyboardButton("Достоинства и"
                    " недостатки - выделение класса")
        btn2 = types.KeyboardButton("Порядок"
                    " рефакторинга - выделение класса")
        back = types.KeyboardButton("🔙 Назад "
                    "к методом рефакторинга")
        markup.add(btn1, btn2, btn5, back)
        photo_false = open('Class_Extraction_False.jpg', 'rb')
        photo = open('Class_Extraction.jpg', 'rb')
        bot.send_message(message.chat.id,
f"Выделение класса \\(Class Extraction\\) "
f"\\- это процесс рефакторинга кода,"
f" в ходе которого часть функциональности или"
f" данных из одного класса выносится "
f"в отдельный класс\\. "
f"Это делается для того, чтобы каждый класс"
f" имел четко определенную "
f"ответственность и был легче понять,"
f" использовать и поддерживать\\. \n \n"
f"Пример с неправильной реализацией\\:",
parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo_false)
        bot.send_message(message.chat.id,
f"Пример с правильной реализацией\\:",
parse_mode='MarkdownV2', reply_markup=markup)
        bot.send_photo(message.chat.id, photo)

    elif (message.text == "Порядок рефакторинга -"
                          " выделение класса"):
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства"
                        " - выделение метода")
        btn2 = types.KeyboardButton("Причины "
            "рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад "
                    "к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
         f"Порядок рефакторинга\\: \n"
f"Перед началом рефакторинга обязательно определите, "
f"как именно следует разделить обязанности класса\\."
f"1\\) Создайте новый класс, который будет содержать "
f"выделенную функциональность\\. \n \n"
f"2\\) Создайте связь между старым и новым классом\\."
f" Лучше всего, если эта связь будет односторонней\\;"
f" при этом второй класс можно будет без проблем "
         f"использовать повторно\\."
f" С другой стороны\\, если вы считаете\\, что это необходимо\\,"
f" всегда можно создать двустороннюю связь\\. \n"
f"3\\) Используйте перемещение поля и перемещение метода для каждого "
f"поля и метода, которые вы решили переместить в новый класс\\. "
f"Для методов имеет смысл начинать с приватных\\, таким образом вы "
f"снижаете вероятность допустить массу ошибок\\."
f" Старайтесь двигаться понемногу и тестировать результат после "
f"каждого перемещения\\, это избавит вас от необходимости исправлять "
f"большое число ошибок в самом конце\\. \n \n"
f"После того как с перемещением покончено\\, пересмотрите ещё раз на"
f"   получившиеся классы\\. Возможно\\, старый класс теперь имеет"
f" смысл назвать по\\-другому ввиду его изменившихся обязанностей\\. "
f"Проверьте ещё раз\\, можно ли избавиться от двусторонней связи "
f"между классами\\, если она возникла\\."
f"4\\) Ещё одним нюансом является доступность нового класса извне\\. "
f"Вы можете полностью спрятать его от клиента\\, сделав приватным\\,"
f" управляя при этом его полями из старого класса\\. Либо сделать его "
f"публичным\\, предоставив клиенту возможность напрямую менять "
f"значения\\. Решение зависит от того\\, насколько безопасны для "
f"поведения старого класса будут неожиданные прямые изменения"
f" значений в новом классе\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга"
                      " - выделение класса"):
        markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства "
                        "- выделение метода")
        btn2 = types.KeyboardButton("Порядок "
            "рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад "
                    "к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
     f"Причины рефакторинга\\: \n"
f"Классы всегда изначально выглядят чёткими и понятными\\. "
f"Они выполняют свою работу и не лезут в обязанности "
     f"других классов\\. "
f"Однако, с течением жизни программы добавляется один метод "
f" \\- тут, одно поле  \\- там\\. В результате некоторые классы"
f" получают массу дополнительных обязанностей\\. \n \n",
                         parse_mode='MarkdownV2', reply_markup=markup)


    elif (message.text == "Достоинства и "
      "недостатки - выделение класса"):
        markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True)
        btn1 = types.KeyboardButton("Порядок"
            " рефакторинга - выделение метода")
        btn2 = types.KeyboardButton("Причины "
            "рефакторинга - выделение метода")
        back = types.KeyboardButton("🔙 Назад "
                "к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
         f"Достоинства\\: \n"
f"1\\) Этот рефакторинг призван помочь в соблюдении "
         f"принципа единственной"
f" обязанности класса\\. Это делает код ваших классов"
         f" очевиднее и понятнее\\.\n"
f"2\\) Классы с единственной обязанностью более"
         f" надёжны и устойчивы к "
f"изменениям\\. Например, у вас есть класс, "
         f"отвечающий за "
f"десять разных вещей\\. И когда вам придётся "
         f"вносить в него изменения, "
f"вы рискуете при корректировках одной вещи "
         f"сломать другие\\. \n\n"
f"Недостатки\\: \n"
f"1\\) Если при проведении этого "
         f"рефакторинга вы перестараетесь,"
f" придётся прибегнуть к встраиванию класса\\. \n",
parse_mode='MarkdownV2', reply_markup=markup)


    # Объединение условных выражений
    elif (message.text == "Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = (types.KeyboardButton
("Причины рефакторинга - Объединение условных выражений"))
        btn1 = (types.KeyboardButton
("Достоинства - Объединение условных выражений"))
        btn2 = (types.KeyboardButton
("Порядок рефакторинга - Объединение условных выражений"))
        back = (types.KeyboardButton
        ("🔙 Назад к методом рефакторинга"))
        markup.add(btn1, btn2, btn5, back)
        str_out_false1 = (
    print_file("Consolidate_Conditional_Expression.java"))
        str_out1 = (
    print_file(""
           "Consolidate_Conditional_Expression_false.java"))
        bot.send_message(message.chat.id,
f"Объединение условных операторов \\- это способ комбинировать"
f" несколько условий в одном выражении для более сложной логики"
f" управления потоком программы\\."
f" В основном это происходит с использованием логических "
f"операторов\\. \n \n"
                         f"Пример с плохим кодом\\:"
                         f"```java\n{str_out1}\n```"
                         f"Пример с правильным кодом\\:"
                         f"```java\n{str_out_false1}\n```",
             parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Причины рефакторинга "
              "- Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = (types.KeyboardButton
        ("Порядок рефакторинга - Объединение условных выражений"))
        btn2 = (types.KeyboardButton
            ("Достоинства - Объединение условных выражений"))
        back = types.KeyboardButton("🔙 Назад"
                            " к методом рефакторинга")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
                         f"Причины рефакторинга\\: \n"
f"Код содержит множество чередующихся операторов, которые "
f"выполняют одинаковые действия\\. "
f"Причина разделения операторов неочевидна\\. \n \n"
f"Главная цель объединения операторов — извлечь условие оператора "
f" в отдельный метод или только в один условный оператор, "
f"упростив его понимание\\. \n",
            parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text ==
          "Достоинства - Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = (types.KeyboardButton
        ("Порядок рефакторинга - Объединение условных выражений"))
        btn2 = (types.KeyboardButton
    ("Причины рефакторинга - Объединение условных выражений"))
        back = types.KeyboardButton("🔙 Назад к методом рефакторинга")
        markup.add(btn2, btn1, back)
        bot.send_message(message.chat.id, f"Достоинства\\: \n"
f"1\\) Убирает дублирование управляющего кода\\. Объединение"
f" множества условных операторов, ведущих к одной цели,"
f" помогает показать, что на самом деле вы делаете только "
f"одну сложную проверку, ведущую к одному общему действию\\. \n"
f"2\\) Объединив все операторы в одном, вы позволяете "
f"выделить это сложное условие в новый метод с названием, "
f"отражающим суть этого выражения\\. \n",
                         parse_mode='MarkdownV2', reply_markup=markup)

    elif (message.text == "Порядок рефакторинга"
                      " - Объединение условных выражений"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Достоинства"
                    " - Объединение условных выражений")
        btn2 = types.KeyboardButton("Причины рефакторинга"
                        " - Объединение условных выражений")
        back = types.KeyboardButton("🔙"
                            " Назад к методом рефакторинга")
        markup.add(btn2, btn1, back)
        bot.send_message(message.chat.id,
f"Порядок рефакторинга\\: \n"
f"Перед тем как осуществлять рефакторинг, убедитесь, что в"
f" условиях операторов нет «побочных эффектов», или, другими"
f" словами, они не модифицируют что\\-то, а только возвращают "
f"значения\\."
f"Побочные эффекты могут быть и в коде, который выполняется"
f" внутри самого оператора\\. Например, по результатам условия,"
f" что\\-то добавляется к переменной\\."
f"1\\) Объедините множество условий в одном с помощью операторов"
f" и и или\\. Объединение операторов обычно следует такому "
f"правилу\\: \n \n"
f"\\-\\-\\-\\- Вложенные условия соединяются с "
f"помощью оператора и\\. \n"
f"\\-\\-\\-\\- Условия, следующие друг за другом, соединяются"
f" с помощью оператора или\\. \n \n"
f"4\\) Извлеките метод из условия оператора и назовите его так,"
f" чтобы он отражал суть проверяемого выражения\\.",
                         parse_mode='MarkdownV2', reply_markup=markup)

    else:
        analiz_itog(message)


bot.polling()
