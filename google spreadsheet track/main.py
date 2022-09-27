from datetime import datetime
import os
import requests


NT_APP_ID = os.environ.get("NT_APP_ID")
NT_API_KEY = os.environ.get("NT_API_KEY")
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
GENDER = "female"
WEIGHT_KG = 60
HEIGHT_CM = 167
AGE = 30

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/310e1a81e64941e795109e5f52ba51ca/workoutTracking/sheet1"
exercise_text = input("Tell me which exercises you did: ")
header = {
    "x-app-id": NT_APP_ID,
    "x-app-key": NT_API_KEY,
    "Content-Type": "application/json"
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=header)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_body = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint,
                                   json=sheet_body,
                                   headers={
                                       "Authorization": f"Basic {SHEETY_TOKEN}"
                                   })
    print(sheet_response.text)
