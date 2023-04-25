from dataframes import get_dataframes
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from pandas._libs.missing import NAType
from joblib import dump


# This function merges all the dataframes into one, with date_debut_sejour as key
def merge_dataframes(df_main, *df_others):
    for df in df_others:
        try:
            df_main = df_main.merge(df, how='left', left_on='DATE_DEBUT_SEJOUR', right_on='Date')
        except Exception as e:
            print(e)
    return df_main


# Main function
if __name__ == "__main__":
    # Get the dataframes
    (df_sejours, df_dates, df_matchs, df_alertes) = get_dataframes()

    # Merge all the dataframes into one
    df_sejours = merge_dataframes(df_sejours, df_dates, df_matchs, df_alertes)

    # Drop the useless columns
    df_sejours = df_sejours.drop(columns=[
        'DateKey', 'Date_x',
        'FullDate', 'MMYYYY',
        'Date_y', 'DATE_x',
        'ID_MATCH', 'Date',
        'DATE_y', 'ID_ALERTE'
    ])

    # Convert the data types of the columns on the correct ones (no NaN)
    df_sejours = df_sejours.convert_dtypes()

    # Create a new class column with "affluence" prediction values
    df_sejours['CLASS'] = df_sejours['NB_ENTREES'].apply(
        lambda
            x: 0 if x < 100 else 1 if 100 <= x < 200 else 2 if 200 <= x < 300 else 3 if 300 <= x < 400 else 4 if 400 <= x < 500 else 5 if 500 <= x < 600 else 6 if 600 <= x < 700 else 7 if 700 <= x < 800 else 8 if 800 <= x < 900 else 9 if 900 <= x < 1000 else 10
    )

    # Show the first 20 rows of the dataframe and the infos (columns, types, etc.)
    df_sejours.head(20)
    df_sejours.info()

    # Add two columns to know if there is a match and an alert on the day of the beginning of the stay
    df_sejours['hasMatch'] = df_sejours['HOME_TEAM'].apply(lambda x: 1 if isinstance(x, NAType) else 0)
    df_sejours['hasAlert'] = df_sejours['TYPE'].apply(lambda x: 1 if isinstance(x, NAType) else 0)

    # Convert the boolean values to 0 and 1
    df_sejours['HolidayZoneA'] = df_sejours['HolidayZoneA'].apply(lambda x: 1 if x == 'VRAI' else 0)
    df_sejours['HolidayZoneB'] = df_sejours['HolidayZoneB'].apply(lambda x: 1 if x == 'VRAI' else 0)
    df_sejours['HolidayZoneC'] = df_sejours['HolidayZoneC'].apply(lambda x: 1 if x == 'VRAI' else 0)

    # Check features names
    feature_names = [
        'IsFullMoon',
        'IsHoliday',
        'hasMatch',
        'DayOfWeek',
        'hasAlert',
    ]

    # Get min and max values from nb_entrees in df_sejours to create the classes
    min_df = df_sejours['NB_ENTREES'].min()
    max_df = df_sejours['NB_ENTREES'].max()

    # Create classes from min and max
    class_names = [i for i in range(min_df, max_df, 100)]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df_sejours[feature_names],
                                                        df_sejours['CLASS'], test_size=0.2, random_state=42)

    # Create a Decision Tree Classifier and train it
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Predict the classes of the testing set
    y_pred = clf.predict(X_test)

    # If you want to export the model and save the visual representation of the tree
    # (graphviz must be installed) :
    # dot_data = tree.export_graphviz(clf, out_file=None, feature_names=feature_names,
    # class_names=class_names,
    # filled=True)
    # graph = graphviz.Source(dot_data, format="pdf")
    # graph.render("decision_tree_graphviz")

    # We now try to predict the affluence on a specific day with specific features :
    day_to_predict = {
        "date": "14/04/2023",
        "features": {
            'IsFullMoon': 0,
            'IsHoliday': 1,
            'hasMatch': 1,
            'DayOfWeek': 5,
            'hasAlert': 0,
        }
    }

    # Create a dataframe with the features of the day to predict
    df_day_to_predict = pd.DataFrame([day_to_predict["features"]])

    # Predict the class of the day to predict
    prediction = clf.predict(df_day_to_predict)

    # Print the prediction
    print(f"Prediction de l'affluence : {class_names[prediction[0]]} personnes en moyenne le {day_to_predict['date']}")

    # Print the accuracy of the model
    print("\n\nAccuracy:{:,.2f}%".format(accuracy_score(y_test, y_pred) * 100))

    # Print the feature importances
    feature_importances = pd.DataFrame(clf.feature_importances_,
                                       index=feature_names,
                                       columns=['importance']).sort_values('importance',
                                                                           ascending=False)
    print(feature_importances)

    # Save the model to use it in the app
    dump(clf, 'model.joblib')
