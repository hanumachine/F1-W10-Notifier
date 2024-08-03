from win10toast import ToastNotifier
import requests
import json
from time import sleep
from datetime import datetime, time, timezone

userminutes = 60
timer = 300

toaster = ToastNotifier()
API_URL = "http://ergast.com/api/f1/current.json"

def check_events():
    response = requests.get(API_URL)
    response_json = json.loads(response.text)
    
    now = datetime.now(timezone.utc)
    races = response_json['MRData']['RaceTable']['Races']

    for race in races:
        race_date = datetime.fromisoformat(race['date'])
        race_time = time.fromisoformat(race['time']) 
        race_event =  datetime.combine(race_date, race_time)

    if race_event.timestamp() > now.timestamp() and race_event.timestamp() - now.timestamp() <= userminutes and race_event.timestamp() - now.timestamp() >= (userminutes*60-timer):
         toaster.show_toast("F1 Notifier",
                f"'{(race['raceName'])}' is happening in around [{(race_event.timestamp() - now.timestamp())}].",
                icon_path=None,
                duration=5,
                threaded=True)

def main():
    while True:
        check_events()
        sleep(timer)

if __name__ == "__main__":
    main()
