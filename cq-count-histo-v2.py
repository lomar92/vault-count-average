import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load JSON File 
with open('vault-data-3.json') as f:
    data = json.load(f)

# Extract monthly Data
months_data = data['data']['months']

# Create Data List for DataFrame
records = []
for month in months_data:
    if month['counts'] is not None:
        record = {
            'timestamp': month['timestamp'],
            'entity_clients': month['counts']['entity_clients'],
            'non_entity_tokens': month['counts']['non_entity_tokens'],
            'non_entity_clients': month['counts']['non_entity_clients'],
            'clients': month['counts']['clients'],
            'secret_syncs': month['counts']['secret_syncs']
        }
        records.append(record)

# Create DataFrames
df = pd.DataFrame(records)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Filter out Dates before 01.01.2024 and after 31.12.2024. This can vary based on the billing start period. 
df = df['2024-01-01':'2024-12-31']

# Custom Quarterly Assignment
quarters = []
for date in df.index:
    if date.month in [1, 2, 3]:
        quarters.append('Q1')
    elif date.month in [4, 5, 6]:
        quarters.append('Q2')
    elif date.month in [7, 8, 9]:
        quarters.append('Q3')
    else:
        quarters.append('Q4')

df['quarter'] = quarters

# Calculate active Clients per Quarter
quarterly_active_clients = df[df['clients'] > 0].groupby('quarter')[['entity_clients', 'non_entity_tokens', 'non_entity_clients', 'clients']].sum() / 3

# Plotting monthly data as a line plot
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['entity_clients'], marker='o', label='Entity Clients Monthly')
plt.plot(df.index, df['non_entity_tokens'], marker='o', label='Non-Entity Tokens Monthly')
plt.plot(df.index, df['non_entity_clients'], marker='o', label='Non-Entity Clients Monthly')
plt.plot(df.index, df['clients'], marker='o', label='Total Clients Monthly')
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('Monthly Client Activity in Vault')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plotting the data for each quarter as a bar chart
fig, ax = plt.subplots(figsize=(10, 6))
quarterly_active_clients.plot(kind='bar', ax=ax)
ax.set_xlabel('Quarter')
ax.set_ylabel('Average Count')
ax.set_title('Quarterly Average Client Activity in Vault')
ax.legend(['Entity Clients Quarterly Average', 'Non-Entity Tokens Quarterly Average', 'Non-Entity Clients Quarterly Average', 'Total Clients Quarterly Average'])
ax.grid(True)
plt.tight_layout()
plt.show()


# Output of quarterly averages
print(quarterly_active_clients)
