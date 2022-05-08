from datetime import datetime

from models import Invoice
from values import Events


class InputError(Exception):
    pass

def extract_invoice(v: dict, user_id: str) -> Invoice:
    event_name = v[Events.INVOICE_SELECT_EVENT.value][Events.INVOICE_SELECT_EVENT.value]\
        ["selected_option"]["text"]["text"]
    event_date = v[Events.INVOICE_SELECT_DATE.value][Events.INVOICE_SELECT_DATE.value]["selected_date"]
    cost = v[Events.INVOICE_SELECT_AMOUNT.value]["plain_text_input-action"]["value"]
    purpose = v[Events.INVOICE_SELECT_DESCRIPTION.value]["purpose"]["value"]
    
    event_date = datetime.strptime(event_date, "%Y-%m-%d")
    
    # Capitalize first letter
    purpose = purpose[0].upper() + purpose[1:]

    try:
        cost = float(cost)
    except:
        raise InputError("Bitte Ganzzahl oder "
                         "Englisches Format nutzen. Bsp: 2 oder 12.69",
                         "invoice_cost")

    if str(cost)[::-1].find(".") > 2:
        raise InputError("Mehr als zwei Nachkommastellen gibt es "
                         "nicht amk.", "invoice_cost")

    return Invoice(event_slug=event_name, date=event_date, purpose=purpose, cost=cost, user=user_id)
