from datetime import datetime

import pandas as pd
from pymongo import MongoClient

from dash.config import MONGO_URI
from dash.utils.logger import get_logger

logger = get_logger(__name__)


# TODO: get info from web to update "curr_price"
def update_portfolio(s_name, s_amount, avg_price):
    client = MongoClient(MONGO_URI)
    db = client.dash
    prev_info = db.portfolio.find_one({"stock_name": s_name})
    if prev_info is None:
        curr_info = {
            "stock_name": s_name,
            "stock_amount": s_amount,
            "avg_price": avg_price,
            "curr_price": 10000,
            "last_update": datetime.today(),
        }
        db.portfolio.insert_one(curr_info)
    else:
        avg_price = (
            avg_price * s_amount + prev_info["avg_price"] * prev_info["stock_amount"]
        )
        stock_amount = s_amount + prev_info["stock_amount"]
        avg_price = int(avg_price / stock_amount)
        curr_info = {
            "stock_name": s_name,
            "stock_amount": stock_amount,
            "avg_price": avg_price,
            "curr_price": 10000,
            "last_update": datetime.today(),
        }
        db.portfolio.replace_one({"stock_name": s_name}, curr_info)

    for a in db.portfolio.find():
        logger.debug(a)


def get_portfolio():
    client = MongoClient(MONGO_URI)
    db = client.dash

    portfolio = list(db.portfolio.find())

    return pd.DataFrame(portfolio)
