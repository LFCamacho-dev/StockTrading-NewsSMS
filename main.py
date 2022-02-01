import os
import requests
import pandas

stock_api_key = os.environ.get("STOCK_API_KEY")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    # "interval": "60min",
    "apikey": stock_api_key,
}


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

def get_stocks():
    response = requests.get(f"https://www.alphavantage.co/query", params=stock_params)
    response.raise_for_status()
    stock_data = response.json()
    # print(stock_data)

    stock_data_df = pandas.DataFrame(stock_data)
    df_sliced = stock_data_df["Time Series (Daily)"].iloc[5:7]

    stock_dif = []
    for day_data in df_sliced:
        stock_dif.append(float(day_data["4. close"]))
        print(day_data["4. close"])

    closing_difference = round((stock_dif[0] - stock_dif[1]) / stock_dif[1] * 100, 2)
    print(closing_difference)

    if closing_difference >= 5:
        print(f"The TSLA stock went up {closing_difference}%")
    elif closing_difference <= -5:
        print(f"The TSLA stock went down {closing_difference}%")


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_api_key = os.environ.get("NEWS_API_KEY")
news_params = {
    "qInTitle": COMPANY_NAME,
    "q": "Tesla",
    "sortBy": "publishedAt",
    "apiKey": news_api_key,
}


def get_news():
    response = requests.get(f"https://newsapi.org/v2/top-headlines", params=news_params)
    response.raise_for_status()
    news_data = response.json()
    for article in range(3):
        print(f"{news_data['articles'][article]}\n")


get_news()









# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors 
are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors 
are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
"""



