import time
import board
import digitalio

# Инициализация пина GPIO18 как выход для управления реле
relay = digitalio.DigitalInOut(board.D18)
relay.direction = digitalio.Direction.OUTPUT

# Некоторые модули реле активируются при LOW (инверсная логика)
# Для таких модулей используйте False для включения, True для выключения

try:
    while True:
        print("Реле ВКЛ (цепь замкнута)")
        relay.value = False  # активное низкое (LOW) - для многих модулей
        time.sleep(2)

        print("Реле ВЫКЛ (цепь разомкнута)")
        relay.value = True   # неактивное (HIGH)
        time.sleep(2)

        # Если ваш модуль имеет прямую логику (активация HIGH),
        # замените строки выше на:
        # relay.value = True   # активное высокое (HIGH)
        # relay.value = False  # неактивное (LOW)

except KeyboardInterrupt:
    print("\nПрограмма завершена.")
    # Отключаем реле перед выходом (безопасное состояние)
    relay.value = True