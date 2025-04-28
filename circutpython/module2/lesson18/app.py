from flask import Flask, render_template, request, jsonify
from mfrc522 import BasicMFRC522
import threading
import time

app = Flask(__name__)

# Создаем объект считывателя
reader = BasicMFRC522()

# Глобальные переменные для хранения данных
last_uid = None
is_running = True

# Функция для фонового считывания карты
def read_rfid():
    global last_uid, is_running
    last = None
    
    while is_running:
        uid = reader.read_id_no_block()
        if uid and uid != last:  # новый UID
            print(f"Считан UID: {uid}")
            last_uid = uid
            last = uid
            time.sleep(0.15)  # дебаунс
        elif uid is None:
            last = None  # карта убрана — ждём новую
        time.sleep(0.02)  # 50 опросов в секунду

# Запускаем фоновый поток для считывания
read_thread = threading.Thread(target=read_rfid)
read_thread.daemon = True
read_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_uid')
def get_uid():
    return jsonify({'uid': last_uid})

# Маршрут для сохранения введенного UID
@app.route('/save_uid', methods=['POST'])
def save_uid():
    global last_uid
    data = request.get_json()
    last_uid = data.get('uid')
    return jsonify({'success': True, 'uid': last_uid})

if __name__ == '__main__':
    try:
        print("[*] RFID веб-приложение запущено (Ctrl-C для выхода)")
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("[*] Программа остановлена")
        is_running = False  # Останавливаем фоновый поток