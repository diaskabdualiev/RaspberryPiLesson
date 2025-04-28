import time
import board
import busio
import digitalio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация ADS1115
ads = ADS.ADS1115(i2c)

# Настройка каналов для осей X и Y джойстика
# ADS1115 имеет 4 аналоговых входа (A0-A3)
x_channel = AnalogIn(ads, ADS.P0)  # Ось X подключена к A0
y_channel = AnalogIn(ads, ADS.P1)  # Ось Y подключена к A1

# Кнопка джойстика подключена к GPIO пину
button = digitalio.DigitalInOut(board.D17)  # Кнопка на GPIO17
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Подтяжка к питанию (кнопка замыкает на GND)

# Функция для преобразования данных АЦП в проценты
def map_to_percent(value, in_min, in_max):
    return int((value - in_min) * 100 / (in_max - in_min))

# Основной цикл
try:
    # Сначала считываем несколько значений для определения центральной позиции
    x_values = []
    y_values = []

    print("Калибровка джойстика...")
    print("Пожалуйста, оставьте джойстик в центральном положении")

    for _ in range(10):
        x_values.append(x_channel.value)
        y_values.append(y_channel.value)
        time.sleep(0.1)

    # Вычисляем средние значения для определения "центра"
    x_center = sum(x_values) // len(x_values)
    y_center = sum(y_values) // len(y_values)

    # Определяем предположительные минимумы и максимумы
    # (могут потребовать коррекции в зависимости от вашей модели джойстика)
    x_min = x_center - 10000
    x_max = x_center + 10000
    y_min = y_center - 10000
    y_max = y_center + 10000

    print(f"Калибровка завершена: X центр = {x_center}, Y центр = {y_center}")
    print("Начинаем считывание джойстика. Нажмите Ctrl+C для выхода.")
    print()

    while True:
        # Считываем значения с джойстика
        x_value = x_channel.value
        y_value = y_channel.value
        button_pressed = not button.value  # Инвертируем, так как кнопка подтянута к VCC

        # Преобразуем значения в проценты от -100% до 100%
        x_percent = map_to_percent(x_value, x_min, x_max) - 50
        y_percent = map_to_percent(y_value, y_min, y_max) - 50

        # Ограничиваем значения в пределах -100% до 100%
        x_percent = max(-100, min(100, x_percent * 2))
        y_percent = max(-100, min(100, y_percent * 2))

        # Определяем направление
        direction = "Центр"
        if abs(x_percent) > 10 or abs(y_percent) > 10:  # Учитываем небольшую мертвую зону
            if abs(x_percent) > abs(y_percent):
                direction = "Вправо" if x_percent > 0 else "Влево"
            else:
                direction = "Вверх" if y_percent < 0 else "Вниз"

        # Выводим информацию
        print(f"X: {x_percent:4d}%, Y: {y_percent:4d}%, Направление: {direction:6s}, Кнопка: {'Нажата' if button_pressed else 'Отжата'}")

        time.sleep(0.2)  # Задержка для снижения частоты обновления

except KeyboardInterrupt:
    print("\nПрограмма завершена.")