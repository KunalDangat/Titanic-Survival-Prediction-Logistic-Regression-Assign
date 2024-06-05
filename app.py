# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qUyHt5YAIBYpfPDoM-QTHgSoVF5CfZPn
"""

#pip install streamlit

import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('logistic_model.pkl')

# Title
st.title("Titanic Survival Prediction App")

# Sidebar for user input parameters
st.sidebar.header('User Input Features')

def user_input_features():
    PassengerId = st.sidebar.number_input('PassengerId', min_value=1, max_value=100000, value=1)
    Pclass = st.sidebar.selectbox('Pclass', (1, 2, 3))
    Age = st.sidebar.slider('Age', 0, 100, 25)
    SibSp = st.sidebar.slider('SibSp', 0, 10, 0)
    Parch = st.sidebar.slider('Parch', 0, 10, 0)
    Fare = st.sidebar.slider('Fare', 0.0, 500.0, 50.0)
    Sex = st.sidebar.selectbox('Sex', ('male', 'female'))
    Embarked = st.sidebar.selectbox('Embarked', ('C', 'Q', 'S'))

    data = {
        'PassengerId': PassengerId,
        'Pclass': Pclass,
        'Age': Age,
        'SibSp': SibSp,
        'Parch': Parch,
        'Fare': Fare,
        'Sex': Sex,
        'Embarked': Embarked
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Encode categorical variables
def encode_categorical(df):
    df['Sex'] = df['Sex'].map({'male': 1, 'female': 0})
    df = pd.get_dummies(df, columns=['Embarked'], drop_first=False)
    return df

input_df = encode_categorical(input_df)

# Ensure all columns are present
required_columns = ['PassengerId', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_female','Sex_male', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
for col in required_columns:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[required_columns]

# Display user input
st.subheader('User Input Features')
st.write(input_df)

# Prediction
prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)

# Display prediction
st.subheader('Prediction')
if prediction == 1:
    st.write("The passenger is predicted to survive.")
else:
    st.write("The passenger is predicted to not survive.")

# Display prediction probability
st.subheader('Prediction Probability')
st.subheader("Prediction Probability")
proba_df = pd.DataFrame({
    'Probability of Not Surviving': [prediction_proba[0]],
    'Probability of Surviving': [prediction_proba[1]]
})
st.write(proba_df)
