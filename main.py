import requests
import datetime as dt
from twilio.rest import Client

today = dt.date.today()
today = today - dt.timedelta(days=1)
yesterday = (today - dt.timedelta(days=1))
today = today.strftime("%Y-%m-%d")
yesterday = yesterday.strftime("%Y-%m-%d")
print(today)
print(yesterday)
print(type(today))
print(type(yesterday))
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
news_api_key = "SECRET"
alpha_vantage_key = "SECRET"
alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": alpha_vantage_key,
}
alpha_response = requests.get(url="https://www.alphavantage.co/query?", params=alpha_params)
alpha_response.raise_for_status()
alpha_data = alpha_response.json()
today_price = alpha_data["Time Series (Daily)"][today]["4. close"]
yesterday_price = alpha_data["Time Series (Daily)"][yesterday]["4. close"]
today_price = int(float(today_price))
yesterday_price = int(float(yesterday_price))
change_of_price = ((today_price - yesterday_price) / yesterday_price) * 100
change_of_price = -1 * int(change_of_price)
print(change_of_price)
if change_of_price > 5 or change_of_price < -5:
    get_news = True
def increase_or_decrease():
    global change_of_price
    if change_of_price <= 0:
        return "🔻"
    elif change_of_price > 0:
        return "🔺"
    else:
        return ""


increase_decrease = increase_or_decrease()
news_params = {
    "q": "TESLA",
    "from": f"{yesterday}",
    "language": "en",
    "pagesize": 10,
    "excludeDomains": "yahoo.com",
    "apikey": news_api_key,
}
news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
news_to_send_title = news_data["articles"][-1]["title"]
news_to_send_content = news_data["articles"][-1]["content"]

account_sid = 'SECRET'
auth_token = 'SECRET'
client = Client(account_sid, auth_token)
message = client.messages.create(
  body= f"TSLA: {increase_decrease}{change_of_price}%\nHeadline: {news_to_send_title}\nBrief: {news_to_send_content}",
  from_='+12765288768',
  to='+SECRET'
)
