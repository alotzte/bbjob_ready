from catboost import CatBoostClassifier
import pandas as pd

loaded_model = CatBoostClassifier()
loaded_model.load_model('fire_prediction_final_1.cbm')


def prediction(dataframe):
    X = pd.get_dummies(dataframe)

    data = pd.DataFrame(dataframe, columns=['Age', 'Education', 'MonthlyIncome', 'NumCompaniesWorked', 'OverTime',
       'TotalWorkingYears', 'YearsAtCompany', 'ResumeOnJobSearchSite',
       'CompanyYearsRatio', 'SentMessages', 'ReceivedMessages',
       'MessageRecipients', 'BccMessageCount', 'CcMessageCount',
       'LateReadMessages', 'DaysBetweenReceivedRead', 'RepliedMessages',
       'SentMessageCharacters', 'OffHoursSentMessages', 'ReceivedSentRatio',
       'ReceivedSentBytesRatio', 'UnansweredQuestions',
       'MaritalStatus_Divorced', 'MaritalStatus_Married',
       'MaritalStatus_Single'])
    data.fillna(0,inplace=True)
    data = data.merge(X,'right')
    predictions = loaded_model.predict_proba(data)

    return predictions[0][1]

