from datetime import datetime
from api import get_events
from values import Events
import templates


def setup_home_page(client, event, logger):
    client.views_publish(
        user_id=event["user"],
        view=templates.home_view_template()
    )


def open_invoice_modal_from_home(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=templates.invoice_submit_template(get_events())
    )


def check_invoice_date(ack, body):
    invoice_date = body["actions"][0]["selected_date"]
    # Check if selected date lies in the future
    today = datetime.today()
    to_check = datetime.strptime(invoice_date, "%Y-%m-%d")
    if today < to_check:
        ack(response_action="errors", errors={
            Events.INVOICE_SELECT_DATE.value: "Du kannst keine Rechnungen aus der Zukunft einreichen."
        })
        return
    ack()


def check_invoice_event(ack):
    ack()


def handle_invoice(ack, body, client):
    values: dict = body["view"]["state"]["values"]
    user: str = body["user"]["id"]
    print(values, user)
    email = client.users_profile_get(user=user)['profile']['email']
    print(email)
    ack()
