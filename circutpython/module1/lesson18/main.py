import board, busio, digitalio
from adafruit_pn532.i2c import PN532_I2C

# I2C-шина и пин reset
i2c   = busio.I2C(board.SCL, board.SDA)
reset = digitalio.DigitalInOut(board.D25)

pn532 = PN532_I2C(i2c, debug=False, reset=reset)

ic, ver, rev, support = pn532.firmware_version
print(f"PN532 v{ver}.{rev} — IC 0x{ic:x}")

pn532.SAM_configuration()          # включаем чтение карт
print("Поднесите NFC-метку…")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid:
        print("Найдена карта, UID:", uid.hex())