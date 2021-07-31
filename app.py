import base64
from datetime import datetime
import re
import urllib.request

from flask import Flask, render_template, request, redirect
from hashids import Hashids
from redis import Redis

#custom
import constants
from utils import get_html, validate_link, link_cleaner

app = Flask(__name__)

redis = Redis(host= constants.REDIS_HOST, port= constants.REDIS_PORT, db=0)

#routes
@app.route("/", methods=['GET', 'POST'])
def gen_shortlink():
	if request.method == 'GET':
		return render_template("index.html")
	elif request.method == 'POST':
		link = request.form["link"]
		if validate_link(link) == False:
			return render_template("index.html", gen="Invalid link!")
		else:	
			#scrape text
			webpage = urllib.request.urlopen(link).read()
			html = get_html(webpage)

			#base64encode html content
			b64_code = base64.b64encode(bytes(str(html), 'utf-8'))
	
			#clean link to get rid of '/' or '?' at the end
			clean_link = link_cleaner(link)

			shortid = None
			#if a link
			if redis.hexists('index', b64_code) is True:
				shortid = str(redis.hget('index', b64_code), 'utf-8')
				gen = "Existing shortlink returned."
			else:
				#generate shortid from current timestamp
				hashid = Hashids(salt=constants.HASHID_SALT, min_length = 4)
				shortid = hashid.encode(int(datetime.today().timestamp()))
		
				#store field-value pair to key/hash(shortid) in Redis
				redis.hset(shortid, 'link', clean_link)
				redis.hset(shortid, 'b64_code', b64_code)
		
				#set b64_code-shortid in index hash
				redis.hset('index', b64_code, shortid)
				gen = "New shortlink generated."

			#append shortid to baseUrl
			shortlink = constants.BASE_URL + "/" + shortid

			#display shortlink to webpage
			return render_template("index.html", shortlink=shortlink, gen=gen)

	else:
		return "Reuest method not allowed!"

@app.route("/<string:shortid>", methods = ['GET'])
def expand_link(shortid):

	#if user entered invalid shorlink; not found in any hash keys
	if len(redis.keys(shortid)) == 0:
		return "Invalid shortlink!"
	#print(link_b)
	#print(type(link_b))
	#browser hits twice with GET :/
	else:
		link = str(redis.hget(shortid, 'link'), 'utf-8')
		base64code = str(redis.hget(shortid, 'b64_code'), 'utf-8')
		#if og_link is up: redirect to og_link
		if urllib.request.urlopen(link).getcode() != 200:		#changed to != for debug
			return redirect(link, code=302)
		#else: render cached version after decoding
		else:
			cached_html = str(base64.b64decode(base64code), 'utf-8')
			return render_template("cached_html.html", cached_html=cached_html)

#main
if __name__ == '__main__':
	app.run(debug=True)