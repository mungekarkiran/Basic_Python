import pandas as pd
import json
import pickle

# Load JSON data
# with open('Sarcasm.json', 'r') as f:
#     json_data = json.load(f)

with open('Sarcasm.json', 'r') as f:
    json_data = ''
    for line in f:
        json_data += line.strip()
        try:
            obj = json.loads(json_data)
            # Do something with the object
            json_data = ''
        except json.decoder.JSONDecodeError:
            # More data is expected, so continue reading
            pass

# Open a binary file for writing
with open('data.pkl', 'wb') as f:
    # Dump the Python object as a pickle
    pickle.dump(json_data, f)

# Close the file
f.close()


# # Convert the JSON data to a DataFrame
# df = pd.json_normalize(json_data)

# # Save the DataFrame as a CSV file
# df.to_csv('data.csv', index=False)

# with open('Sarcasm.json', encoding='utf-8') as inputfile:
#     df = pd.read_json(inputfile)

# Read the JSON data to a DataFrame
df = pd.read_json('Sarcasm.json', lines=True)

# Save the DataFrame as a CSV file
df.to_csv('csvfile.csv', encoding='utf-8', index=False)