import os
from datetime import datetime

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import controllers
from values import Events

load_dotenv() 

app = App(token=os.environ["TOKEN"],signing_secret=os.environ["SIGNING_SECRET"])

# Declare the event data dict which will be filled once the home-tab
# of the bot is opened
EVENT_DATA: dict

app.event("app_home_opened")(controllers.setup_home_tab)

# Open the invoice modal via its global shortcut
app.global_shortcut(Events.OPEN_HOME_BUTTON.value)(controllers.open_invoice_modal_from_shortcut)


# Open the invoice modal but this time by pressing the corresponding button
# in the home tab
app.action(Events.OPEN_HOME_BUTTON.value)(controllers.open_invoice_modal_from_home)

@app.action("event-selection")
def handle_selection(ack, body):
    ack()
    
@app.action("users_select-action")
def handle_some_action(ack, body):
    ack()

    
@app.action("invoice-date-select")
def handle_datepicker(ack, body):
    invoice_date = body["actions"][0]["selected_date"]
    # Check if selected date lies in the future
    today = datetime.today()
    to_check = datetime.strptime(invoice_date,"%Y-%m-%d")
    if today < to_check:
        #raise InputError("Du kannst keine Rechnungen aus der "
        #                  "Zukunft einreichen.", "event_date")
        errors = {}
        errors["invoice-date-select"] = ("Du kannst keine Rechnungen aus der "
                                         "Zukunft einreichen.")
        ack(response_action="errors",errors=errors)
        return
    else:
        ack()
    return
    
app.view(Events.INVOICE.value)(controllers.handle_invoice_submission)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SOCKET_TOKEN"]).start()
