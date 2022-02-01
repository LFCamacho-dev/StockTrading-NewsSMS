import os
import random
import requests
import pandas
from twilio.rest import Client

stock_api_key = os.environ.get("STOCK_API_KEY")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    # "interval": "60min",
    "apikey": stock_api_key,
}


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
        send_sms("🔺", closing_difference)
    elif closing_difference <= -5:
        print(f"The TSLA stock went down {closing_difference}%")
        send_sms("🔻", closing_difference)


news_api_key = os.environ.get("NEWS_API_KEY")
news_params = {
    "qInTitle": COMPANY_NAME,
    "q": "Tesla",
    "sortBy": "publishedAt",
    "apiKey": news_api_key,
}

api_key = os.environ.get("APIKEY")
account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("AUTH_TOKEN")


def send_sms(tri, dif):

    response = requests.get(f"https://newsapi.org/v2/top-headlines", params=news_params)
    response.raise_for_status()
    news_data = response.json()
    # for article in range(3):
    #     print(f"{news_data['articles'][article]}\n")
    news_article = news_data['articles'][random.randint(0, 2)]
    article_title = news_article["title"]
    article_description = news_article["description"]

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=os.environ.get("TO_TEL"),
        from_=os.environ.get("FROM_TEL"),
        body=f"{STOCK}: {tri}{dif}%\n"
             f"Headline: {article_title}\n"
             f"Brief: {article_description}\n"
    )

    print(f"the ID is: {message.sid}, and the status is: {message.status}")


get_stocks()
