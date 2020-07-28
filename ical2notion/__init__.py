#! /usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import requests
from ics import Calendar, Event
from notion.client import NotionClient
from notion.collection import NotionDate
import click

@click.command()
@click.argument(
        "database",
)
@click.argument(
        "token",
)
@click.argument(
        "icals",
        nargs=-1,
)
def ical2notion(database, token, icals):
    """Google calendar to notion made simple."""
    # Check that the user supplied all the arguments
    if not database:
        click.echo("Please supply a notion database link")
        exit()
    if not token:
        click.echo("Please supply a notion token")
    if not icals:
        click.echo("Please supply one or more ical links")


    # Download the users ical files and get all events
    events = []
    for url in icals:
        c = Calendar(requests.get(url).text)
        events += list(c.timeline) #

    events = [e for e in events if e > Event(begin=datetime.now())]

    # Authenticate with notion
    client = NotionClient(token_v2=token)

    # Add each event to the notion database
    gcal_table = client.get_collection_view(database)


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

if __name__ == "__main__":
    ical2notion()

