import base64
from datetime import datetime
import re
import urllib.request

from flask import Flask, render_template, request, redirect
from hashids import Hashids
from redis import Redis

#custom
import constants
from utils import get_html, link_cleaner

app = Flask(__name__)

redis = Redis(host= constants.REDIS_HOST, port= constants.REDIS_PORT, db=0)

#routes
@app.route("/", methods=['GET', 'POST'])
def gen_shortlink():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		link = request.form["link"]
		#scrape text
		webpage = urllib.request.urlopen(link).read()
		html = get_html(webpage)

		#base64encode html content
		b64_code = base64.b64encode(bytes(str(html), 'utf-8'))
	
		#clean link to get rid of '/' or '?' at the end
		clean_link = link_cleaner(link)

		shortid = None
		#store field-value pair to key/hash(linkIndex) in Redis; duplicates keys get overwritten
		if len(redis.keys(pattern=clean_link)) == 0:
			#generate shortid from current timestamp
			hashid = Hashids(salt=constants.HASHID_SALT, min_length = 4)
			shortid = hashid.encode(int(datetime.today().timestamp()))
		
			#store field-value pair to key/hash(clean_link) in Redis
			redis.hset(clean_link, 'shortid', shortid)
			redis.hset(clean_link, 'b64_code', b64_code)
		
			#set link-shortid in linkIndex hash
			redis.hset("linkIndex", shortid, clean_link)
		else:
			shortid = str(redis.hget(clean_link, 'shortid'), 'utf-8')

		#append shortid to baseUrl
		shortlink = constants.BASE_URL + "/" + shortid

		#display shortlink to webpage
		return render_template("index.html", shortlink=shortlink)

@app.route("/<string:shortid>", methods = ['GET'])
def expand_link(shortid):

	#get link from linkIndex hash
	link_b = redis.hget('linkIndex', shortid)

	#if user entered invalid shorlink
	if link_b is None:
		return "Invalid shortlink!"
	#print(link_b)
	#print(type(link_b))
	#browser hits twice with GET :/
	else:
		link = str(link_b, 'utf-8')
	
		#if og_link is up: redirect to og_link
		if urllib.request.urlopen(link).getcode() != 200:		#changed to != for debug
			return redirect(link, code=302)

		#else: render cached version after decoding
		else:
			base64code = str(redis.hget(link, 'b64_code'), 'utf-8')
			cached_html = str(base64.b64decode(base64code), 'utf-8')
			return render_template("cached_html.html", cached_html=cached_html)

#main
if __name__ == '__main__':
	app.run(debug=True)