import datetime
import re

from gr_datetime.gr_numbers import num2word

DAYS_NOMINATIVE = [
    "Δευτέρα",
    "Τρίτη",
    "Τετάρτη",
    "Πέμπτη",
    "Παρασκευή",
    "Σάββατο",
    "Κυριακή",
]

MONTHS_GENITIVE = [
    "Ιανουαρίου",
    "Φεβρουαρίου",
    "Μαρτίου",
    "Απριλίου",
    "Μαΐου",
    "Ιουνίου",
    "Ιουλίου",
    "Αυγούστου",
    "Σεπτεμβρίου",
    "Οκτωβρίου",
    "Νοεμβρίου",
    "Δεκεμβρίου",
]


def get_full_date():
    fdate = get_date()
    fhour = get_hour()

    return f"{fdate} {fhour}"


def get_date():
    today = datetime.date.today()
    wd = today.weekday()
    d, m, y = today.day, today.month, today.year

    str_wd = DAYS_NOMINATIVE[wd]
    str_d = num2word(d).capitalize()
    # fem
    str_d = re.sub("σσερα", "σσερις", str_d)
    str_m = MONTHS_GENITIVE[m]
    str_y = num2word(y)

    fdate = f"Καλημέρα. Σήμερα η μέρα, εδώ που μένω εγώ, είναι {str_wd}, {str_d} (του) {str_m} (του έτους) {str_y}."

    return fdate


def get_hour():
    now = datetime.datetime.now()
    h, m = now.hour, now.minute

    pm = h > 12
    h %= 12

    str_h = num2word(h)
    str_m = num2word(m)

    # To fem
    str_h = str_h.replace("ένα", "μία")

    fhour = f"Και η ώρα είναι {str_h}"
    if m > 0:
        fhour += f" και {str_m} λεπτά"
    fhour += " μ.μ." if pm else " π.μ."
    fhour += "."

    return fhour
