import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. Set your OpenWeatherMap API key
API_KEY = "a53326a11a6cb4729f505258c9ec1dbf"  # Replace with your actual API key
CITY = "Mumbai"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# 2. Fetch data from API
response = requests.get(URL)
data = response.json()

# 3. Parse the data
forecast_list = data['list']

# Extract relevant info
weather_data = []
for forecast in forecast_list:
    dt = datetime.fromtimestamp(forecast['dt'])
    temp = forecast['main']['temp']
    humidity = forecast['main']['humidity']
    weather_data.append({'datetime': dt, 'temperature': temp, 'humidity': humidity})

# 4. Convert to DataFrame
df = pd.DataFrame(weather_data)

# 5. Plotting
plt.figure(figsize=(14, 6))
sns.lineplot(x='datetime', y='temperature', data=df, label='Temperature (°C)', color='orange')
sns.lineplot(x='datetime', y='humidity', data=df, label='Humidity (%)', color='blue')
plt.title(f"5-Day Weather Forecast for {CITY}")
plt.xlabel("Date and Time")
plt.ylabel("Values")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()