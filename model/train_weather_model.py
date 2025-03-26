import pandas as pd
import joblib
import psycopg2
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

POSTGRES_CONN = {
    'host': 'postgres',
    'dbname': 'weatherdb',
    'user': 'airflow',
    'password': 'airflow'
}

def fetch_data():
    conn = psycopg2.connect(**POSTGRES_CONN)
    df = pd.read_sql("SELECT * FROM processed_weather_data ORDER BY timestamp DESC LIMIT 200", conn)
    conn.close()
    return df

def train_and_save_model():
    df = fetch_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.dayofweek

    X = df[['hour', 'day', 'temperature_celsius']]
    y_temp = df[['temperature_celsius']]
    y_cls = df[['is_raining', 'is_cloudy']]

    X_train, X_test, y_temp_train, y_temp_test = train_test_split(X, y_temp, test_size=0.2)
    X_train_cls, X_test_cls, y_cls_train, y_cls_test = train_test_split(X, y_cls, test_size=0.2)

    temp_model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor())
    ])
    temp_model.fit(X_train, y_temp_train)

    weather_model = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', MultiOutputClassifier(RandomForestClassifier()))
    ])
    weather_model.fit(X_train_cls, y_cls_train)

    joblib.dump(temp_model, 'temperature_model.pkl')
    joblib.dump(weather_model, 'weather_model.pkl')

if __name__ == '__main__':
    train_and_save_model()
