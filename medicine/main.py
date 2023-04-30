import pandas as pd
import model
from model import Medicine
from database import engine
from sqlalchemy.orm import sessionmaker

model.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Read the text file
with open('medx.txt', 'r') as file:
    lines = file.readlines()

# Create a list of dictionaries
data = []
for line in lines:
    line = line.strip().split('|')
    item = {
        'product_name': line[0].strip(),
        'generic_name': line[1].strip(),
        'dosage_form': line[2].strip(),
        'strength': line[3].strip(),
        'manufacturer': line[4].strip(),
        'price_type': line[5].strip().split(':')[0].strip(),
        'price': line[5].strip().split(':')[-1].replace('à§³', '').replace('৳','').replace(',', '').strip()
    }
    data.append(item)

# Create a dataframe
df = pd.DataFrame(data)
df['price'] = df['price'].replace(['Price not available', 'Price Unavailable', 'Not for sale'], 0)
df['price'] = df['price'].astype(float)

# Check which rows have already been inserted
existing_medicines = session.query(Medicine).all()
# existing_product_names = [medicine.product_name for medicine in existing_medicines]
last_processed_index = len(existing_medicines)

print("Last processed index: ", last_processed_index)

# Insert new rows
for i in range(last_processed_index, len(df)):
    row = df.iloc[i]

    # if row['product_name'] in existing_product_names:
    #     continue  # skip the rows that have already been processed

    medicine = Medicine(product_name=row['product_name'], generic_name=row['generic_name'], dosage_form=row['dosage_form'], 
                        strength=row['strength'], manufacturer=row['manufacturer'], 
                        price_type=row['price_type'], price=row['price'])
    session.add(medicine)
    print("Added :", row['product_name'])

    if i % 100 == 0:  # commit the changes every 100 rows to avoid long transactions
        session.commit()

session.commit()  
session.close()
