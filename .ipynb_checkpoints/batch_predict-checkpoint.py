import pandas as pd
import datetime
import sys
from fbprophet import Prophet

# take in the priors as command line arguments
changepoint_prior = float(sys.argv[1])
seasonality_prior = float(sys.argv[2])
 
# Read our data from the mounted data folder in our execution. This is configured to be different data in each region
df = pd.read_csv('data/data.csv', skipfooter=1, engine='python')
print(df.head())

# Prepare the data for retraining
df = df.dropna(axis=0, how='any')
df
 
fuel_type = list(df.columns)[2]
fuel_type
print(fuel_type)
df_for_prophet = df[['datetime', fuel_type]].rename(columns = {'datetime':'ds', fuel_type:'y'})
df_for_prophet['ds'] = pd.to_datetime(df['datetime'])

# Select the first 3000 records - this is simply to shorten the training time in the workshop
df_for_prophet=df_for_prophet.head(3000)

X = df_for_prophet.copy()
y = df_for_prophet['y']
proportion_in_training = 0.8
split_index = int(proportion_in_training*len(y))
X_train, y_train = X.iloc[:split_index], y.iloc[:split_index]
X_test, y_test = X.iloc[split_index:], y.iloc[split_index:]
 
# Configure the parameters for our model training
print(changepoint_prior)
 
params = {  
    'changepoint_prior_scale': changepoint_prior,
    'seasonality_prior_scale': seasonality_prior,
}

m = Prophet(**params)
m.fit(X_train)
 
future = m.make_future_dataframe(periods=int(len(y_test)/2), freq='H')
forecast = m.predict(future)
# forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail() #uncomment to inspect the DataFrame
 
# Save our prediction results as a graph into our results folder.
import matplotlib.pyplot as plt
plt.gcf()
fig = m.plot(forecast)
plt.plot(X_test['ds'].dt.to_pydatetime(), X_test['y'], 'r', linewidth = 1, linestyle = '--', label = 'real')
plt.legend()
plt.savefig("results/" + fuel_type + "_results.png")

# Perform cross validation to access the accuracy of the model with our given training parameters
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
 
 
df_cv = cross_validation(m, horizon='1 days')
df_p = performance_metrics(df_cv, rolling_window=1)
 
from domino.data_sources import DataSourceClient

# report back to the central DB our findings
ds = DataSourceClient().get_datasource("Snowflake")
import os
sql = "INSERT INTO hybridworkshop (NAME, LOCATION, PROJECT, TYPE, FUEL, MAE, RMSE) VALUES ('{}', '{}', '{}', 'Job', '{}', '{}', '{}');".format(os.environ.get("DOMINO_STARTING_USERNAME"),os.environ.get("DOMINO_HARDWARE_TIER_ID"),os.environ.get("DOMINO_PROJECT_NAME"),fuel_type,round(df_p['mae'][0], 3),round(df_p['rmse'][0], 3))
ds.query(sql)

# This snippet populates the dashboard in the Domino Jobs UI to keep track of the high level results.
import json
with open('/mnt/dominostats.json', 'w') as f:
    f.write(json.dumps({"MAE": round(df_p['mae'][0], 3), "RMSE": round(df_p['rmse'][0], 3)}))