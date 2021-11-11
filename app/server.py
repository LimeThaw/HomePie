from flask import Flask, render_template
import redis
import os

app = Flask(__name__)
redis_hostname = os.environ.get('REDIS_HOSTNAME', "redis")
print(f"Redis run on: {redis_hostname} \n")
cache = redis.Redis(host=redis_hostname, port=6379)

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

@app.route("/inc_clicks")
def inc_clicks():
	current = get_clicks()
	new = current+1
	cache.set("clicks", new)
	return {"clicks": new}

@app.route("/dec_clicks")
def dec_clicks():
	current = get_clicks()
	new = current-1
	cache.set("clicks", new)
	return {"clicks": new}

