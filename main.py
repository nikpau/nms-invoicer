import json
import os
import dynamics as dyn
import helper
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from json_blocks import __path__
    
load_dotenv() 
app = App(token=os.environ["TOKEN"],signing_secret=os.environ["SIGNING_SECRET"])

# Add functionality here
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    
    # Parse the home_tab_view json file
    with open(__path__[0] + "/home_tab_view.json", "r") as file:
        home = json.load(file)
    
    try:
    # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
      # the user that opened your app's app home
        user_id=event["user"],
      # the view object that appears in the app home
        view = json.dumps(home))
  
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

# Say something upon mentioning the bot
@app.event("app_mention")
def event_test(say):
    say("What's up?")

@app.message("")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    user = message["user"]
    say(text=f"Hey there <@{user}>!")

# Open the invoice modal via its global shortcut
@app.global_shortcut("open-invoice-modal")
def open_invoice_modal(ack, shortcut, client):
  
  ack()
  
  client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view = dyn.push_event_list(
            dyn.create_event_list(
                helper.get_eventlist()
                )
            )
    )

# Open the invoice modal but this time by pressing the corresponding button
# in the home tab
@app.action("home-submit-button")
def open_invoice_modal_from_home(ack, body, client):
    
    # Ackowledge the incoming request
    ack()
    
    # Open the modal
    client.views_open(
        trigger_id = body["trigger_id"],
        view = dyn.push_event_list(
            dyn.create_event_list(
                helper.get_eventlist()
                )
            )
    )

@app.action("static_select-action")
def handle_selection(ack, body, logger):
    ack()
    
@app.action("users_select-action")
def handle_some_action(ack, body, logger):
    ack()
    
@app.view("invoice")
def handle_view_events(ack, body, logger, client):
    logger.info(body)
    values: dict = body["view"]["state"]["values"]
    
    try:
        stripped: dict = helper.strip(values)
    except ValueError as e:
        errors = {}
        errors["event_cost"] = e.args[0]
        ack(response_action="errors",errors=errors)
        return
    
    ack()
    file = helper.Datafile(stripped["event_name"])
    file.store(stripped)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SOCKET_TOKEN"]).start()
