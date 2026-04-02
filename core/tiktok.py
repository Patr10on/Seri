import os
from dotenv import load_dotenv

load_dotenv()

TARGET_USER = os.getenv("TARGET_USERNAME")


def send_streak_mock() -> tuple[bool, str]:
    return True, f"MOCK: @{TARGET_USER} kullanıcısına mesaj gönderildi (Playwright tetiklenmedi)"


def send_streak() -> tuple[bool, str]:
    return False, "Playwright Termux'ta desteklenmiyor. VPS gerekli."
