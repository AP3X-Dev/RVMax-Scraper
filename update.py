import pandas as pd
from datetime import datetime
import schedule
import time
import os

def job():
    # List of input CSV files
    input_files = ['input1.csv', 'input2.csv', 'input3.csv']
    
    for input_file in input_files:
        if os.path.exists(input_file):
            df = pd.read_csv(input_file)

            # Check if 'price' column exists in DataFrame
            if 'price' in df.columns:
                # Remove rows with empty 'price' cell
                df = df[df['price'].notna()]

                # Write the data back to a new CSV file
                output_file = 'output_' + input_file
                df.to_csv(output_file, index=False)
                print(f"{datetime.now()}: Task completed successfully for {input_file}!")
        else:
            print(f"{datetime.now()}: {input_file} does not exist!")

# Schedule the job every 24 hours
schedule.every(24).hours.do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
