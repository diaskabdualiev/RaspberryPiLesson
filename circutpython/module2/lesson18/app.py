from flask import Flask, render_template, jsonify
import board
import busio
import digitalio
import threading
import time
from adafruit_pn532.i2c import PN532_I2C

app = Flask(__name__)

# Глобальные переменные для хранения данных с NFC
last_uid = None
is_running = True

# Инициализация PN532
def init_pn532():
    try:
        # I2C-шина и пин reset
        i2c = busio.I2C(board.SCL, board.SDA)
        reset = digitalio.DigitalInOut(board.D25)
        
        # Создаем объект PN532
        pn532 = PN532_I2C(i2c, debug=False, reset=reset)
        
        # Выводим информацию о версии прошивки
        ic, ver, rev, support = pn532.firmware_version
        print(f"PN532 v{ver}.{rev} — IC 0x{ic:x}")
        
        # Включаем чтение карт
        pn532.SAM_configuration()
        
        return pn532
    except Exception as e:
        print(f"Ошибка инициализации PN532: {e}")
        return None

# Функция для считывания NFC в отдельном потоке
def read_nfc():
    global last_uid, is_running
    
    # Инициализируем PN532
    pn532 = init_pn532()
    if not pn532:
        print("Не удалось инициализировать PN532, завершение работы")
        return
    
    print("Поднесите NFC-метку...")
    
    # Основной цикл сканирования
    while is_running:
        try:
            # Пытаемся считать NFC метку
            uid = pn532.read_passive_target(timeout=0.5)
            
            if uid:
                uid_hex = uid.hex()
                print(f"Найдена карта, UID: {uid_hex}")
                last_uid = uid_hex
                
                # Небольшая задержка, чтобы избежать повторного считывания
                time.sleep(0.5)
        except Exception as e:
            print(f"Ошибка при считывании NFC: {e}")
            time.sleep(1)

# Запускаем поток считывания NFC
nfc_thread = threading.Thread(target=read_nfc)
nfc_thread.daemon = True
nfc_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_uid')
def get_uid():
    return jsonify({'uid': last_uid})

if __name__ == '__main__':
    try:
        print("NFC веб-приложение запущено")
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("Программа остановлена")
        is_running = False