import pandas as pd
import sys

def main(input_file, output_file):
    df = pd.read_csv(input_file)

    df.rename(columns={'JSC «Kaspi Bank», BIC CASPKZKA, www.kaspi.kz': 'test'}, inplace=True)

    column_name = df.columns[0]

    mask = ~df['test'].astype(str).str[0].str.isdigit()

    df = df[~mask]

    df = df.reset_index(drop=True)

    def extract_date(row):
        return row[0].split(" ")[0] if pd.notnull(row[0]) else None

    df['date'] = df.apply(lambda row: extract_date(row), axis=1)

    def amount(lst):
        sign = -1 if '-' in lst else 1
        currency_index = lst.index('₸')

        if currency_index == 4:
            amount_parts = lst[currency_index-2:currency_index]
        elif currency_index == 3:
            amount_parts = lst[currency_index-1:currency_index]
        elif currency_index == 5:
            amount_parts = lst[currency_index-3:currency_index]

        amount_str = ''.join(amount_parts).replace(' ', '').replace(',', '.')

        return float(amount_str) * sign

    df['amount'] = pd.NA

    for i in range(len(df)):
        lst = [element for element in df.loc[i, 'test'].split(" ") if element != '']
        df.at[i, 'amount'] = amount(lst)

    def transaction(lst):
        currency_index = lst.index('₸')
        transaction_index = currency_index + 1
        return lst[transaction_index]

    df['transaction'] = pd.NA

    for i in range(len(df)):
        lst = [element for element in df.loc[i, 'test'].split(" ") if element != '']
        df.at[i, 'transaction'] = transaction(lst)

    def details(lst):
        currency_index = lst.index('₸')
        string = ''
        
        for i in lst[currency_index + 2:]:
            string += i + " "  
            
        return string.strip() 

    df['details'] = pd.NA

    for i in range(len(df)):
        lst = [element for element in df.loc[i, 'test'].split(" ") if element != '']
        df.at[i, 'details'] = details(lst)
    
    df.drop(columns=['test'], inplace=True)

    df.to_csv(output_file, index=False)  

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test.py [input_file] [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
