# ical2notion

ICal2Notion is a simple command line tool that is used to update a Notion database from an .ical file hosted online (like on Google Calendar).

## Installation
To install clone the repository and run `python setup.py install`.

## Usage
1. Find your Notion authentication token. This is located in the `token_v2` cookie under the domain `www.notion.so`.
	1. Navigate to a Notion workspace
	2. Click the lock on the left hand side of the URL bar
	3. Click Cookies
	4. Drop down the `www.notion.so` list
	5. Drop down the `Cookies` list
	6. Copy the content from the `token_v2` cookie
2. Create a database for the Google Calendar to be populated into
	1. Create a new page
	2. Create an inline table
	3. Click "Open as page"
	4. Copy that URL
3. Find your ical public link
	1. Open google calendar
	2. Click on the three dots to the right of a calendar listed under My calendars on the bottom left
	3. Click settings and sharing
	4. Scroll all the way to the bottom and copy the "Secret address in iCal format" link

Run `ical2notion [TOKEN] [URL] [iCal]`. You can list multiple icals at the end.


