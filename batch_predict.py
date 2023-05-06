import pandas as pd
import datetime
import sys
 
changepoint_prior = float(sys.argv[1])
seasonality_prior = float(sys.argv[2])
 
df = pd.read_csv('data/data.csv', skipfooter=1, engine='python')
print(df.head())

df = df.dropna(axis=0, how='any')
df
 
fuel_type = list(df.columns)[2]
fuel_type
print(fuel_type)
df_for_prophet = df[['datetime', fuel_type]].rename(columns = {'datetime':'ds', fuel_type:'y'})
df_for_prophet['ds'] = pd.to_datetime(df['datetime'])

df_for_prophet=df_for_prophet.head(3000)

X = df_for_prophet.copy()
y = df_for_prophet['y']
proportion_in_training = 0.8
split_index = int(proportion_in_training*len(y))
X_train, y_train = X.iloc[:split_index], y.iloc[:split_index]
X_test, y_test = X.iloc[split_index:], y.iloc[split_index:]
 
print(changepoint_prior)
 
params = {  
    'changepoint_prior_scale': changepoint_prior,
    'seasonality_prior_scale': seasonality_prior,
}
 
from fbprophet import Prophet
m = Prophet(**params)
m.fit(X_train)
 
future = m.make_future_dataframe(periods=int(len(y_test)/2), freq='H')
forecast = m.predict(future)
# forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail() #uncomment to inspect the DataFrame
 
import matplotlib.pyplot as plt
plt.gcf()
fig = m.plot(forecast)
plt.plot(X_test['ds'].dt.to_pydatetime(), X_test['y'], 'r', linewidth = 1, linestyle = '--', label = 'real')
plt.legend()
plt.savefig("results/" + fuel_type + "_results.png")
 
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
 
 
df_cv = cross_validation(m, horizon='1 days')
df_p = performance_metrics(df_cv, rolling_window=1)
 
from domino.data_sources import DataSourceClient

# instantiate a client and fetch the datasource instance
ds = DataSourceClient().get_datasource("Snowflake")
import os
sql = "INSERT INTO hybridworkshop (NAME, LOCATION, PROJECT, TYPE, FUEL, MAE, RMSE) VALUES ('{}', '{}', '{}', 'Job', '{}', '{}', '{}');".format(os.environ.get("DOMINO_STARTING_USERNAME"),os.environ.get("DOMINO_HARDWARE_TIER_ID"),os.environ.get("DOMINO_PROJECT_NAME"),fuel_type,round(df_p['mae'][0], 3),round(df_p['rmse'][0], 3))
ds.query(sql)
 
import json
with open('/mnt/dominostats.json', 'w') as f:
    f.write(json.dumps({"MAE": round(df_p['mae'][0], 3), "RMSE": round(df_p['rmse'][0], 3)}))