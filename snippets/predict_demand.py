#Once we have trained the model we can use it to predict future energy production needs:
future = m.make_future_dataframe(periods=int(len(y_test)/2), freq='H')
forecast = m.predict(future)

# Suppress FutureWarning to keep the output clearer
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

#And create a visualisation of it:
import matplotlib.pyplot as plt
plt.gcf()
fig = m.plot(forecast)
plt.plot(X_test['ds'].dt.to_pydatetime(), X_test['y'], 'r', linewidth = 1, linestyle = '--', label = 'real')
plt.legend()
