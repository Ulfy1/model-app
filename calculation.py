import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import tensorflow as tf

def calculate(age, sex, bmi, children, smoker, region):
    data = {"age":[age],
        "sex":[sex],
        "bmi":[bmi],
        "children":[children],
        "smoker":[smoker],
        "region":[region]}
    
    print(type(bmi))

    for key in data.keys():
        if type(data[key][0]) == str:
            data[key][0] = data[key][0].lower()

    df = pd.DataFrame(data)

    insurance = pd.read_csv("insurance.csv")
    X = insurance.drop("charges", axis=1)
            
    ct = make_column_transformer(
        (MinMaxScaler(), ["age", "bmi", "children"]),
        (OneHotEncoder(handle_unknown="ignore"), ["sex", "smoker", "region"])
    )

    ct.fit(insurance)

    normalized_df = ct.transform(df)
    
    model = tf.keras.models.load_model("model.keras")

    result = model.predict(normalized_df)

    return int(result[0])
