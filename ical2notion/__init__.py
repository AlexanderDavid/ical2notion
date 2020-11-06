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
@click.option('-v', '--verbose', count=True)
def ical2notion(database, token, icals, verbose):
    """Google calendar to notion made simple."""
    # Download the users ical files and get all events
    events = []
    for url in icals:
        # Log if verbose
        if verbose == 1:
            click.echo(f"Downloading calendar from {url}")
        try:
            c = Calendar(requests.get(url).text)
            events += list(c.timeline)
        except Exception as e:
            # Echo the exception if verbose verbose
            if verbose == 2:
                click.echo("Exception occured while downloading calendar: {e}", err=True)
            # Echo that it failed if just verbose
            else:
                click.echo("Exception occured while downloading calendar", err=True)

    events = [e for e in events if e > Event(begin=datetime.now())]

    # Authenticate with notion
    try:
        client = NotionClient(token_v2=token)
    except requests.exceptions.HTTPError as e:
        # Echo the exception if verbose verbose
        if verbose == 2:
            click.echo("Exception occured while authenticating with notion: {e}", err=True)
        # Echo that it failed if just verbose
        else:
            click.echo("Exception occured while authenticating with notion", err=True)

    # Add each event to the notion database
    try:
        gcal_table = client.get_collection_view(database)
    except Exception as e:
        # Echo the exception if verbose verbose
        if verbose == 2:
            click.echo("Exception occured while accessing notion database: {e}", err=True)
        # Echo that it failed if just verbose
        else:
            click.echo("Exception occured while accessing notion database", err=True)


    for event in events:
        # Check that it isn't in there
        cont = True
        for row in gcal_table.collection.get_rows():
            if row.Name == event.name:
                add_or_update(row, event)
                cont = False
                break
        if cont:
            row = gcal_table.collection.add_row()
            add_or_update(row, event)

def add_or_update(row, event):
    row.Name = event.name
    # Check if the event is an "All Day" these get messed up if we do a direct conversion
    if event.duration == timedelta(days=1):
        row.Do = NotionDate((event.begin))
    else:
        row.Do = NotionDate(datetime.fromisoformat(str(event.begin)),
                              datetime.fromisoformat(str(event.end)))
    row.Type = "Event"

if __name__ == "__main__":
    ical2notion()

