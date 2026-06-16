from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

import utils as util
import buttons as btn
import states as state
from config.bot import bot
from config.settings import GROUP_ID


@bot.callback_query_handler(lambda c: c.data == "register_btn")
def handler_start_btn(query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    bot.set_state(user_id, state.Register.fio, chat_id)
    bot.send_message(chat_id, "Iltimos toliq ismingizni yozing")


@bot.message_handler(content_types=["text"], state=state.Register.fio)
def handler_fio(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fio = message.text
    with bot.retrieve_data(user_id, chat_id) as data:
        data["fio"] = fio
        bot.set_state(user_id, state.Register.age, chat_id)
        bot.send_message(chat_id, "Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())
        print(data)


@bot.message_handler(content_types=["text"], state=state.Register.age)
def handler_age(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    age = message.text  # "hello"
    if age.isdigit():  # True|False # "123"=True
        age = int(age)
        if age > 13 and age < 30:
            # '1' > 13
            # True or False == True
            # True and False == False
            with bot.retrieve_data(user_id, chat_id) as data:
                data["age"] = age
                fio = data["fio"]
                bot.set_state(user_id, state.Register.course, chat_id)
                bot.send_message(chat_id, f"Iltimos {fio}, bizni kurslardan birini tanlang", reply_markup=btn.courses())
        else:
            bot.set_state(user_id, state.Register.age, chat_id)
            bot.send_message(chat_id,
                             "Kechirasiz, bizni kursalar 13-30 yoshgacham mojjallangan.")
    else:
        bot.set_state(user_id, state.Register.age, chat_id)
        bot.send_message(chat_id,
                         "Kechirasiz, faqat raqam yozing\n <b>masalan</b>: <i>25</i>",
                         parse_mode="HTML")


@bot.message_handler(content_types=["text"], state=state.Register.course)
def handler_course(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text in btn.COURSES:
        with bot.retrieve_data(user_id, chat_id) as data:
            data["course"] = text
            bot.set_state(user_id, state.Register.contact, chat_id)
            bot.send_message(
                chat_id,
                "Telefon raqamingizni yuboring pastdagi tugma orqali\n"
                "Yoki shu formatda: +998332300701\n\n"
                "<i>Siz bilan bog'lanishimiz uchun bu muxim</i>",
                reply_markup=btn.share_contact(), parse_mode="HTML")
    else:
        bot.set_state(user_id, state.Register.course, chat_id)
        bot.send_message(chat_id,
                         "Faqat pastdagi tugmalardan foydalaning",
                         reply_markup=btn.courses())


@bot.message_handler(content_types=["text", "contact"], state=state.Register.contact)
def handler_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text:
        print("here")
        import re
        pattern = r"^\+?(998)?(9(0|1|3|4|5|7|8|9)|88|20|50|33|77)\d{7}$"
        if re.match(pattern, message.text):
            with bot.retrieve_data(user_id, chat_id) as data:
                data["contact"] = message.text
                bot.set_state(user_id, state.Register.address, chat_id)
                bot.send_message(chat_id,
                                 "Yashash manzilingizni yozing",
                                 reply_markup=btn.share_location())
        else:
            bot.set_state(user_id, state.Register.contact)
            bot.send_message(
                chat_id,
                "Iltimos tog'ri formatda yuboring yoki pastdagi tugmani bosing\n"
                "<b>Format</b>: <i>+998332300701</i>", parse_mode="HTML",
                reply_markup=btn.share_contact()
            )
    if message.contact:
        with bot.retrieve_data(user_id, chat_id) as data:
            data["contact"] = message.contact.phone_number
            bot.set_state(user_id, state.Register.address, chat_id)
            bot.send_message(chat_id,
                             "Yashash manzilingizni yuboring",
                             reply_markup=btn.share_location())


@bot.message_handler(content_types=["location", "text"], state=state.Register.address)
def handler_address(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.location:
        with bot.retrieve_data(user_id, chat_id) as data:
            data["latitude"] = message.location.latitude
            data["longitude"] = message.location.longitude
            bot.set_state(user_id, state.Register.study_time, chat_id)
            bot.send_message(chat_id, "O'qish vaqtini tanlang", reply_markup=btn.study_time())

    if message.text:
        bot.set_state(user_id, state.Register.address, chat_id)
        bot.send_message(chat_id,
                         "Yashash manzilingizni yuboring",
                         reply_markup=btn.share_location())


@bot.message_handler(content_types=["text"], state=state.Register.study_time)
def handler_study_time(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text in btn.STUDY_TIME:
        with bot.retrieve_data(user_id, chat_id) as data:
            data["study_time"] = text
            bot.set_state(user_id, state.Register.document, chat_id)
            bot.send_message(chat_id,
                             "Hujjatingizni yuboring",
                             reply_markup=ReplyKeyboardRemove())
    else:
        bot.set_state(user_id, state.Register.study_time, chat_id)
        bot.send_message(chat_id,
                         "Faqat pastdagi tugmalardan foydalaning",
                         reply_markup=btn.study_time())


@bot.message_handler(content_types=["document", "photo", "text"], state=state.Register.document)
def handler_document(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.photo:
        photo = message.photo[-1]
        with bot.retrieve_data(user_id, chat_id) as data:
            data["document"] = photo.file_id
            bot.set_state(user_id, state.Register.confirmation, chat_id)
            text = util.generate_text(data) + "<b>Barcha Malumotlar tog'rimi ?</b>"
            bot.send_message(chat_id,
                             text, parse_mode="HTMl",
                             reply_markup=btn.confirm())
    if message.document:
        filename = message.document.file_name
        if filename.endswith(".pdf"):
            with bot.retrieve_data(user_id, chat_id) as data:
                data["document"] = message.document.file_id
                bot.set_state(user_id, state.Register.confirmation, chat_id)
                text = util.generate_text(data) + "<b>Barcha Malumotlar tog'rimi ?</b>"
                bot.send_message(chat_id,
                                 text, parse_mode="HTMl",
                                 reply_markup=btn.confirm())
        else:
            bot.set_state(user_id, state.Register.document, chat_id)
            bot.send_message(chat_id,
                             "Hujjatingizni yuboring faqat pdf formatda",
                             reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"], state=state.Register.confirmation)
def handler_confirm(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text == "❌Yoq":
        bot.delete_state(user_id, chat_id)
        bot.send_message(
            chat_id,
            "Bekor qilindi qaytadan boshlash uchun  /start ni bosing",
            reply_markup=ReplyKeyboardRemove())
    elif text == "✅Ha":
        with bot.retrieve_data(user_id, chat_id) as data:
            text = util.generate_text(data)
            try:
                bot.send_document(
                    GROUP_ID,
                    document=data.get("document"),
                    caption=text, parse_mode="HTML"
                )
            except Exception:
                bot.send_photo(
                    GROUP_ID,
                    photo=data.get("document"),
                    caption=text, parse_mode="HTML"
                )
            bot.send_message(
                chat_id, "Malumotlar yuborildi.",
                reply_markup=ReplyKeyboardRemove())
            data.clear()
        bot.delete_state(user_id, chat_id)
