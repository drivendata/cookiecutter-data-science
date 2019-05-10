import pandas as pd
from src.data.make_dataset import massage_data


mock_data = {
   'whether he/she donated blood in March 2007': [1, 0, 0, 1],
   'Time (months)': [36, 10, 12, 16],
   'Recency (months)': [10, 20, 15, 22] 
}


def test_massage_data():
    raw = pd.DataFrame(mock_data)
    data = massage_data(raw)
    assert data.iloc[0, 2] == 10
    assert data.iloc[3, 6] == 7
    