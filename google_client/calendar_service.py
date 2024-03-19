from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from datetime import datetime 

# GoogleEventCreate
class GoogleCalendarService():

    # put list of params here like the calendar url etc..

    
    def __init__(self, access_token):
        self.access_token = access_token
        
        creds = Credentials(access_token)
        self.service = build('calendar', 'v3', credentials=creds)

    # Function to clean up any time that might not have the trailing/pre 0 => let the user deal with this we need to know exactly what they want 
    # def time_cleanup(self, time):
    #     if ":" in time:
    #         return 


    def list_calendars(self, user):
        print("Fetching all calendars:")
        calendar_list = self.service.calendarList().list().execute().get('items', [])
        for calendar in calendar_list:
            print(calendar['summary'])


    # get timezone from user browser and pass it here
    def create_event(self, task):
        start_time = list(map(int, task['start_time'].split(":")))
        end_time = list(map(int, task['end_time'].split(":")))
        google_event = {
            'summary': task['task_name'],
            'start': {
                'dateTime': datetime.today().replace(hour=start_time[0], minute=start_time[1]).isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': datetime.today().replace(hour=end_time[0], minute=end_time[1]).isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 5},
                ],
            },

        }
        
        created_event = self.service.events().insert(calendarId="primary", body=google_event).execute()
        print(f"Created event: {created_event['id']}")


    def create_events(self, events):
        # Takes in list of events and creates them => at this point we should be sure that we can create them all: frontend has done all the input checking and serialization
        created_events = events.map(self.create_event, events)

        return created_events