import psutil
import os
import time

warning_leval = 25
critical_leval = 15

sound = "sounds/alert.wav"

def notify(message, batter_leval, urgency):
    os.system(
        f'notify-send "{message} {int(batter_leval)}%" -u {urgency} -i "🔋"')


if __name__ == "__main__":
    has_notifyed = False
    notifyed_critical = False
    while True:
        battery_leval = int(psutil.sensors_battery().percent)
        is_charging = psutil.sensors_battery().power_plugged

        if not is_charging:

            if battery_leval <= critical_leval:
                if not notifyed_critical:
                    notify("Battery Leval Critical", battery_leval, "critical")
                    notifyed_critical = True
                    os.system(f"paplay {sound}")

            else:
                if not has_notifyed:
                    if battery_leval <= warning_leval:
                        notify("Battery Leval Low", battery_leval, "normal")
                        has_notifyed = True
                        os.system(f"paplay {sound}")

                    else:
                        pass
                else:
                    pass

        else:
            has_notifyed = False
            notifyed_critical = False

        time.sleep(60)
