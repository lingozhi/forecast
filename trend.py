from get_data import lottery_data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

def process_ball_features(df, color_prefix, start, end):
    for i in range(start, end + 1):
        col = f'{color_prefix}_{i:02d}'
        target_column = '开奖蓝球号码' if color_prefix == '蓝' else '开奖红球号码'
        df[col] = df[target_column].apply(lambda x: 1 if f'{i:02d}' in (
            x if isinstance(x, (tuple, list)) else str(x).split(',')) else 0)
        df[f'{col}_MA'] = df[col].rolling(window=10).mean()
        df[f'{col}_Slope'] = df[col].rolling(window=10).mean().diff()
        df[f'{col}_odd'] = np.where(i % 2 == 0, 0, 1)  # 更直观的条件表达式
        df[f'{col}_rolling_std'] = df[col].rolling(window=10).std()
    return df

def extract_additional_features(df, window_sizes=[10, 20, 30]):
    for window in window_sizes:
        for col in df.columns:
            if col.startswith('红_') or col.startswith('蓝_'):
                df[f'{col}_freq_{window}'] = df[col].rolling(window=window).mean()
    return df

def train_and_predict_for_all_balls(df, color_prefix, start, end, features):
    model_probabilities = {}
    for i in range(start, end + 1):
        number = f'{color_prefix}_{i:02d}'
        if number in df.columns:
            X = df[features]
            y = df[number]
            if len(y.unique()) > 1:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LogisticRegression(random_state=42, max_iter=1000)
                model.fit(X_train, y_train)
                last_features = X.iloc[[-1]].values.reshape(1, -1)
                proba = model.predict_proba(last_features)[0][1]
                model_probabilities[number] = proba
            else:
                model_probabilities[number] = 0
    return model_probabilities

df = pd.DataFrame(lottery_data)
df = process_ball_features(df, '红', 1, 33)
df = process_ball_features(df, '蓝', 1, 16)
df = extract_additional_features(df)
df.fillna(0, inplace=True)

scaler = StandardScaler()
features = [col for col in df.columns if col.endswith('_MA') or col.endswith('_Slope') or col.endswith('_rolling_std') or col.endswith('_freq_10')]
X_scaled = scaler.fit_transform(df[features])
df[features] = X_scaled

red_probabilities = train_and_predict_for_all_balls(df, '红', 1, 33, features)
blue_probabilities = train_and_predict_for_all_balls(df, '蓝', 1, 16, features)

predicted_reds = sorted(red_probabilities, key=red_probabilities.get, reverse=True)[:6]
predicted_blue = sorted(blue_probabilities, key=blue_probabilities.get, reverse=True)[0]

print("预测的红球号码:", [int(n.split('_')[1]) for n in predicted_reds])
print("预测的蓝球号码:", int(predicted_blue.split('_')[1]))
