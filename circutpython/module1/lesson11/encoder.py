import board
import digitalio
import time
from adafruit_debouncer import Debouncer

# Настройка контактов энкодера
pin_clk = digitalio.DigitalInOut(board.D17)  # CLK
pin_dt = digitalio.DigitalInOut(board.D18)   # DT
pin_clk.direction = digitalio.Direction.INPUT
pin_dt.direction = digitalio.Direction.INPUT
pin_clk.pull = digitalio.Pull.UP
pin_dt.pull = digitalio.Pull.UP

# Настройка кнопки с debouncer
pin_sw = digitalio.DigitalInOut(board.D27)  # SW
pin_sw.direction = digitalio.Direction.INPUT
pin_sw.pull = digitalio.Pull.UP
button = Debouncer(pin_sw)

# Глобальные переменные
global_counter = 0
clk_last_state = pin_clk.value

try:
    print("Энкодер инициализирован. Начните вращать его...")
    
    while True:
        # Обработка энкодера
        clk_state = pin_clk.value
        dt_state = pin_dt.value
        
        # Если состояние CLK изменилось, значит произошло вращение
        if clk_state != clk_last_state:
            # Если DT отличается от CLK, значит вращение по часовой стрелке
            if dt_state != clk_state:
                global_counter += 1
            else:
                global_counter -= 1
                
            print('Global Counter =', global_counter)
            
        clk_last_state = clk_state
        
        # Обработка кнопки с debounce
        button.update()
        if button.fell:  # Кнопка была нажата (изменение с HIGH на LOW из-за подтяжки)
            global_counter = 0
            print('Counter reset')
        
        # Небольшая задержка для стабильности
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("Программа остановлена")