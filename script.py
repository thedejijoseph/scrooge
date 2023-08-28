
import json
import pandas as pd
import copy

input_file = 'input.csv'
output_file = 'output.csv'

df = pd.read_csv(input_file)

df['Amount'] = df['Amount'].str.replace('[₦$,]', '', regex=True).astype(float)
df['Transaction Type'] = df['Amount'].apply(lambda x: 'DR' if x < 0 else 'CR')

data = df.to_json(orient='records')
data = json.loads(data)
prepared = []

for record in data:
    if record['Type'] == 'Transfer':
        payment = copy.deepcopy(record)
        payment['Account'] = record['Payment account']
        payment['Amount'] = - record['Amount']
        payment['Transaction Type'] = 'DR'
        payment['Payment account'] = ''

        receiving = copy.deepcopy(record)
        receiving['Account'] = record['Account receivable']
        receiving['Account receivable'] = ''

        prepared.append(payment)
        prepared.append(receiving)
    
    else:
        prepared.append(record)

df = pd.read_json(json.dumps(prepared))

# Save Cleaned Data to Output CSV
df.to_csv(output_file, index=False)
