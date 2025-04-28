from mfrc522 import BasicMFRC522
import time

reader = BasicMFRC522()


print("[*] Готов к работе (Ctrl-C для выхода)")
last = None                 # запомним предыдущий UID

while True:
    uid = reader.read_id_no_block()
    if uid and uid != last: # новый UID
        print(uid)
        last = uid
        # маленький «дебаунс», чтобы не печатать сотни строк в секунду
        time.sleep(0.15)
    elif uid is None:
        last = None         # карта убрана — ждём новую
    time.sleep(0.02)        # 50 опросов-в-секунду