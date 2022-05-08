import json
import os
import requests
from slack import WebClient

from slack_bolt import App
from helper import Datafile, strip
from inserter import LatexBuilder
import templates
from api import get_events
from values import Events


class InputError(Exception):
    pass

def setup_home_tab(client, event, logger):
        client.views_publish(
            user_id=event["user"],
            view = templates.home_view_template()
        )

def open_invoice_modal_from_shortcut(ack, shortcut, client: WebClient):
  
  ack()
  
  client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view = templates.invoice_submit_template(get_events())
    )

def open_invoice_modal_from_home(ack, body, client):
  ack()
  client.views_open(
        trigger_id=body["trigger_id"],
        # A simple view payload for a modal
        view = templates.invoice_submit_template(get_events())
    )
  
def handle_invoice_submission(ack, body, client: WebClient):
    
    values: dict = body["view"]["state"]["values"]
    user: str = body["user"]["id"]
    
    try:
        stripped: dict = strip(values, user)
    except InputError as e:
        errors = {}
        errors[e.args[1]] = e.args[0]
        ack(response_action="errors",errors=errors)
        return
    
    ack()
    file = Datafile(stripped["event_name"])
    file.store(stripped)
    
    # Ask user in private chat to upload the respective invoice
    ask_for_file(user, client)
    
    builder = LatexBuilder(file.filename,file.date_of_event)
    builder.set().compile()
    
    return

def ask_for_file(user_id: str, client: WebClient):
    
    client.chat_postMessage(
        channel=user_id,
        text=Events.ASK_FOR_FILE.value
    )
    
# TODO Save file somewhere
def save_uploaded_invoice(client: WebClient, body):
    
    file_url = body["event"]["files"][0]["url_private_downloads"]
    
    file = requests.get(file_url).content
    