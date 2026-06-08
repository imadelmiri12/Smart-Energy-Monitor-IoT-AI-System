from machine import Pin, I2C
import ssd1306
from time import sleep
import random
import network
import ujson
from umqtt.simple import MQTTClient

# =========================
# WIFI
# =========================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")

print("Connexion WiFi...")

while not wifi.isconnected():
    sleep(1)

print("WiFi connecté")
print(wifi.ifconfig())

# =========================
# MQTT
# =========================

BROKER = "broker.emqx.io"
TOPIC = b"home/energy/data"

client = MQTTClient(
    client_id="esp32-energy",
    server=BROKER
)

client.connect()
print("MQTT connecté")

# =========================
# OLED
# =========================

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# =========================
# INTERRUPTEURS
# =========================

swLamp = Pin(13, Pin.IN, Pin.PULL_UP)
swTV   = Pin(12, Pin.IN, Pin.PULL_UP)
swFan  = Pin(14, Pin.IN, Pin.PULL_UP)
swPC   = Pin(27, Pin.IN, Pin.PULL_UP)
swAC   = Pin(26, Pin.IN, Pin.PULL_UP)
swWM   = Pin(25, Pin.IN, Pin.PULL_UP)

# =========================
# LEDS
# =========================

ledLamp = Pin(15, Pin.OUT)
ledTV   = Pin(2, Pin.OUT)
ledFan  = Pin(4, Pin.OUT)
ledPC   = Pin(16, Pin.OUT)
ledAC   = Pin(17, Pin.OUT)
ledWM   = Pin(5, Pin.OUT)

print("Smart Energy System Started")

# =========================
# BOUCLE PRINCIPALE
# =========================

while True:

    lamp_on = not swLamp.value()
    tv_on   = not swTV.value()
    fan_on  = not swFan.value()
    pc_on   = not swPC.value()
    ac_on   = not swAC.value()
    wm_on   = not swWM.value()

    # LEDs
    ledLamp.value(lamp_on)
    ledTV.value(tv_on)
    ledFan.value(fan_on)
    ledPC.value(pc_on)
    ledAC.value(ac_on)
    ledWM.value(wm_on)

    # Consommation variable

    lamp_power = random.randint(8, 12) if lamp_on else 0
    tv_power   = random.randint(80, 180) if tv_on else 0
    fan_power  = random.randint(50, 100) if fan_on else 0
    pc_power   = random.randint(100, 300) if pc_on else 0
    ac_power   = random.randint(800, 1800) if ac_on else 0
    wm_power   = random.randint(500, 2000) if wm_on else 0

    total_power = (
        lamp_power +
        tv_power +
        fan_power +
        pc_power +
        ac_power +
        wm_power
    )

    # =========================
    # JSON MQTT
    # =========================

    payload = {
        "lamp": lamp_power,
        "tv": tv_power,
        "fan": fan_power,
        "pc": pc_power,
        "ac": ac_power,
        "wm": wm_power,
        "total": total_power
    }

    try:
        client.publish(
            TOPIC,
            ujson.dumps(payload)
        )
        print("MQTT envoyé")
    except Exception as e:
        print("Erreur MQTT:", e)

    # =========================
    # TERMINAL
    # =========================

    print("-----------------------------")
    print("Lampe      :", lamp_power, "W")
    print("TV         :", tv_power, "W")
    print("Ventilo    :", fan_power, "W")
    print("PC         :", pc_power, "W")
    print("Clim       :", ac_power, "W")
    print("Machine    :", wm_power, "W")
    print("TOTAL      :", total_power, "W")

    # =========================
    # OLED
    # =========================

    oled.fill(0)

    oled.text("SMART ENERGY", 0, 0)

    oled.text("L:" + str(lamp_power), 0, 12)
    oled.text("TV:" + str(tv_power), 64, 12)

    oled.text("F:" + str(fan_power), 0, 24)
    oled.text("PC:" + str(pc_power), 64, 24)

    oled.text("AC:" + str(ac_power), 0, 36)

    oled.text("TOT:" + str(total_power), 0, 54)

    oled.show()

    sleep(2)