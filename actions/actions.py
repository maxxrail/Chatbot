from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled
import datetime, requests

class ActionScheduleMeeting(Action):

    def name(self) -> Text:
        return "action_schedule_meeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        person = tracker.get_slot('person')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        topic = tracker.get_slot('topic')
        # Here, you would include logic to schedule the meeting
        dispatcher.utter_message(text=f"Meeting with {person} on {date} at {time} about {topic} has been scheduled.")
        return []

class ActionSetReminder(Action):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        reminder = tracker.get_slot('reminder')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        reminder_time = f"{date} {time}"
        reminder_datetime = datetime.datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S')

        dispatcher.utter_message(text=f"Reminder set for {reminder} on {date} at {time}.")

        return [ReminderScheduled(
            "action_remind_user",
            trigger_date_time=reminder_datetime,
            name="reminder",
            kill_on_user_message=False
        )]

class ActionRemindUser(Action):

    def name(self) -> Text:
        return "action_remind_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="This is your reminder.")
        return []

class ValidateReminderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reminder_form"

    def validate_date(self,
                      slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Logic to validate the date
        try:
            datetime.datetime.strptime(slot_value, '%Y-%m-%d')
            return {"date": slot_value}
        except ValueError:
            dispatcher.utter_message(text="The date format is incorrect. Please use YYYY-MM-DD.")
            return {"date": None}

    def validate_time(self,
                      slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Logic to validate the time
        try:
            datetime.datetime.strptime(slot_value, '%H:%M:%S')
            return {"time": slot_value}
        except ValueError:
            dispatcher.utter_message(text="The time format is incorrect. Please use HH:MM:SS.")
            return {"time": None}

class ActionGetCurrentTime(Action):

    def name(self) -> Text:
        return "action_get_current_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot('location')
        if not location:
            dispatcher.utter_message(text="Please provide a location to get the current time.")
            return []

        time_url = f"http://worldtimeapi.org/api/timezone/{location}"

        response = requests.get(time_url)
        if response.status_code == 200:
            time_data = response.json()
            current_time = time_data.get('datetime', 'Time not available')
            dispatcher.utter_message(text=f"The current time in {location} is {current_time}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve the time for that location.")

        return []

class ActionWebSearch(Action):

    def name(self) -> Text:
        return "action_web_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        query = tracker.get_slot('query')
        if not query:
            dispatcher.utter_message(text="I need a query to search for.")
            return []

        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query
        }

        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        if search_results['query']['search']:
            first_result = search_results['query']['search'][0]
            title = first_result['title']
            snippet = first_result['snippet']
            page_id = first_result['pageid']
            page_url = f"https://en.wikipedia.org/?curid={page_id}"
            response_text = f"Here's what I found on Wikipedia:\n\n{title}\n{snippet}...\nRead more: {page_url}"
        else:
            response_text = "Sorry, I couldn't find any information on that topic."

        dispatcher.utter_message(text=response_text)
        return []