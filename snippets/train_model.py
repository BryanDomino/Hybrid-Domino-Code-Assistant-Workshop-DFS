# Using Prophet to predict future demand of our fuel type.

# Prepare the data formatting for use, with the fuel_type = list(df.columns)[2] to pick the fuel type automatically
fuel_type = list(df.columns)[2]
fuel_type
df_for_prophet = df[['datetime', fuel_type]].rename(columns = {'datetime':'ds', fuel_type:'y'})
df_for_prophet['ds'] = pd.to_datetime(df['datetime'])

# Create our training and testing sets from the data
X = df_for_prophet.copy()
y = df_for_prophet['y']
proportion_in_training = 0.8
split_index = int(proportion_in_training*len(y))
X_train, y_train = X.iloc[:split_index], y.iloc[:split_index]
X_test, y_test = X.iloc[split_index:], y.iloc[split_index:]

# Suppress FutureWarning to keep the output clearer
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# import Prophet and train our model!
from fbprophet import Prophet
m = Prophet()
m.fit(X_train)

# save our model file
import pickle
with open("model" + fuel_type + ".pkl", "wb") as f:
      pickle.dump(m, f)
