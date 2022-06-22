import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Script settings
pd.set_option('display.max_columns', None)
DATE_COL = 'Buchungstag'
AMOUNT_COL = 'Umsatz in EUR'
CUMULATIVE_COL = 'Cumulative'
CLEAN_DATA = 'comdirect_clean.csv'
OLD_BALANCE = 3858.77


# Define help functions fpr parsing
def date_parser(date):
    try:
        return dt.datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        return None


def number_parser(number_text):
    num = number_text.replace('.', '')
    num = num.replace(',', '.')
    return float(num)


# Read CSV data
data = pd.read_csv(CLEAN_DATA,
                   sep=';',
                   parse_dates=[DATE_COL],
                   date_parser=date_parser)
date_eur = data[[DATE_COL, AMOUNT_COL]]
date_eur[AMOUNT_COL] = date_eur[AMOUNT_COL].apply(number_parser)
date_eur = date_eur[date_eur[DATE_COL].notnull()]


# Aggregate list by dates
date_eur_by_day = date_eur.groupby(DATE_COL).agg('sum')
date_eur_by_day.reset_index(inplace=True)
date_eur_by_day[CUMULATIVE_COL] = date_eur_by_day[AMOUNT_COL].cumsum(axis=0) + OLD_BALANCE


# Plot the final data
plt.xlabel('Date')
plt.ylabel('Balance (€)')
plt.plot(date_eur_by_day[DATE_COL], date_eur_by_day[CUMULATIVE_COL])
plt.show()
