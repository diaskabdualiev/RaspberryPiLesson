from RPLCD.i2c import CharLCD
import time

# Создаем объект LCD
# i2c_expander - тип I2C экспандера (обычно 'PCF8574')
# address - I2C адрес (обычно 0x27 или 0x3F)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8)

# Очищаем дисплей
lcd.clear()

# Выводим текст
lcd.write_string('helloworld')
lcd.cursor_pos = (1, 0)  # Переходим на вторую строку
lcd.write_string('Raspberry Pi 5')

# Ждем некоторое время
time.sleep(5)

# Очищаем дисплей перед выходом
lcd.clear()