from functools import reduce
import random
import string
import os
from telegram import (Update ,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ReplyKeyboardMarkup,
                      BotCommand,
                      BotCommandScopeChat,
                      )
#import asyncio
import json
import mysql.connector
from typing import Final
from telegram.ext import (Application,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          filters,
                          ContextTypes,
                          )

#TOKEN: Final = os.getenv("API_KEY")
ADMIN_ID: Final = int(os.getenv("ADMIN"))
BOT_USERNAME = "@INSTABOT_shop_bot"

# instagram bots list

insta_bots = {
        "WELCOME_BOT":"""1️⃣ ربات خوشامدگویی به فالوورهای جدید\n
هر فالوور جدیدی که به پیجت اضافه بشه، یه پیام خوشامدگویی دریافت می‌کنه! می‌تونی توی این پیام لینک سایت، تخفیف ویژه یا معرفی محصولت رو بذاری تا فالوورای جدیدت از همون اول با خدماتت آشنا بشن. دیگه نیازی به ارسال دستی پیام نیست، این ربات خودش کارو برات انجام می‌ده!""",
        "LOTTERY_COMMENT":"""2️⃣ ربات قرعه‌کشی کامنتی\n
می‌خوای یه مسابقه جذاب برگزار کنی؟ این ربات کامنت‌های یه پست خاص رو بررسی می‌کنه و از بین افرادی که یه کلمه خاص رو کامنت گذاشتن، یه برنده یا چند برنده رو به‌صورت شانسی انتخاب می‌کنه! می‌تونی شرط تعیین کنی که فقط کسانی که یه کلمه خاص نوشتن توی قرعه‌کشی شرکت کنن، یا اینکه بین همه کامنت‌ها قرعه‌کشی انجام بشه.""",
        "MENTIONS_ANSWER":"""3️⃣ ربات پاسخ خودکار به منشن‌ها\n
هر وقت کسی توی استوری یا کامنت اسم پیجت رو منشن کنه، این ربات به‌صورت خودکار براش یه پیام می‌فرسته. می‌تونی ازش برای تشکر از منشن، ارسال کد تخفیف، معرفی محصول یا هدایت به دایرکت استفاده کنی. با این کار، هم تعامل بیشتری می‌گیری، هم پیجت حرفه‌ای‌تر دیده می‌شه!""",
        "GETUSER_INFO":"""4️⃣ ربات دریافت اطلاعات از کاربران\n
می‌خوای از مشتری‌هات شماره، ایمیل یا اطلاعات دیگه‌ای بگیری؟ این ربات به‌صورت خودکار توی دایرکت اطلاعاتی که نیاز داری رو از کاربر دریافت و ذخیره می‌کنه. مثلاً می‌تونی یه فرم ثبت‌نام داشته باشی که هر کسی پیام بده، اطلاعاتش جمع‌آوری بشه. دیگه نیازی به پیگیری دستی نداری، این ربات همه‌چیزو برات منظم می‌کنه!""",
        "STORY_REMINDER":"""5️⃣ ربات یادآوری استوری\n
خیلی از فالوورها استوری‌هاتو نمی‌بینن، اما با این ربات می‌تونی بهشون پیام بدی و یادآوری کنی که استوری جدیدتو ببینن! می‌تونی لینک استوری، توضیحات یا پیشنهاد ویژه بذاری تا نرخ بازدید استوری‌هات بالاتر بره و تعامل بیشتری بگیری.""",
        "DEFAULT_DIRECT":"""6️⃣ ربات پاسخ هوشمند به دایرکت\n
اگه کسی توی دایرکت یه کلمه خاص (مثلاً "قیمت"، "خرید"، "ارسال") رو بفرسته، این ربات به‌صورت خودکار جواب مناسب رو براش ارسال می‌کنه! دیگه لازم نیست برای هر پیام دستی جواب بدی، این ربات مثل یه پشتیبان ۲۴ ساعته برای پیجت عمل می‌کنه و سوالات رایج رو جواب می‌ده.""",
        "COMMENT_DIRECT":"""7️⃣ ربات پاسخ خودکار به کامنت‌ها\n
یه روش فوق‌العاده برای افزایش تعامل و فروش! با این ربات، هر کسی که زیر پست‌های مشخص‌شده یه کلمه خاص رو کامنت کنه، به‌صورت خودکار یه پیام دایرکت دریافت می‌کنه.
✅ ارسال لینک دانلود بعد از کامنت "دانلود"
✅ ارسال کد تخفیف بعد از کامنت "تخفیف"
✅ هدایت کاربر به سایت یا محصول خاص
می‌تونی تعیین کنی که فقط روی یه پست خاص فعال باشه یا روی همه پست‌ها!""",
        "STORYREP_DIRECT":"""8⃣ ربات پاسخ خودکار به ریپلای استوری\n
اگه کسی استوری‌تو ریپلای کنه، این ربات به‌صورت خودکار براش یه پیام ارسال می‌کنه.
✅ ارسال لینک یا توضیحات بعد از ریپلای به استوری
✅ پاسخ خودکار به استوری‌های تعاملی (مثل نظرسنجی‌ها)
✅ راهنمایی مشتری‌ها بدون نیاز به جواب دستی
این ربات بهت کمک می‌کنه همیشه با فالوورات در تعامل باشی، بدون اینکه وقتت گرفته بشه!
💡 چرا این ربات‌ها ضروری هستن؟
🔹 افزایش تعامل و درگیر کردن فالوورها
🔹 رشد سریع‌تر پیج و جذب فالوور واقعی
🔹 صرفه‌جویی در زمان و مدیریت راحت‌تر پیج
🔹 افزایش فروش و بهبود تجربه مشتری
📩 همین حالا ربات مورد نظرت رو سفارش بده و اینستاگرامتو حرفه‌ای‌تر کن! 🚀"""}

