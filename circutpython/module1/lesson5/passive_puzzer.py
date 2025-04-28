import board
import pwmio
import time

# Настройка пина для пассивного зуммера с использованием PWM
buzzer = pwmio.PWMOut(board.D18, frequency=440, duty_cycle=0)

# Словарь нот и их частот в Гц
NOTES = {
    'C4': 262,  # До четвертой октавы
    'D4': 294,  # Ре
    'E4': 330,  # Ми
    'F4': 349,  # Фа
    'G4': 392,  # Соль
    'A4': 440,  # Ля
    'B4': 494,  # Си
    'C5': 523,  # До пятой октавы
    'REST': 0,  # Пауза
}

# Функция для проигрывания ноты заданной длительности
def play_note(note, duration):
    if note == 'REST':
        # Пауза - просто ждем
        buzzer.duty_cycle = 0
        time.sleep(duration)
    else:
        # Устанавливаем частоту ноты
        buzzer.frequency = NOTES[note]
        # Устанавливаем громкость (50% от максимальной)
        buzzer.duty_cycle = 32768  # 50% от 65535
        # Ждем заданную длительность
        time.sleep(duration)
        # Выключаем звук
        buzzer.duty_cycle = 0
        # Небольшая пауза между нотами
        time.sleep(0.05)

# Простая мелодия - "Маленькая звездочка" (Twinkle Twinkle Little Star)
MELODY = [
    ('C4', 0.3), ('C4', 0.3), ('G4', 0.3), ('G4', 0.3),
    ('A4', 0.3), ('A4', 0.3), ('G4', 0.6),
    ('F4', 0.3), ('F4', 0.3), ('E4', 0.3), ('E4', 0.3),
    ('D4', 0.3), ('D4', 0.3), ('C4', 0.6),
]

try:
    print("Воспроизведение мелодии на пассивном зуммере")
    print("Нажмите Ctrl+C для остановки")

    while True:
        # Воспроизводим мелодию
        for note, duration in MELODY:
            print(f"Играем ноту: {note}")
            play_note(note, duration)

        # Пауза перед повторением
        time.sleep(1)

except KeyboardInterrupt:
    # Выключаем зуммер при завершении
    buzzer.duty_cycle = 0
    print("\nПрограмма завершена")