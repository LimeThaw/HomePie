from flask import Flask, render_template
from flask.globals import request
import redis
import os
import util

app = Flask(__name__)
redis_hostname = os.environ.get('REDIS_HOSTNAME', "redis")
print(f"Redis run on: {redis_hostname} \n")
cache = redis.Redis(host=redis_hostname, port=6379)

if __name__ == '__main__':
	sqlite_path = "./debug.db"
else:
	sqlite_path = "/sqlite_data/timeseries.db"
print("SQLite Path: " + sqlite_path)

def get_clicks():
	clicks = cache.get("clicks")
	if not clicks:
		clicks = 0
		cache.set("clicks", clicks)
	else:
		clicks = int(clicks)
		return clicks

@app.route("/")
def hello():
	return render_template('home.html', clicks=get_clicks())
	# return render_template('home.html', clicks=0)

@app.route("/clicks/inc_clicks")
def inc_clicks():
	current = get_clicks()
	new = current+1
	cache.set("clicks", new)
	return {"clicks": new}

@app.route("/clicks/dec_clicks")
def dec_clicks():
	current = get_clicks()
	new = current-1
	cache.set("clicks", new)
	return {"clicks": new}

@app.route("/timeseries/data")
def get_all_timeseries_data():
	sqlite_conn = util.sqlite_connect(sqlite_path)
	tables = util.sqlite_execute(sqlite_conn, "SELECT name FROM sqlite_master WHERE type='table';")
	ret_dict = {}
	for t in tables:
		table_name = t[0]


		# util.sqlite_execute(sqlite_conn, f"INSERT INTO {table_name} (timestamp, value) VALUES (strftime('%s', 'now'), {random.uniform(0.0, 10.0)});")

		t_data = util.sqlite_execute(sqlite_conn, f"SELECT * FROM {table_name} ORDER BY timestamp ASC;")
		ret_dict[table_name] = t_data



	return ret_dict

@app.route("/timeseries/names")
def get_timeseries_names():
	sqlite_conn = util.sqlite_connect(sqlite_path)
	re = util.sqlite_execute(sqlite_conn, "SELECT name FROM sqlite_master WHERE type='table';")
	return {"result": re}

@app.route("/timeseries/add/<name>")
def add_timeseries(name):
	sqlite_conn = util.sqlite_connect(sqlite_path)
	re = util.sqlite_execute(sqlite_conn, "SELECT name FROM sqlite_master WHERE type='table';")
	if name in [x[0] for x in re]:
		return {"result": "Error: Timeseries already exists", "code": -1}

	re = util.sqlite_execute(sqlite_conn,
		"create table if not exists " + name + """(
		timestamp timestamp primary key,
		value float not null
		);""")
	return {"result": re, "code": 0}

@app.route("/timeseries/addvalue", methods=["POST"])
def add_timeseries_value():
	print(request.form.get('series') + " - " + request.form.get('value'))
	
	table_name = request.form.get('series')
	value = request.form.get('value')
	sqlite_conn = util.sqlite_connect(sqlite_path)
	re = util.sqlite_execute(sqlite_conn, "SELECT name FROM sqlite_master WHERE type='table';")
	if not table_name in [x[0] for x in re]:
		return {"result": "Error: Timeseries does not exists", "code": -1}

	re = util.sqlite_execute(sqlite_conn, f"INSERT INTO {table_name} (timestamp, value) VALUES (strftime('%s', 'now'), {value});")
	return {"result": "OK", "code": 0}


@app.teardown_appcontext
def teardown(exception):
	print("teardown")
	util.sqlite_disconnect()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')