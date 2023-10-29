import datetime
from gr_datetime.gr_numbers import num2word
import re

days_of_week = [
    'Δευτέρα',
    'Τρίτη',
    'Τετάρτη',
    'Πέμπτη',
    'Παρασκευή',
    'Σάββατο',
    'Κυριακή'
]

months_greek_genitive = [
    'Ιανουαρίου',
    'Φεβρουαρίου',
    'Μαρτίου',
    'Απριλίου',
    'Μαΐου',
    'Ιουνίου',
    'Ιουλίου',
    'Αυγούστου',
    'Σεπτεμβρίου',
    'Οκτωβρίου',
    'Νοεμβρίου',
    'Δεκεμβρίου'
]

def get_date():
    today = datetime.date.today()

    wd = today.weekday()
    d = today.day
    m = today.month
    y = today.year

    str_wd = days_of_week[wd]
    str_d = num2word(d).capitalize()
    # fem
    str_d = re.sub("σσερα", "σσερις", str_d)
    str_m = months_greek_genitive[m]
    str_y = num2word(y)

    fdate = f"Καλημέρα. Σήμερα η μέρα, εδώ που μένω εγώ, είναι {str_wd}, {str_d} (του) {str_m} (του έτους) {str_y}."

    now = datetime.datetime.now()
    h = now.hour
    m = now.minute

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

    return f"{fdate} {fhour}"
