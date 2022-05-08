from helper import extract_invoice
from inserter import LatexBuilder
from storage import read_invoices, write_invoices
import templates
from api import get_events

class InputError(Exception):
    pass

def setup_home_tab(client, event, logger):
        client.views_publish(
            user_id=event["user"],
            view = templates.home_view_template()
        )

def open_invoice_modal_from_shortcut(ack, shortcut, client):
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
  
def handle_invoice_submission(ack, body, client):
    values: dict = body["view"]["state"]["values"]
    user: str = body["user"]["id"]
    
    try:
        invoice = extract_invoice(values, user)
    except InputError as e:
        errors = {}
        errors[e.args[1]] = e.args[0]
        ack(response_action="errors",errors=errors)
        return
    
    ack()

    try:
      invoices = read_invoices(invoice.event_slug)
    except:
      invoices = []

    invoices.append(invoice)
    write_invoices(invoice.event_slug, invoices)

    events = get_events()
    builder = LatexBuilder(events[invoice.event_slug], invoices)
    builder.set().compile()
    
    return
