from typing import List
import requests
import os
from settings.config import load_env_config

config = load_env_config()

def send_to_smtp2go(subject: str=None, recipients: str=None, text: str=None, html: str=None, attachments: List=[]):
    api_key = config['smtp2go_key']
    url = config['smtp2go_url'] + "email/send"
    headers = { "Content-Type": "application/json" }
    data = {
        "api_key": api_key,
        "sender": config['smtp2go_name'] + " <"+config['smtp2go_address']+">",
        "to": [recipients],
        "subject": subject,
        "text_body": text,
        "html_body": html,
        "attachments": attachments,
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response.json()

def get_notification_string(title: str=None, body: str=None, foot: str=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, "../../"))
    template_path = os.path.join(base_dir, "templates", "notifications.html")
    html = ""
    with open(template_path, "r", encoding="utf-8") as file:
        html = file.read()
    if html != "":
        html = html.replace("@title@", title)
        html = html.replace("@body@", body)
        html = html.replace("@foot@", foot)
    return html

def send_email(subject: str=None, recipients: str=None, title: str=None, body: str=None, foot: str=None, attachments: List=[]):
    text = str(title) + "\n" + str(body) + "\n" + str(foot)
    html = get_notification_string(title=title, body=body, foot=foot)
    return send_to_smtp2go(subject=subject, recipients=recipients, text=text, html=html, attachments=attachments)

def e_send_token(username: str=None, email: str=None, token: str=None, minutes: int=0):
    title = "New Token"
    msg = "<p>Hello " + str(username) + ",<br><br>Use the code below to complete your action:<br><br>"+str(token)+"<br><br>The above token expires in " + str(minutes) + " minutes<br>If you didn't originate this please reach out to our support team at support@upteek.com</p>"
    footnote = "💕 & ✨, Upteek."
    return send_email(subject=title, recipients=email, title=title, body=msg, foot=footnote)