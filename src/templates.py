

from datetime import datetime
import json

from values import Events


def home_view_template():
    template = {
        "type": "home",
        "callback_id": "home_view",

        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Willkommen beim Invoicer*:tada:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Du hast Geld für den Verein ausgegeben und willst es jetzt zurück?\n Perfekt! Reiche einfach deine Rechnung unten ein und den Rest mache ich :smile:"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Rechnung einreichen!"
                        },
                        "style": "primary",
                        # "value": "submit-invoice",
                        "action_id": Events.OPEN_HOME_BUTTON.value
                    }
                ]
            }
        ]
    }
    return json.dumps(template)


def invoice_submit_template(events):
    template = {
        "title": {
            "type": "plain_text",
            "text": "Rechnung Einreichen",
            "emoji": True
        },
        "callback_id": Events.INVOICE.value,
        "submit": {
            "type": "plain_text",
            "text": "Einreichen",
            "emoji": True
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Abbrechen",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Moin, ich bin dein Rechnungsbot! Du hast Geld f\u00fcr unseren Verein ausgegeben und willst es jetzt echt wieder haben? Na gut...\n\nBitte f\u00fclle dieses Formular aus:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "block_id": Events.INVOICE_SELECT_EVENT.value,
                "text": {
                    "type": "mrkdwn",
                    "text": "*Event*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Event ausw\u00e4hlen",
                        "emoji": True
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": slug,
                            },
                            "value": slug
                        }
                        for slug in events.keys()
                    ],
                    "action_id": Events.INVOICE_SELECT_EVENT.value,
                }
            },
            {
                "type": "section",
                "block_id": Events.INVOICE_SELECT_DATE.value,
                "text": {
                    "type": "mrkdwn",
                    "text": "*Rechnungsdatum*"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Veranstaltungsdatum",
                        "emoji": True
                    },
                    "action_id": Events.INVOICE_SELECT_DATE.value
                }
            },
            {
                "type": "input",
                "block_id": Events.INVOICE_SELECT_DESCRIPTION.value,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "purpose"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Wof\u00fcr hast du Geld ausgegeben?",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": Events.INVOICE_SELECT_AMOUNT.value,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Wie viel Geld hast du ausgegeben?",
                    "emoji": True
                }
            }
        ]
    }
    return json.dumps(template)
