import time
import board
import busio
import adafruit_mpu6050
import math

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация MPU6050
mpu = adafruit_mpu6050.MPU6050(i2c)

# Установка диапазонов измерения (опционально)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_2_G  # ±2g
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_250_DPS  # ±250 °/s

# Функция для расчета угла наклона из данных акселерометра
def calculate_tilt_angles(x, y, z):
    # Конвертируем значения акселерометра в углы наклона (в градусах)
    # используя тригонометрические формулы
    roll = math.atan2(y, z) * 180 / math.pi
    pitch = math.atan2(-x, math.sqrt(y*y + z*z)) * 180 / math.pi
    return roll, pitch

# Основной цикл
try:
    print("MPU6050 готов к работе!")
    print("Перемещайте датчик для изменения значений")
    print("Нажмите Ctrl+C для выхода")
    print()

    while True:
        # Считываем данные с акселерометра (g)
        acceleration = mpu.acceleration

        # Считываем данные с гироскопа (град/с)
        gyro = mpu.gyro

        # Считываем температуру (°C)
        temperature = mpu.temperature

        # Вычисляем углы наклона
        roll, pitch = calculate_tilt_angles(acceleration[0], acceleration[1], acceleration[2])

        # Выводим данные в консоль
        print("Акселерометр (м/с²): X={:5.2f}, Y={:5.2f}, Z={:5.2f}".format(
            acceleration[0], acceleration[1], acceleration[2]))

        print("Гироскоп (°/с):       X={:5.2f}, Y={:5.2f}, Z={:5.2f}".format(
            gyro[0], gyro[1], gyro[2]))

        print("Углы наклона (°):     Roll={:5.2f}, Pitch={:5.2f}".format(
            roll, pitch))

        print("Температура: {:.2f} °C".format(temperature))
        print("-" * 50)

        # Задержка для наглядности вывода
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nПрограмма завершена.")