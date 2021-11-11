from flask import Flask, render_template
import redis
import os

app = Flask(__name__)
redis_hostname = os.environ.get('REDIS_HOSTNAME', "redis")
print(f"Redis run on: {redis_hostname} \n")
cache = redis.Redis(host=redis_hostname, port=6379)

@app.route("/")
def hello():
	clicks = int(cache.get("clicks"))
	return render_template('home.html', clicks=clicks)