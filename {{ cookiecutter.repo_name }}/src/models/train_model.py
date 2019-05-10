import pickle
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]

if '{{ cookiecutter.python_interpreter }}' == 'python3':
    PROTOCOL = pickle.DEFAULT_PROTOCOL
else:
    PROTOCOL = 2


def fetch_processed(data_path):
    """
    fetch the data that was processed in make data
    """
    data = pd.read_csv(ROOT / data_path)
    data_y = data.label
    data_x = data.drop(['label'], axis=1)
    
    # Create training and test sets
    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, 
        test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test


def fit_model(X_train, y_train):
    """
    fit a model to the training data
    """
    model = RandomForestClassifier(n_estimators=100)

    # Fit to the training data
    model.fit(X_train, y_train)
    return model


def main():
    """ Trains the model on the retrieved data write it back to file
    """
    x_train, x_test, y_train, y_test = fetch_processed('data/processed/transfusion_data.csv')
    
    # Train the model 
    model = fit_model(x_train, y_train)
    
    # Store model and test set for prediction
    with open(ROOT / 'models/transfusion.model', 'wb') as fout:
        pickle.dump(model, fout, PROTOCOL)
    x_test.to_csv(ROOT / 'data/processed/transfusion_x_test.csv',
        index=False)
    y_test.to_csv(ROOT / 'data/processed/transfusion_y_test.csv',
        index=False)


if __name__ == '__main__':
    main()
