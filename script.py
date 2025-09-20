import os
import pandas as pd

# --------------- Define folder paths ---------------
folder_path = 'archive'  # replace with your folder path
cleaned_path = 'cleaned_datasets'  # folder to save cleaned files


# --------------- Automated Cleaning Function ---------------
def cleaning_all_files(filename):
    # Read CSV file
    df = pd.read_csv(f"{folder_path}/{filename}")

    # drop nan rows. some are empty rows so they are removed
    df = df.dropna(how='all')

    # Delete rows that are wrongly entered
    df.drop(df[df['Product'] == 'Product'].index, inplace=True)

    # split Purchase Address column. State_ is a temp place holder that has state and zip.
    df[['Address', 'City', 'State_']] = df['Purchase Address'].str.split(',', expand=True)

    # split the "State_" into state and zip code
    df[['State', 'Zip Code']] = df['State_'].str.strip().str.split(' ', n=1, expand=True)

    df = df.drop('Purchase Address', axis=1)
    df = df.drop('State_', axis=1)  # drop the temp place holder column

    # create revenue column
    df['Revenue'] = df['Quantity Ordered'].astype(float) * df['Price Each'].astype(float)

    # States abbreviation to full names
    states_replace = {
        'MA': 'Massachusetts',
        'OR': 'Oregon',
        'CA': 'California',
        'TX': 'Texas',
        'GA': 'Georgia',
        'WA': 'Washington',
        'NY': 'New York',
        'ME': 'Maine'
    }

    df['State'] = df['State'].map(states_replace)  # Replaced using maps

    # Save cleaned file
    df.to_csv(f"{cleaned_path}/{filename}", index=False)


# --------------- Loop through all files in the folder ---------------
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # if the file is a CSV file, run the functions
    try:
        if os.path.isfile(file_path) and filename.lower().endswith('.csv'):
            cleaning_all_files(filename)
            print(filename, "— cleaned and saved.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
# --------------- End of Script ---------------

print("\n\n"
      "All files processed and script ended successfully.")