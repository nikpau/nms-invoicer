import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import controllers
from values import Events

load_dotenv()

app = App(token=os.environ["TOKEN"],
          signing_secret=os.environ["SIGNING_SECRET"])


app.event("app_home_opened")(controllers.setup_home_page)
app.action(Events.OPEN_HOME_BUTTON.value)(
    controllers.open_invoice_modal_from_home)
app.action(Events.INVOICE_SELECT_DATE.value)(controllers.check_invoice_date)
app.action(Events.INVOICE_SELECT_EVENT.value)(controllers.check_invoice_event)
app.view(Events.INVOICE.value)(controllers.handle_invoice)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SOCKET_TOKEN"]).start()
