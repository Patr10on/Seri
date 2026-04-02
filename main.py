import os
import time
import threading
import schedule
import telebot
from dotenv import load_dotenv
from core.tiktok import send_streak, send_streak_mock

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN)


def auth_only(func):
    def wrapper(message):
        if message.chat.id != ADMIN_CHAT_ID:
            return
        func(message)
    return wrapper


def run_streak_and_notify():
    bot.send_message(ADMIN_CHAT_ID, "⏳ Seri gönderiliyor...")
    success, detail = send_streak()
    if success:
        bot.send_message(ADMIN_CHAT_ID, f"✅ {detail}")
    else:
        bot.send_message(ADMIN_CHAT_ID, f"❌ Hata:\n{detail}")
        try:
            with open("screenshot_error.png", "rb") as img:
                bot.send_photo(ADMIN_CHAT_ID, img, caption="Hata ekran görüntüsü")
        except FileNotFoundError:
            pass


@bot.message_handler(commands=["seri"])
@auth_only
def cmd_seri(message):
    t = threading.Thread(target=run_streak_and_notify)
    t.daemon = True
    t.start()


@bot.message_handler(commands=["durum"])
@auth_only
def cmd_durum(message):
    start = time.time()
    elapsed = round((time.time() - start) * 1000, 2)
    bot.reply_to(message, f"🟢 Sistem aktif, ping: {elapsed} ms")


@bot.message_handler(commands=["test"])
@auth_only
def cmd_test(message):
    success, detail = send_streak_mock()
    bot.reply_to(message, f"🧪 Test sonucu:\n{detail}")


def scheduler_loop():
    schedule.every().day.at("00:01").do(run_streak_and_notify)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    sched_thread = threading.Thread(target=scheduler_loop)
    sched_thread.daemon = True
    sched_thread.start()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
