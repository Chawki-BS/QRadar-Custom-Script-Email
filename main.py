import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

SEC_TOKEN = '<Your Security Token>'
URL = 'https://<Your QRadar IP address>/api/siem/offenses'

SMTP_SERVER = "<Your SMTP Server>"
SMTP_PORT = 587 # Default
SMTP_USERNAME = "<Your SMTP Server username>"
SMTP_PASSWORD = "<Your SMTP Server password>"
EMAIL_FROM = "<Your SMTP Server email address>"
EMAIL_TO = "<Destination Email Address>"

header = {
        'SEC':SEC_TOKEN,
        'Content-type':'application/json',
        'accept':'application/json'
        }

#set up query parameters to retrieve the last offense
params = {
        "fields": "description, domain_id, start_time, magnitude, source_network, destination_networks, assigned_to, status",
        "sort": "-id",
        "range": "0-0"
        }

#response
r = requests.get(URL, headers=header, verify=False, params=params)

offenses = r.json()
offense = offenses[0]

# Create the HTML content of the email
html_content = f"""
<html>
<head>
<style>
    /* CSS styles */
    table {{
        border-collapse: collapse;
    }}
    th, td {{
        padding: 8px;
        border: 1px solid black;
    }}
    b {{
        background-color: #f2f2f2;
    }}
    h1 {{
        color: #333;
    }}
</style>
</head>
<body>
    <h1>A new offense has been fired !</h1>
    <table>
        <tr>
            <td><b>Description</td>
            <td>{offense['description']}</td>
        </tr>
        <tr>
            <td><b>Tenant</td>
            <td>{offense['domain_id']}</td>
        </tr>
        <tr>
            <td><b>Time</td>
            <td>{offense['start_time']}</td>
        </tr>
        <tr>
            <td><b>Severity</td>
            <td>{offense['magnitude']}</td>
        </tr>
        <tr>
            <td><b>Source</td>
            <td>{offense['source_network']}</td>
        </tr>
        <tr>
            <td><b>Destination</td>
            <td>{offense['destination_networks']}</td>
        </tr>
        <tr>
            <td><b>Assigned</td>
            <td>Assigned: {offense['assigned_to']}</td>
        </tr>
        <tr>
           <td><b>Status</td>
           <td>Status: {offense['status']}</td>
        </tr>
    </table>
</body>
</html>
"""

# Set up the email message
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Offense Information'
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

# Create a MIMEText object for the HTML content
html_part = MIMEText(html_content, 'html')

# Attach the HTML part to the email message
msg.attach(html_part)

# Set up the SMTP server and send the email
smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp_server.starttls()
smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
smtp_server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
smtp_server.quit()