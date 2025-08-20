import requests
import time
import os

# ضع التوكن و chat_id الخاص بك هنا
BOT_TOKEN = "5004504482:AAHnUZO85qogytwBhBbqvIfdgkUR6YQDgio"
CHAT_ID = "1164267189"

# رابط الملف الذي تريد فحصه
UID_LOG_URL = "http://try-if-you-can-she5.mypressonline.com/UID-LOG.txt"

# ملف لحفظ الـUIDs التي تم إرسالها مسبقاً
SEEN_FILE = "seen_uids.txt"


def load_seen_uids():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)


def save_seen_uids(uids):
    with open(SEEN_FILE, "w") as f:
        for uid in uids:
            f.write(uid + "\n")


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)


def check_new_uids():
    seen = load_seen_uids()
    try:
        response = requests.get(UID_LOG_URL)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
    except Exception as e:
        print("خطأ عند قراءة الرابط:", e)
        return

    new_seen = set(seen)
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            uid = parts[0]
            ip = parts[1]
            code = parts[2]
            if uid not in seen:
                msg = f"📌 UID جديد\nUID: {uid}\nIP: {ip}\nCode: {code}"
                send_to_telegram(msg)
                new_seen.add(uid)

    save_seen_uids(new_seen)


if __name__ == "__main__":
    check_new_uids()