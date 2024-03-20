import os
import pandas as pd
from datetime import datetime

def concat_excel(directory):
    concatenated_df = pd.DataFrame()

    # loop through all files in the directory
    for file in os.listdir(directory):        
        if file.endswith('.xlsx'):
            file_path = os.path.join(directory, file)
            df = pd.read_excel(file_path, header=6) # change header position
            concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    return concatenated_df

def process_summary(directory):
    ticker_data = []
    merged_df = pd.DataFrame()

    # loop through all files in the directory
    for file in os.listdir(directory):        
        if file.endswith('.xlsx'):
            file_path = os.path.join(directory, file)

            # read without headers to find the correct header row
            temp_df = pd.read_excel(file_path, header=None)
            temp_df = temp_df.astype(str)  # Convert all columns to strings

            header_row = temp_df[temp_df.apply(lambda x: x.str.contains('Exchange Date', na=False)).any(axis=1)].index[0]
            
            # re-read with correct header row
            df = pd.read_excel(file_path, header=header_row)

            # convert 'Exchange Date' to datetime and filter by date range
            df['Exchange Date'] = pd.to_datetime(df['Exchange Date'])
            start_date = datetime(2023, 12, 21)
            end_date = datetime(2024, 3, 18)
            df = df[df['Exchange Date'].between(start_date, end_date)]

            # calc avgs
            averages = df[['Bid', 'Ask', 'Volume']].mean()

            # append data to list
            ticker = file.split('.')[0]
            ticker_data.append([ticker, averages['Bid'], averages['Ask'], averages['Volume']])

            # concatenate to merged_df
            df['Ticker'] = ticker
            merged_df = pd.concat([merged_df, df], ignore_index=True)

    # convert list of data to a DataFrame
    main_df = pd.DataFrame(ticker_data, columns=['Ticker', 'Avg Bid', 'Avg Ask', 'Avg Volume'])

    return main_df, merged_df