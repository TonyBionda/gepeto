from django.http import JsonResponse
from joblib import load
import pandas as pd


def load_model():
    # load model
    clf = load('model.joblib')
    return clf


def predict_from_model(full_moon, vacation, match, day_of_week, alert):
    # Get the prediction from the model
    clf = load_model()
    prediction = clf.predict([[full_moon, vacation, match, day_of_week, alert]])
    # Return the prediction
    return prediction.tolist()


def get_date_dataframe(date):
    print("Date : ", date)
    # Get date dataframe
    df = pd.read_csv('dates.csv')
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    df = df.loc[date]
    return df
