import pandas as pd

df = pd.read_csv("datasets/ora_test.csv")

init_balance = 572.81
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%y')
df = df.iloc[::-1]
deposit = 0
income = 0
expenditures = 0
balance_trend = []
expenditures_trend = []
income_trend = []
dates = []

for row in df.iterrows():
    init_balance += row[1]['amount']
    if row[1]['details'] == 'To Kaspi Deposit':
        deposit += row[1]['amount']
    elif row[1]['details'] == 'From Kaspi Deposit':
        deposit -= row[1]['amount']
    elif row[1]['amount'] > 0:
        income += row[1]['amount']
    elif row[1]['amount'] < 0:
        expenditures -= row[1]['amount']
    income_trend += [income]
    expenditures_trend += [expenditures]
    if init_balance < 0:
        print(row)
        print(init_balance)
    balance_trend += [init_balance]
    dates += [row[1]['date']]

df_current = pd.DataFrame({'current_balance' : balance_trend, 'dates' : dates, 'income_trend' : income_trend, 'expenditures_trend' : expenditures_trend})
plot = df_current.plot(x='dates', kind='line')
fig = plot.get_figure()
fig.savefig("outputs/line-graph.png")