# data base info

DB_CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "database": os.getenv("USER")
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_discount_code(length=6):
    characters = string.ascii_uppercase + string.digits  # حروف بزرگ و اعداد
    return ''.join(random.choices(characters, k=length))

# تولید یک کد تخفیف




# commands

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):

    if update.message.chat.id == ADMIN_ID:
        command = [BotCommand("start", "شروع کردن ربات"),
                   BotCommand("admin", "فرستادن پیام همگانی"),
                   BotCommand("check", "برسی تعداد ارسال"),
                   BotCommand("users","لیست کاربران")]
        scope = BotCommandScopeChat(chat_id=ADMIN_ID)
        await app.bot.set_my_commands(command,scope=scope)

    chat_id = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("ربات ها🤖", callback_data="bots"),
         InlineKeyboardButton("قوانین و مقررات📙", callback_data="law")],
        [InlineKeyboardButton("ربات های شما", callback_data="mybots"),
         InlineKeyboardButton("راهنما📖", callback_data="guide")],
        [InlineKeyboardButton("👩‍💻پشتیبانی👩‍💻", callback_data="backup")]
    ]
    keyboards = [
        ["🤖ربات ها🤖"],
        ["حساب کاربری📗","ربات های من🤖"],
        ["سبد خرید🛒", "پشتیبانی👩‍💻"],
        ["راهنما📖","تخفیف❤️", "قوانین و مقررات📙"],
    ]
    user_data = {
        "instagram_user": None,
        "instagram_pass": None,
        "OFFS": {},
        "bots": {},
        "Aura": 0,
        "gusses": {}
    }
    jason_obj = json.dumps(user_data)
    reply_markup = InlineKeyboardMarkup(buttons)
    reply_markup2 = ReplyKeyboardMarkup(keyboards,resize_keyboard=True)
    await update.message.reply_text(f"""💡 مدیریت اینستاگرام راحت‌تر از همیشه!
سلام! 👋 خوش اومدی به @INSTABOT_shop_bot 🚀""", reply_markup=reply_markup2)
    await update.message.reply_text("""
اینجا می‌تونی ربات‌هایی داشته باشی که بهت کمک می‌کنن تعامل پیجت رو ببری بالا و کاراتو هوشمندتر کنی:

✅ ربات خوشامدگویی به فالوورهای جدید – به محض فالو کردن، یه پیام حرفه‌ای براشون ارسال می‌کنه!

🎁 ربات قرعه‌کشی کامنتی – از بین کسایی که یه کلمه خاص رو کامنت کنن، برنده رو انتخاب کن!

🔔 ربات پاسخ خودکار به منشن‌ها – هر وقت کسی پیجت رو منشن کنه، یه پیام خودکار براش ارسال کن.

📩 ربات دریافت اطلاعات از کاربران – شماره، ایمیل یا هر اطلاعات دیگه‌ای که نیاز داری رو از کاربرا بگیر.

👀 ربات یادآوری استوری – به فالوورات پیام بده که استوری‌های جدیدت رو ببینن!

💬 ربات پاسخ هوشمند به دایرکت – هر کسی یه کلمه خاص رو بفرسته، ربات جواب مناسب رو براش ارسال می‌کنه!

با این ابزارها، هم در وقتت صرفه‌جویی می‌کنی، هم تعامل پیجت رو چند برابر می‌کنی! 😎
سوالی داشتی، پشتیبانی رو بزن! 🚀""", reply_markup=reply_markup)
    if context.args[0]:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE chat_id={int(context.args[0])}")
            users = cursor.fetchall()
            data = json.loads(users[0][1])
            user_data_obj = {
                "instagram_user": data["instagram_user"],
                "instagram_pass": data["instagram_pass"],
                "OFFS": data["OFFS"],
                "bots": data["bots"],
                "Aura": data["Aura"],
                "gusses":data["gusses"].add(chat_id)
            }
            if user_data_obj ==10:
                discount_code = generate_discount_code()
                while discount_code in user_data_obj["OFFS"]:
                    discount_code = generate_discount_code()
                user_data_obj["OFFS"].add(discount_code)

            user_j = json.dumps(user_data_obj)
            cursor.execute(f"UPDATE `users` SET `user_data`=(%s) WHERE chat_id={int(context.args[0])} ", (user_j,))
            conn.commit()
            print(f"data : {data}")
        except mysql.connector.Error as e:
            print(f"error caused {e}")


    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO users (chat_id) VALUE ({chat_id})")
        conn.commit()
        cursor.execute(f"UPDATE `users` SET `user_data`=(%s) WHERE chat_id={chat_id} ", (jason_obj,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ خطای MySQL: {err}")
    finally:
        cursor.close()
        conn.close()

async def see_insta_bots(update:Update,context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.user_data["show_pros"] = True
    keyboard = [
        ["سبد خرید🛒","بازگشت🔙"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)

    context.user_data["list_text"] = await context.bot.send_message(chat_id=chat_id, text="🤖لیست ربات های اینستاگرام🤖", reply_markup=reply_markup)

    if not context.user_data.get("seebots"):
        context.user_data["seebots"] = {"message_ids":[], "more":0}

    for bot , guide in list(insta_bots.items())[0:3]:
        button = [
                [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")]
            ]

        reply_markup = InlineKeyboardMarkup(button)
        context.user_data["product"] = await context.bot.send_message(text=guide,
                                           reply_markup=reply_markup,
                                           chat_id=chat_id)
        context.user_data.values().mapping["seebots"]["message_ids"].append(context.user_data.get("product").message_id)

    message_id = context.user_data.values().mapping["seebots"]["message_ids"]
    button = [
            [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")],
            [InlineKeyboardButton("بیشتر↓", callback_data="more")]
        ]

    reply_markup= InlineKeyboardMarkup(button)
    context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=message_id[-1], reply_markup=reply_markup)

async def mybots(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.user_data.get("mybots"):
        context.user_data["mybots"] = {}
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT user_data FROM users WHERE chat_id={chat_id}")
            users = cursor.fetchall()
            print(f"users : {users}")
            print(f"data: {json.loads(users[0][0])}")
            user_data = json.loads(users[0][0])
            print(user_data.get("bots"))
            if user_data.get("bots"):
                context.user_data["mybots"] = user_data.get("bots")

                await context.bot.send_message(chat_id=chat_id,
                                               text=f"🤖لیست ربات های شما🤖:\n \n "
                                                    f"{"\n".join(f"{key} : {value} "
                                                                 for key, value in context.user_data.get("mybots").items())}")
            else:
                await context.bot.send_message(chat_id=chat_id,
                                               text="متاسفانه شما رباتی ندارید😓")
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"❌ خطای MySQL: {err}")
        finally:
            conn.close()
    else:
        await context.bot.send_message(chat_id=chat_id,
                                           text=f"🤖لیست ربات های شما🤖:\n \n "
                                                f"{"\n".join(f"{key} : {value} "
                                                             for key, value in context.user_data.get("mybots").items())}")

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id,text="""راهنمای کامل و مطمئن استفاده از ربات‌ها 📖✨
سوالات متداول:
✅ چگونه از ربات‌ها استفاده کنم؟
بعد از خرید و تأیید سفارش، آموزش کامل استفاده از ربات برای شما ارسال می‌شود. با راهنمای گام‌به‌گام، به‌راحتی می‌توانید از آن استفاده کنید.
✅ آیا برای استفاده از ربات‌ها به رمز عبور نیاز است؟
بله، برای عملکرد صحیح ربات‌ها، نیاز به نام کاربری و رمز عبور پیج اینستاگرام شماست. امنیت اطلاعات شما برای ما در اولویت است.
✅ اگر در استفاده از ربات‌ها مشکل داشتم؟
نگران نباشید! تیم پشتیبانی همیشه در کنار شماست. کافی است دکمه "پشتیبانی" را بزنید تا مشکل شما را سریع حل کنیم.
✅ چطور تخفیف بگیرم؟
با زدن دکمه "تخفیف"، می‌توانید روش‌های دریافت تخفیف را ببینید. علاوه بر این، بعد از هر خرید، امتیاز جمع می‌کنید که در آینده می‌توانید آن‌ها را به تخفیف تبدیل کنید.
✅ ربات‌ها چطور کار می‌کنند؟
ربات‌ها برای اجرا به سرور نیاز دارند، اما نگران هزینه نباشید! ما سرور رایگان در اختیارتان قرار می‌دهیم و ربات شما را روی سرور خودمان راه‌اندازی می‌کنیم. هر زمان که خواستید، می‌توانید سورس کد پروژه را تحویل بگیرید و یا ربات خود را خاموش یا روشن کنید.
✅ چطور ربات‌هایم را مدیریت کنم؟
از بخش "🤖 ربات‌های من 🤖" می‌توانید به‌راحتی ربات‌های خود را مدیریت کنید.
اعتماد شما سرمایه ماست، پس با خیال راحت از خدمات ما استفاده کنید! ❤️""")

async def backup(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(text="""پیام خود را ارسال کنید. پیام شما به صورت خودکار از طریق ربات برای تیم پشتیبانی ارسال خواهد شد و در اسرع وقت از طریق همین ربات پاسخ خواهید گرفت. در صورتی که نیاز به کمک بیشتری داشتید، ما همیشه در کنار شما هستیم. :)""",
                                   chat_id=chat_id)
    context.user_data["backup"] = True

async def laws(update: Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="""📌 قوانین و مقررات استفاده از ربات
🔹 نوع خدمات:
ما فقط ربات‌های مدیریت و تعامل هوشمند در اینستاگرام ارائه می‌دهیم و هیچ‌گونه خدمات فالو، آنفالو، لایک، ویو یا افزایش تعامل غیرواقعی نداریم. ربات‌های ما شامل:
✅ ربات خوش‌آمدگویی به فالوورهای جدید
✅ ربات قرعه‌کشی کامنتی
✅ ربات پاسخ خودکار به منشن‌ها
✅ ربات دریافت اطلاعات از کاربران
✅ ربات یادآور استوری
✅ ربات پاسخ خودکار به کامنت‌ها
✅ ربات پاسخ هوشمند به دایرکت
✅ ربات پاسخ خودکار به ریپلای استوری
🔹 امنیت و حریم خصوصی:
برای استفاده از ربات‌ها، وارد کردن نام کاربری و رمز عبور اینستاگرام ضروری است. اطلاعات شما رمزگذاری‌شده و کاملاً محرمانه ذخیره می‌شود و هیچ‌کس جز شما به آن دسترسی ندارد.
🔹 حذف اطلاعات:
در هر زمان که بخواهید، می‌توانید از بخش "حساب کاربری" درخواست حذف اطلاعات دهید تا تمام داده‌های شما از سیستم پاک شود.
🔹 مسئولیت کاربر:
⚠️ مسئولیت امنیت حساب اینستاگرام بر عهده خود شماست.
⚠️ استفاده نادرست از ربات‌ها که منجر به مسدود شدن حساب شود، بر عهده کاربر است.
🔹 تعهدات ما:
✔️ اطلاعات شما در اختیار هیچ فرد یا سازمانی قرار نمی‌گیرد.
✔️ سرورهای ما امن و مطمئن هستند و از داده‌های شما محافظت می‌کنند.
✔️ تیم پشتیبانی همیشه همراه شماست! از طریق دکمه "پشتیبانی" با ما در تماس باشید.
🔹 قوانین مالی:
💰 بازگشت وجه امکان‌پذیر نیست. لطفاً قبل از خرید، توضیحات مربوط به هر ربات را با دقت مطالعه کنید.
🔹 به‌روزرسانی قوانین:
🔄 قوانین ممکن است تغییر کنند، لطفاً این بخش را به‌صورت دوره‌ای مطالعه کنید.
✅ استفاده از ربات به‌منزله پذیرش این قوانین است.
با خیال راحت از خدمات ما استفاده کنید! ❤️""")

async def off(update: Update,context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    link = f"http://t.me/INSTABOT_shop_bot?start={chat_id}"

    await context.bot.send_message(chat_id=chat_id, text=f"""🚀 مدیریت حرفه‌ای اینستاگرام، بدون زحمت!

دیگه لازم نیست ساعت‌ها وقت بذاری تا به کامنت‌ها، دایرکت‌ها و منشن‌ها پاسخ بدی! 🤯 با ربات‌های هوشمند ما، همه‌چیز اتوماتیک و حرفه‌ای انجام میشه!

✨ چیارو می‌تونی اتومات کنی؟
✅ خوش‌آمدگویی به فالوورهای جدید
✅ قرعه‌کشی حرفه‌ای بین کامنت‌ها 🎁
✅ پاسخ خودکار به دایرکت و کامنت‌ها
✅ منشن‌های مهم رو از دست نده!
✅ یادآوری استوری و تعامل بیشتر 📢

💡 مدیریت پیجت رو هوشمند کن و در زمانت صرفه‌جویی کن!
همین حالا ربات موردنظرت رو فعال کن و اینستاگرام رو مثل یه حرفه‌ای مدیریت کن!

🔥 شروع کن ⏳👉 [لینک به ربات]({link})""",parse_mode="Markdown")
    await context.bot.send_message(chat_id,
                                   text="پیام بالا رو به اشتراک بزارید, اگر بتونید ده نفر کار بر جذب کنین, یه کد 25 درصد تخفیف برای قیمت کلتون میگیرید❤️")

# admin commands
async def bot_members(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id == ADMIN_ID:
        timer = await update.message.reply_text("⌛️")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        if users:
            chat_ids = "\n".join(str(user[0]) for user in users)
            await context.bot.edit_message_text(chat_id=ADMIN_ID,
                                                text=f"📋 لیست چت آیدی ها:\n{chat_ids}",
                                                message_id=timer.message_id)
        else:
            await context.bot.edit_message_text(chat_id=ADMIN_ID,
                                                text="❌ هیچ کاربری ثبت نشده است.",
                                                message_id=timer.message_id)

# button handler

async def button_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    bots = ["WELCOME_BOT",
     "LOTTERY_COMMENT",
     "MENTIONS_ANSWER",
     "GETUSER_INFO",
     "STORY_REMINDER",
     "DEFAULT_DIRECT",
     "COMMENT_DIRECT",
     "STORYREP_DIRECT"]
    query = update.callback_query
    data = query.data
    print(data)
    try:
        pro = (data.split("-")[1] in bots)
    except Exception:
        pass

    match data:
        case "bots":
            await see_insta_bots(update,context)
        case "backup":
            await backup(update,context)
        case "more":
            if context.user_data.values().mapping["seebots"]["more"] <1:
                print("more 0 -> 1")
                context.user_data.values().mapping["seebots"]["more"] = 1
                call_backdata = context.user_data["product"].reply_markup.inline_keyboard[0][0]["callback_data"]

                if call_backdata.split("-")[0] == "buy" :
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bots[2]}")]
                    ]
                else:
                    button = [
                        [InlineKeyboardButton("به سبد خرید افزوده شد✅", callback_data=f"cancel-{bots[2]}")]
                    ]
                message_id = context.user_data.values().mapping["seebots"]["message_ids"][-1]
                reply_markup = InlineKeyboardMarkup(button)
                await context.bot.edit_message_reply_markup(chat_id,message_id=message_id,
                                                            reply_markup=reply_markup)

                for bot , guide in list(insta_bots.items())[3:6]:
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")]
                    ]
                    reply_markup = InlineKeyboardMarkup(button)
                    context.user_data["product"] = await context.bot.send_message(chat_id=chat_id,text=guide,
                                                                                  reply_markup=reply_markup)
                    context.user_data.values().mapping["seebots"]["message_ids"].append(context.user_data.get("product").message_id)

                button = [
                    [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")],
                    [InlineKeyboardButton("کمتر↑", callback_data="less")],
                    [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                ]
                reply_markup = InlineKeyboardMarkup(button)
                message_id = context.user_data.get("product").message_id
                context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id,message_id,reply_markup= reply_markup)
                return

            if context.user_data.values().mapping["seebots"]["more"] == 1:
                print("more 1 ->2")
                context.user_data.values().mapping["seebots"]["more"] = -1
                call_backdata = context.user_data["product"].reply_markup.inline_keyboard[0][0]["callback_data"]

                if call_backdata.split("-")[0] == "buy":
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bots[5]}")]
                    ]
                else:
                    button = [
                        [InlineKeyboardButton("به سبد خرید افزوده شد✅", callback_data=f"cancel-{bots[5]}")]
                    ]
                print("looping")
                message_id = context.user_data.values().mapping["seebots"]["message_ids"][-1]
                reply_markup = InlineKeyboardMarkup(button)
                await context.bot.edit_message_reply_markup(chat_id, message_id=message_id,
                                                            reply_markup=reply_markup)

                for bot, guide in list(insta_bots.items())[6:]:
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")]
                    ]
                    reply_markup = InlineKeyboardMarkup(button)
                    context.user_data["product"] = await context.bot.send_message(chat_id=chat_id, text=guide,
                                                                                  reply_markup=reply_markup)
                    context.user_data.values().mapping["seebots"]["message_ids"].append(context.user_data.get("product").message_id)


                button = [
                    [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bot}")],
                    [InlineKeyboardButton("کمتر↑", callback_data="less")],

                ]
                reply_markup = InlineKeyboardMarkup(button)
                message_id = context.user_data.get("product").message_id
                context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id, message_id,
                                                                                           reply_markup=reply_markup)
                return
        case "less":
            print(context.user_data.values().mapping["seebots"]["more"])
            if context.user_data.values().mapping["seebots"]["more"] > 0:
                try:
                    call_backdata = context.user_data["ms3"].reply_markup.inline_keyboard[0][0]["callback_data"]
                except Exception:
                    call_backdata = context.user_data["product"].reply_markup.inline_keyboard[0][0]["callback_data"]
                context.user_data.values().mapping["seebots"]["more"] = -1
                print(context.user_data.values().mapping["seebots"]["more"])

                message_ids = context.user_data.values().mapping["seebots"]["message_ids"]
                reversed_message_ids = list(reversed(message_ids))
                for message_id in reversed_message_ids[0:3]:
                    await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
                    context.user_data.values().mapping["seebots"]["message_ids"].pop()
                if call_backdata.split("-")[0] == "buy":
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bots[2]}")],
                        [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                    ]
                else:
                    button = [
                        [InlineKeyboardButton("به سبد خرید افزوده شد✅",callback_data=f"cancel-{bots[2]}")],
                        [InlineKeyboardButton("بیشتر↓", callback_data="more")]

                    ]
                reply_markup = InlineKeyboardMarkup(button)
                context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id=chat_id,message_id=message_ids[-1],
                                                            reply_markup=reply_markup)
                print(context.user_data.get("product").reply_markup)
                return

            if context.user_data.values().mapping["seebots"]["more"] == -1:
                print("mor -1 -> -2")
                try:
                    call_backdata = context.user_data["ms6"].reply_markup.inline_keyboard[0][0]["callback_data"]
                except Exception:
                    call_backdata = context.user_data["product"].reply_markup.inline_keyboard[0][0]["callback_data"]
                context.user_data.values().mapping["seebots"]["more"] = 1

                message_ids = context.user_data.values().mapping["seebots"]["message_ids"]
                reversed_message_ids = list(reversed(message_ids))
                for message_id in reversed_message_ids[0:2]:
                    await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
                    context.user_data.values().mapping["seebots"]["message_ids"].pop()
                if call_backdata.split("-")[0] == "buy":
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{bots[5]}")],
                    [InlineKeyboardButton("کمتر↑", callback_data="less")],
                        [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                    ]
                else:
                    button = [
                        [InlineKeyboardButton("به سبد خرید افزوده شد✅",callback_data=f"cancel-{bots[5]}")],
                    [InlineKeyboardButton("کمتر↑", callback_data="less")],
                        [InlineKeyboardButton("بیشتر↓", callback_data="more")]

                    ]
                reply_markup = InlineKeyboardMarkup(button)
                context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id=chat_id,message_id=message_ids[-1],
                                                            reply_markup=reply_markup)
                print(context.user_data.get("product").reply_markup)
                return
        case "mybots":
            await mybots(update,context)
        case "guide":
            await help_command(update,context)
        case "law":
            await laws(update,context)
        case pro:
            if not context.user_data.get("shoplist"):
                context.user_data["shoplist"] = set()
            button = [
                [InlineKeyboardButton("به سبد خرید افزوده شد✅",callback_data=f"cancel-{query.data.split("-")[1]}")]
            ]
            reply_markup = InlineKeyboardMarkup(button)
            message_ids = context.user_data.values().mapping["seebots"]["message_ids"]
            if not query.data.startswith("cancel-"):
                if message_ids[bots.index(query.data.split("-")[1])] == message_ids[-1]:
                    if query.data.split("-")[0] == "buy":
                        if len(message_ids) < 4:
                            button = [
                            [InlineKeyboardButton("به سبد خرید افزوده شد✅", callback_data=f"cancel-{query.data.split("-")[1]}")],
                            [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                        ]
                        elif 3 < len(message_ids) <7:
                            button = [
                                [InlineKeyboardButton("به سبد خرید افزوده شد✅", callback_data=f"cancel-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],
                                [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                            ]
                        elif len(message_ids) >7:
                            button = [
                                [InlineKeyboardButton("به سبد خرید افزوده شد✅", callback_data=f"cancel-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],
                                ]
                    else:
                        if len(message_ids) < 4:

                            button = [
                            [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                            [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                        ]
                        elif 3 < len(message_ids) <7:
                            button = [
                                [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],
                                [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                            ]
                        elif len(message_ids) >7:
                            button = [
                                [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],
                                ]
                    reply_markup = InlineKeyboardMarkup(button)
                    context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id=chat_id,
                                                        message_id=message_ids[bots.index(query.data.split("-")[1])],
                                                        reply_markup=reply_markup)
                    if len(message_ids) <4:
                        context.user_data["ms3"] = context.user_data.get("product")
                    elif 3< len(message_ids) <7:
                        context.user_data["ms6"] = context.user_data.get("product")

                else:
                    await context.bot.edit_message_reply_markup(chat_id=chat_id,
                                                                message_id=message_ids[bots.index(query.data.split("-")[1])],
                                                                reply_markup=reply_markup)


                context.user_data["shoplist"].add(query.data.split("-")[1])
                try:
                    bots_price = {"WELCOME_BOT": 69000,
                                  "LOTTERY_COMMENT": 150000,
                                  "MENTIONS_ANSWER": 90000,
                                  "GETUSER_INFO": 150000,
                                  "STORY_REMINDER": 69000,
                                  "DEFAULT_DIRECT": 150000,
                                  "COMMENT_DIRECT": 100000,
                                  "STORYREP_DIRECT": 100000}
                    shop_list = "\n\n".join(f"نام محصول:{key} , قیمت: {value}".strip() for key, value in bots_price.items() if
                                            key in context.user_data.get("shoplist"))
                    context.user_data["paylist"] = await context.bot.edit_message_text(chat_id=chat_id,
                                                                                       message_id=context.user_data.get(
                                                                                           "paylist").message_id,
                                                                                       text=f"""سبد خرید🛒
نام کاربری:

سفارشات 🤖:
{shop_list}
                ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
                قیمت کل: {reduce(lambda x, y: x + y, [key for bot, key in bots_price.items() if bot in context.user_data.get("shoplist")])}
                قابل پرداخت: {reduce(lambda x, y: x + y, [key for bot, key in bots_price.items() if bot in context.user_data.get("shoplist")])}""")
                except Exception as e:
                    print(f"error, caused{e}")
                return

            elif query.data.startswith("cancel-"):
                if message_ids[bots.index(query.data.split("-")[1])] == message_ids[-1]:
                    if len(message_ids) < 4:
                        button = [
                            [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                            [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                        ]
                    elif 3 < len(message_ids) <7:
                        button = [
                                [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],
                                [InlineKeyboardButton("بیشتر↓", callback_data="more")]
                            ]
                    elif len(message_ids) >7:
                        button = [
                                [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")],
                                [InlineKeyboardButton("کمتر↑", callback_data="less")],]

                    reply_markup = InlineKeyboardMarkup(button)
                    context.user_data["product"] = await context.bot.edit_message_reply_markup(chat_id=chat_id,
                                                        message_id=message_ids[bots.index(query.data.split("-")[1])],
                                                        reply_markup=reply_markup)
                    if len(message_ids) <4:
                        context.user_data["ms3"] = context.user_data.get("product")
                    elif 3< len(message_ids) <7:
                        context.user_data["ms6"] = context.user_data.get("product")
                else:
                    button = [
                        [InlineKeyboardButton("افزودن به سبد خرید🛒", callback_data=f"buy-{query.data.split("-")[1]}")]
                    ]
                    reply_markup = InlineKeyboardMarkup(button)
                    await context.bot.edit_message_reply_markup(chat_id=chat_id,
                                                                message_id=message_ids[bots.index(query.data.split("-")[1])],
                                                                reply_markup=reply_markup)
                context.user_data["shoplist"].remove(query.data.split("-")[1])
                try:
                    bots_price = {"WELCOME_BOT": 69000,
                            "LOTTERY_COMMENT": 150000,
                            "MENTIONS_ANSWER": 90000,
                            "GETUSER_INFO": 150000,
                            "STORY_REMINDER": 69000,
                            "DEFAULT_DIRECT": 150000,
                            "COMMENT_DIRECT": 100000,
                            "STORYREP_DIRECT": 100000}
                    shop_list = "\n\n".join(f"نام محصول: {key} , قیمت: {value}" for key, value in bots_price.items() if
                                            key in context.user_data.get("shoplist"))
                    context.user_data["paylist"] = await context.bot.edit_message_text(chat_id=chat_id,
                                                    message_id=context.user_data.get("paylist").message_id,text=f"""سبد خرید🛒
نام کاربری: 

سفارشات 🤖:

{shop_list}

ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
قیمت کل: {reduce(lambda x,y:x+y,[key for bot , key in bots_price.items() if bot in context.user_data.get("shoplist")])}
قابل پرداخت: {reduce(lambda x,y:x+y,[key for bot , key in bots_price.items() if bot in context.user_data.get("shoplist")])}""" )
                except Exception as e:
                    print(f"error, caused{e}")
            print(context.user_data.get("shoplist"))

# message handler
async def message_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    bots = {"WELCOME_BOT":69000,
     "LOTTERY_COMMENT":150000,
     "MENTIONS_ANSWER":90000,
     "GETUSER_INFO":150000,
     "STORY_REMINDER":69000,
     "DEFAULT_DIRECT":150000,
     "COMMENT_DIRECT":100000,
     "STORYREP_DIRECT":100000}

    if text == "بازگشت🔙":
        if context.user_data.get("show_pros"):
            context.user_data["show_pros"] = False

            message_ids = context.user_data.values().mapping["seebots"]["message_ids"]
            reversed_message_ids = list(reversed(message_ids))
            for message_id in reversed_message_ids:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                context.user_data.values().mapping["seebots"]["message_ids"].pop()
            await context.bot.delete_message(chat_id=chat_id,
                                             message_id=context.user_data.get("list_text").message_id)
            keyboards = [
                ["🤖ربات ها🤖"],
                ["حساب کاربری📗", "ربات های من🤖"],
                ["سبد خرید🛒", "پشتیبانی👩‍💻"],
                ["راهنما📖", "تخفیف❤️", "قوانین و مقررات📙"],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboards)
            await context.bot.send_message(chat_id=chat_id,
                                           text="جانم چه کاری برات انجام بدم؟",
                                           reply_markup=reply_markup)
        else:
            keyboards = [
                ["🤖ربات ها🤖"],
                ["حساب کاربری📗", "ربات های من🤖"],
                ["سبد خرید🛒", "پشتیبانی👩‍💻"],
                ["راهنما📖", "تخفیف❤️", "قوانین و مقررات📙"],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboards)
            await context.bot.send_message(chat_id=chat_id,
                                           text="جانم چه کاری برات انجام بدم؟",
                                           reply_markup=reply_markup)
    elif text == "🤖ربات ها🤖":
        await see_insta_bots(update,context)
    elif text == "سبد خرید🛒":
        if context.user_data.get("shoplist"):
            shop_list =  "\n\n".join(f"نام محصول: {key} , قیمت: {value}" for key, value in bots.items() if key in context.user_data.get("shoplist"))
            print(f"shop list = {shop_list}")
            context.user_data["paylist"] = await context.bot.send_message(chat_id=chat_id, text=f"""سبد خرید🛒
نام کاربری: 

سفارشات 🤖:

{shop_list}

ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
قیمت کل: {reduce(lambda x,y:x+y,[key for bot , key in bots.items() if bot in context.user_data.get("shoplist")])}
قابل پرداخت: {reduce(lambda x,y:x+y,[key for bot , key in bots.items() if bot in context.user_data.get("shoplist")])}""")
        else:
            await context.bot.send_message(chat_id=chat_id,text="سبد خرید خالی است❌")
    elif text == "ربات های من🤖":
        await mybots(update,context)
    elif text == "پشتیبانی👩‍💻":
        await backup(update,context)
    elif text == "راهنما📖":
        await help_command(update,context)
    elif text == "قوانین و مقررات📙":
        await laws(update,context)
    elif text == "تخفیف❤️":
        await off(update,context)


if "__main__" == __name__:
    print("starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("users", bot_members))
   # app.add_handler(CommandHandler("admin", admin_command))
   # app.add_handler(CommandHandler("check", check_send_messages))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))


    print("polling...")
    app.run_polling()

