import psutil
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv("DB_PATH")
print(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()
cur = conn.cursor()

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

def getNotifyStatus(name):
    try:
        query = cur.execute(f"SELECT bool FROM notify WHERE name = '{name}';") 
        conn.commit()
        value = query.fetchone()[0]  
        return value
    except:
        return "query failed"
     
def updateNotifyed(name, bit):
    try:
        cur.execute(f"UPDATE notify SET bool = {bit} WHERE name = '{name}';")
        conn.commit()
        return "query executed"
    except:
        return "query failed"

def reset():
    updateNotifyed("normal", 0)
    updateNotifyed("critical", 0)


if __name__ == "__main__":  
    if not is_charging:
        
        print(getNotifyStatus("normal"))
        if battery_leval <= warning_leval and getNotifyStatus("normal") == 0:  
            try:
                notify("Battery Leval Low", battery_leval, "normal")
                # playSound()
                print(getNotifyStatus("normal"))
                updateNotifyed("normal", 1)
            except:
                print("Failed to execute")

        if battery_leval <= critical_leval and getNotifyStatus("critical") == 0:   
            try: 
                notify("Battery Leval Critical", battery_leval, "critical")
                # playSound()
                updateNotifyed("critical", 1)
            except: 
               print("Failed to execute") 

    else:
        try:
            reset()
        except:
            print("query Failed")
