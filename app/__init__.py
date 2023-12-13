import psutil
import sqlite3
import os

conn = sqlite3.connect("needsCharged.db")
c = conn.cursor()

warning_leval = 1000
critical_leval = 1000

battery_leval = int(psutil.sensors_battery().percent)
is_charging = psutil.sensors_battery().power_plugged


def playSound():
    sound = "../sounds/alert.wav"
    os.system(f"paplay {sound}")


def notify(message, batter_leval, urgency):
    os.system(
        f'notify-send "{message} {int(batter_leval)}%" -u {urgency} -i "🔋"')

if __name__ == "__main__": 
    if not is_charging:

            if battery_leval <= warning_leval:
                notify("Battery Leval Low", battery_leval, "normal")
                playSound()

            if battery_leval <= critical_leval:
                notify("Battery Leval Critical", battery_leval, "critical")
                playSound()
