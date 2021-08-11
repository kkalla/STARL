from bokeh.client import pull_session
from bokeh.embed import server_session
from config import BOKEH_APP_URL_ROOT, SECRET_KEY
from db_model import update_portfolio
from flask import Flask, flash, redirect, render_template, request, url_for
from utils.logger import get_logger

app = Flask(__name__)
app.secret_key = SECRET_KEY

logger = get_logger(__name__)


@app.route("/")
def main_page():
    pie_url = f"{BOKEH_APP_URL_ROOT}/portfolio_pie"
    with pull_session(url=pie_url) as session:
        # update or customize that session
        session.document.roots[0].title.text = "Special sliders for a specific user!"
        script = server_session(session_id=session.id, url=pie_url)
    return render_template("index.html", script=script, template="Flask")


@app.route("/addStock", methods=["GET"])
def add_stock():
    stock_name = request.args.get("stockName")
    try:
        stock_amount = int(request.args.get("stockAmount"))
    except:
        flash(f"수량은 숫자!", category="error")
        return render_template("index.html")
    try:
        avg_price = int(request.args.get("avgPrice"))
    except:
        flash(f"평균단가는 숫자!", category="error")
        return render_template("index.html")
    logger.debug(f"stock_name => {stock_name}\n stock_amount => {stock_amount}")
    logger.debug(f"avg_price => {avg_price}")
    update_portfolio(stock_name, stock_amount, avg_price)
    flash("Update success!")

    return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
