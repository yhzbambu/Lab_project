from pyecharts.charts import Kline,Line,Bar,Grid
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker
import pymysql

db = pymysql.connect(
	host='163.18.104.164',
	user='bambu',
	password='test123',
	database="stock",
	port=3306
)
cursor = db.cursor()


bar = (
    Bar(init_opts=opts.InitOpts(width="1600px", height="280px"))
    .add_xaxis(Faker.choose())
    .add_yaxis("商家A", Faker.values())
	.set_global_opts(
		legend_opts = opts.LegendOpts(is_show=False),
	)
)
line = (
	Line()
	.add_xaxis(xaxis_data=Faker.choose())
	.add_yaxis(
		series_name="MA5",
		y_axis=Faker.values(),
		z=10000
	)
	.set_global_opts(
		legend_opts = opts.LegendOpts(is_show=False),
	)
)
line.overlap(bar)
grid_chart = Grid(init_opts=opts.InitOpts(width="1600px", height="280px"))

grid_chart.add(
	line,
	grid_opts=opts.GridOpts(is_show=True),
)

grid_chart.render("bar_base.html")