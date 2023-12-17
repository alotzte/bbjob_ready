from catboost import CatBoostClassifier
import pandas as pd

loaded_model = CatBoostClassifier()
loaded_model.load_model('fire_prediction_final_1.cbm')


def prediction(dataframe):
    X = pd.get_dummies(dataframe)

    data = pd.DataFrame(dataframe, columns=['Age', 'DistanceFromHome', 'Education', 'MonthlyIncome', 'MonthlyRate',
       'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears',
       'TrainingTimesLastYear', 'YearsAtCompany', 'YearsWithCurrManager',
       'SentMessages', 'ReceivedMessages', 'AddressCount', 'BccCount',
       'CcCount', 'HoursToRead', 'DaysBetweenReceiveRead', 'RepliedMessages',
       'OutgoingMessageLength', 'MessagesOutsideWork', 'SentReceivedRatio',
       'DataVolumeRatio', 'UnansweredQuestions', 'BusinessTravel_Non-Travel',
       'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
       'MaritalStatus_Divorced', 'MaritalStatus_Married',
       'MaritalStatus_Single', 'OverTime_No', 'OverTime_Yes'])
    data.fillna(0,inplace=True)
    data = data.merge(X,'right')
    predictions = loaded_model.predict_proba(data)

    return predictions[0][1]

