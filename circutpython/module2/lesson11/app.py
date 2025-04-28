from flask import Flask, render_template, jsonify
import time
import board
import digitalio
import threading

app = Flask(__name__)

# Инициализация выводов энкодера
# Выходы A и B энкодера подключены к GPIO17 и GPIO18 соответственно
pin_a = digitalio.DigitalInOut(board.D17)
pin_b = digitalio.DigitalInOut(board.D18)
pin_a.direction = digitalio.Direction.INPUT
pin_b.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP  # Подтяжка к питанию
pin_b.pull = digitalio.Pull.UP  # Подтяжка к питанию

# Инициализация кнопки энкодера
button = digitalio.DigitalInOut(board.D27)  # Кнопка на GPIO27
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Подтяжка к VCC (кнопка замыкает на GND)

# Глобальные переменные для хранения состояния
counter = 0
button_state = False
last_button_state = False
last_a_state = pin_a.value
last_direction = ""
events = []  # для хранения истории событий

# Блокировка для многопоточного доступа
lock = threading.Lock()

# Функция для опроса энкодера в отдельном потоке
def encoder_polling():
    global counter, button_state, last_button_state, last_a_state, last_direction, events
    
    try:
        print("Роторный энкодер: поворачивайте ручку или нажмите на нее")
        
        while True:
            with lock:
                # Считываем текущее состояние выводов энкодера
                a_state = pin_a.value
                b_state = pin_b.value
                
                # Если состояние вывода A изменилось, значит произошло вращение
                if a_state != last_a_state:
                    # Определяем направление вращения сравнивая состояния выводов A и B
                    if b_state != a_state:
                        direction = "по часовой стрелке"
                        counter += 1
                    else:
                        direction = "против часовой стрелки"
                        counter -= 1
                    
                    # Сохраняем направление и добавляем событие
                    last_direction = direction
                    events.append(f"Вращение {direction}, Счетчик: {counter}")
                    # Ограничиваем историю событий до 10
                    if len(events) > 10:
                        events = events[-10:]
                
                # Обновляем последнее состояние вывода A
                last_a_state = a_state
                
                # Обработка нажатия кнопки
                button_state = not button.value  # Инвертируем значение
                
                # Проверяем изменение состояния кнопки (обнаружение фронта)
                if button_state and not last_button_state:
                    events.append(f"Кнопка нажата! Сброс счетчика с {counter} на 0")
                    counter = 0
                
                # Обновляем последнее состояние кнопки
                last_button_state = button_state
            
            # Небольшая задержка для стабилизации
            time.sleep(0.01)
            
    except Exception as e:
        print(f"Ошибка в потоке опроса энкодера: {e}")

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# API для получения текущего состояния энкодера
@app.route('/api/encoder-state')
def encoder_state():
    with lock:
        return jsonify({
            'counter': counter,
            'button_state': button_state,
            'last_direction': last_direction,
            'events': events
        })

# Запуск потока опроса энкодера
def start_encoder_thread():
    encoder_thread = threading.Thread(target=encoder_polling, daemon=True)
    encoder_thread.start()

if __name__ == '__main__':
    # Запускаем поток для опроса энкодера
    start_encoder_thread()
    
    # Запускаем веб-сервер Flask
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)