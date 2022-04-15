from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Events(AutoName):
    OPEN_HOME_BUTTON = auto()
    INVOICE = auto()
    INVOICE_SELECT_DATE = auto()
    INVOICE_SELECT_EVENT = auto()
    INVOICE_SELECT_AMOUNT = auto()
    INVOICE_SELECT_DESCRIPTION = auto()
    APP_HOME_OPENED = auto