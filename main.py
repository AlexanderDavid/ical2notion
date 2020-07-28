import config
from datetime import datetime
from datetime import timedelta
import requests
from ics import Calendar, Event
from notion.client import NotionClient
from notion.collection import NotionDate

# Check that the user has updated the config file
if config.notion_page is None or config.gcal_icals == [] or config.notion_token is None:
    print("Please populate config.py")
    exit()

# Download the users ical files and get all events
events = []
for url in config.gcal_icals:
    c = Calendar(requests.get(url).text)
    events += list(c.timeline) #

events = [e for e in events if e > Event(begin=datetime.now())]

# Authenticate with notion
client = NotionClient(token_v2=config.notion_token)

# Add each event to the notion database
gcal_table = client.get_collection_view(config.notion_page)

def add_or_update(row, event):
    row.uid = event.uid
    row.title = event.name
    row.description = event.description
    # Check if the event is an "All Day" these get messed up if we do a direct conversion
    if event.duration == timedelta(days=1):
        row.date = NotionDate((event.begin))
    else:
        row.date = NotionDate(datetime.fromisoformat(str(event.begin)),
                              datetime.fromisoformat(str(event.end)))
    row.location = event.location

for event in events:
    # Check that it isn't in there
    cont = True
    for row in gcal_table.collection.get_rows():
        if row.uid == event.uid:
            add_or_update(row, event)
            cont = False
            break
    if cont:
        row = gcal_table.collection.add_row()
        add_or_update(row, event)

