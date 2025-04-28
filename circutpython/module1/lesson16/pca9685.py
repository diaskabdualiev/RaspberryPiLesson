import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация PCA9685
pca = PCA9685(i2c)

# Установка частоты ШИМ (50 Гц для большинства сервоприводов)
pca.frequency = 50

# Создаем объект сервопривода (используем канал 0)
servo_motor = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)

# Демонстрация последовательного движения
def sequential_movement():
    print("Последовательное движение сервопривода...")
    
    print("Сервопривод: поворот на 0°")
    servo_motor.angle = 0
    time.sleep(0.5)
    
    print("Сервопривод: поворот на 90°")
    servo_motor.angle = 90
    time.sleep(0.5)
    
    print("Сервопривод: поворот на 180°")
    servo_motor.angle = 180
    time.sleep(0.5)
    
    print("Сервопривод: возврат на 90°")
    servo_motor.angle = 90
    time.sleep(0.5)

# Демонстрация плавного движения
def smooth_movement():
    print("Плавное движение сервопривода...")
    
    # Установка сервопривода в начальное положение
    servo_motor.angle = 0
    time.sleep(1)
    
    # Плавное движение сервопривода от 0° до 180°
    for angle in range(0, 181, 5):
        servo_motor.angle = angle
        print(f"Угол: {angle}°")
        time.sleep(0.05)
    
    # Пауза в конечном положении
    time.sleep(1)
    
    # Плавное движение сервопривода от 180° до 0°
    for angle in range(180, -1, -5):
        servo_motor.angle = angle
        print(f"Угол: {angle}°")
        time.sleep(0.05)

# Демонстрация повторяющегося движения
def oscillating_movement():
    print("Повторяющееся движение сервопривода...")
    for _ in range(5):  # Повторить 5 раз
        servo_motor.angle = 150
        time.sleep(0.3)
        servo_motor.angle = 30
        time.sleep(0.3)

# Основной цикл
try:
    print("PCA9685 готов к работе!")
    print("Демонстрация различных типов движения сервопривода")
    
    # Устанавливаем сервопривод в нейтральное положение
    servo_motor.angle = 90
    time.sleep(1)
    
    # Демонстрация различных типов движения
    sequential_movement()
    time.sleep(1)
    
    smooth_movement()
    time.sleep(1)
    
    oscillating_movement()
    time.sleep(1)
    
    # Возвращаем сервопривод в нейтральное положение
    print("Возврат в нейтральное положение...")
    servo_motor.angle = 90
    
    print("Демонстрация завершена!")

except KeyboardInterrupt:
    # Перед выходом устанавливаем сервопривод в безопасное положение
    servo_motor.angle = 90
    print("\nПрограмма завершена.")