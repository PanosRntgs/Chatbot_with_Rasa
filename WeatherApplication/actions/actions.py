from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.latest_message['text']
        weather_data = self.get_weather(city)
        print(f"City: {city}")
        print(f"Weather Data: {weather_data}")

        if weather_data:
            response = f"The weather in {city} is {weather_data['main']['temp']} C with {weather_data['weather'][0]['description']} "
        else:
            response = f"Sorry, I can't find the weather data for {city}, please try again"

        dispatcher.utter_message(text=response)

        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        api_key = "f3991d45f79cd222c658dd2fd58210b7"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "units": "metric",
            "appid": api_key
        }

        try:
            print(f"API URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            api_response = response.json()
            print(f"API Response: {api_response}")
            return api_response

        except requests.exceptions.RequestException as error:
            print(f"API Requests Error: {error}")
            return None



