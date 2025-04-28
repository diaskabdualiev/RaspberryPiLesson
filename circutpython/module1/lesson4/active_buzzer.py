import board
import digitalio
import time

# Настройка пина для активного зуммера
buzzer_pin = digitalio.DigitalInOut(board.D18)  # GPIO18
buzzer_pin.direction = digitalio.Direction.OUTPUT

def beep(duration):
    """Функция для подачи звукового сигнала заданной длительности."""
    buzzer_pin.value = True
    print("Зуммер ВКЛ")
    time.sleep(duration)
    buzzer_pin.value = False
    print("Зуммер ВЫКЛ")

try:
    print("Программа управления активным зуммером запущена")
    print("Нажмите Ctrl+C для завершения")

    while True:
        # Один короткий сигнал
        beep(0.2)
        time.sleep(0.2)

        # Два коротких сигнала
        beep(0.2)
        time.sleep(0.2)
        beep(0.2)
        time.sleep(0.2)

        # Один длинный сигнал
        beep(1.0)
        time.sleep(1.0)

except KeyboardInterrupt:
    # Выключаем зуммер при завершении
    buzzer_pin.value = False
    print("\nПрограмма завершена")