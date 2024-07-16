import json
import pandas as pd
import matplotlib.pyplot as plt

# Laden der JSON-Daten aus einer Datei
with open('vault-data-3.json') as f:
    data = json.load(f)

# Extrahieren der monatlichen Daten
months_data = data['data']['months']

# Erstellen einer Liste von Daten für das DataFrame
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

# Erstellen des DataFrames
df = pd.DataFrame(records)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Daten vor 01.01.2024 und nach 31.12.2024 filtern
df = df['2024-01-01':'2024-12-31']

# Benutzerdefinierte Quartalszuweisung
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

# Berechnung der durchschnittlichen Werte pro Quartal
quarterly_avg = df.groupby('quarter').sum() / 3

# Plotten der monatlichen Daten
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

# Plotten der Daten für jedes Quartal
plt.figure(figsize=(10, 6))
plt.plot(quarterly_avg.index, quarterly_avg['entity_clients'], marker='o', label='Entity Clients Quarterly Average')
plt.plot(quarterly_avg.index, quarterly_avg['non_entity_tokens'], marker='o', label='Non-Entity Tokens Quarterly Average')
plt.plot(quarterly_avg.index, quarterly_avg['non_entity_clients'], marker='o', label='Non-Entity Clients Quarterly Average')
plt.plot(quarterly_avg.index, quarterly_avg['clients'], marker='o', label='Total Clients Quarterly Average')
plt.xlabel('Quarter')
plt.ylabel('Average Count')
plt.title('Quarterly Average Client Activity in Vault')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Ausgabe der Quartalsdurchschnitte
print(quarterly_avg)
