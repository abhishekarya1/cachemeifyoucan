from redis import Redis
from hashids import Hashids
from datetime import datetime
import re

redis = Redis(
     host= 'localhost',
     port= '6379')

link = str(input())

hashid = Hashids(salt="this is my salt", min_length = 4)
shortid = hashid.encode(int(datetime.today().timestamp()))

#strip the url for spaces
clean_link = link.strip()

#to avoid '/' or '?' at the end creating duplicate entries in db
if clean_link[-1:] in ['/', '?']:
    clean_link = clean_link[:-1]
    
#store field-value pair to key(link_hash) in Redis; duplicates fields get overwritten
redis.hset(clean_link, shortid, "base64code")
value = redis.keys()
print(value)