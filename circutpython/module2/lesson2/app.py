from flask import Flask, render_template
import board
import digitalio

app = Flask(__name__)

# Функция для инициализации пина
def setup_led():
    led = digitalio.DigitalInOut(board.D18)
    led.direction = digitalio.Direction.OUTPUT
    return led

# Глобальная переменная для хранения состояния
led_state = False

@app.route('/')
def home():
    return render_template('index.html', status="LED выключен" if not led_state else "LED включен")

@app.route('/on')
def led_on():
    global led_state
    led = setup_led()
    led.value = True
    led_state = True
    led.deinit()  # Освобождаем GPIO
    return render_template('index.html', status="LED включен")

@app.route('/off')
def led_off():
    global led_state
    led = setup_led()
    led.value = False
    led_state = False
    led.deinit()  # Освобождаем GPIO
    return render_template('index.html', status="LED выключен")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)