import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

ROOT = Path(__file__).resolve().parents[2]


def massage_data(raw_data):
    """ Preprocess the data for predictions
    """
    raw_data.rename(index=str, columns={"whether he/she donated blood in March 2007": "label"}, inplace=True)
  
    # generate features for year for time columns
    for x, y in zip(['time_years', 'recency_years'], ['Time (months)', 'Recency (months)']):
        raw_data[x] = (raw_data[y] / 12).astype('int')
 
    # generate features for quarter for time columns (3 month periods)
    for x, y in zip(['time_quarters', 'recency_quarters'], ['Time (months)', 'Recency (months)']):
        raw_data[x] = (raw_data[y] / 3).astype('int')

    return raw_data


def main():
    """ Retrieves data and runs processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    df = pd.read_csv(ROOT / 'data/raw/transfusion_data_raw.csv')
    processed_data = massage_data(df)
    processed_data.to_csv(ROOT / 'data/processed/transfusion_data.csv', index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    load_dotenv(find_dotenv())

    main()