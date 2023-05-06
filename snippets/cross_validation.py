# Do Some Cross Validation and report the results back to a central database
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from domino.data_sources import DataSourceClient
import os

# Prophet cross validation
df_cv = cross_validation(m, initial='45 days', horizon='45 days')
df_p = performance_metrics(df_cv, rolling_window=1)

# Write the output to Snowflake
ds = DataSourceClient().get_datasource("Snowflake")
sql = "INSERT INTO hybridworkshop (NAME, LOCATION, PROJECT, TYPE, FUEL, MAE, RMSE) VALUES ('{}', '{}', '{}', 'Workspace', '{}', '{}', '{}');".format(os.environ.get("DOMINO_STARTING_USERNAME"),os.environ.get("DOMINO_HARDWARE_TIER_ID"),os.environ.get("DOMINO_PROJECT_NAME"),fuel_type,round(df_p['mae'][0], 3),round(df_p['rmse'][0], 3))
ds.query(sql)

# Lastly, print the performance metric results out
print(df_p)