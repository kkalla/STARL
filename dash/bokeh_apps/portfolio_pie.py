# encoding: utf-8

from math import pi

import numpy as np
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.palettes import Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum

from dash.db_model import get_portfolio

print(__name__)


portfolio = get_portfolio()
portfolio.loc[:, "total"] = portfolio["stock_amount"] * portfolio["curr_price"]
portfolio = portfolio.loc[:, ["stock_name", "total"]]
portfolio["angle"] = portfolio["total"] / portfolio["total"].sum() * 2 * pi
portfolio["color"] = Category20[max(len(portfolio), 3)]
portfolio["portion"] = (portfolio["angle"] / (2 * pi) * 100).astype(int)
portfolio["portion"] = [f"{d}%" for d in portfolio["portion"]]

text_angle = []
curr_end = 0
for angle in portfolio["angle"]:
    text_angle.append((curr_end + (angle / 2)))
    curr_end += angle
text_angle = np.array(text_angle)
xr = 0.2 * np.cos(text_angle)
yr = (0.5 * np.sin(text_angle)) + 1
portfolio["xr"] = xr
portfolio["yr"] = yr

p = figure(
    plot_height=350,
    title="Pie Chart",
    toolbar_location=None,
    tools="hover",
    tooltips="@stock_name: @total",
    x_range=(-0.5, 1.0),
)
p.wedge(
    x=0,
    y=1,
    radius=0.4,
    start_angle=cumsum("angle", include_zero=True),
    end_angle=cumsum("angle"),
    line_color="white",
    fill_color="color",
    legend_field="stock_name",
    source=portfolio,
)
source = ColumnDataSource(portfolio)
labels = LabelSet(
    x="xr", y="yr", text="portion", angle=0, source=source, render_mode="canvas"
)
p.add_layout(labels)
p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

curdoc().add_root(p)
