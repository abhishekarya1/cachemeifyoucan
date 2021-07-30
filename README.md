# 📓 cachemeifyoucan!
Simple link shortener with powerful and efficient webpage archive.

<span style="display:inline-block;">
<!-- <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"> &emsp;&ensp; -->
<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" width="300px"> &emsp;&ensp;&emsp;&ensp;&emsp;
<img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Redis_Logo.svg" width="295px">
</span>

### About
Shortened links that redirects to the original. If the original is down, a cached version of the webpage is displayed.

### Built With
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Redis](https://redis.io/)
- [Heroku](https://www.heroku.com/)

### Libraries used
- [Hashids](https://pypi.org/project/hashids/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Concepts and working
- In-memory data store
- Webpage scraping
- HTML templating
- Character encodings (bytes and strings)

### Endpoints
**/** (`GET`, `POST`) : A link is input on the page by the user and all `<style>` and `<script>` are stripped from it, only plain HTML is kept, hyperlinks are disabled too. The plain HTML code is then encoded using [base64encoding](https://docs.python.org/3/library/base64.html). The `b64_code` is searched in data store and if found, a previously generated `shortid` is returned to the user. If this is the first time that link is being shortened, then a `shortie` is generated (using Hashids library) based on the current timestamp and added to data store alongwith `link` and `b64_code`.

The `link`, `shortid`, and `b64_code` is stored to redis following the given schema:
![redis_schema](/static/images/redis_schema.png)

**/shortid** (`GET`) : `shortid` from the link is lookedup in data store and if not found an "Invalid shortlink!" message is shown to the user. If a valid `shortid` is found, then the corresponding `b64_code` and link values are fetched. If the fetched link is up (returns a success response code 200) then user is redirected to it, else `b64_code` fetched from store is decoded to display cached version of the webpage.


### References
- [Hashes in Redis](https://pythontic.com/database/redis/hash%20-%20add%20and%20remove%20elements)
- [RedisLabs Doc on Redis](https://redislabs.com/ebook/part-1-getting-started/chapter-1-getting-to-know-redis/1-2-what-redis-data-structures-look-like/1-2-4-hashes-in-redis/)
- [Hashids Doc](https://pypi.org/project/hashids/)
- [Guide to Parsing HTML with BeautifulSoup in Python](https://stackabuse.com/guide-to-parsing-html-with-beautifulsoup-in-python)

### Acknowledgements
- [Original idea of base64 encoding on HN](https://news.ycombinator.com/item?id=2464213)
- [URL shortener design and hashids usage](https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite)
- [Original bs4 html scraping method - bumpkin's answer](https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text)

### Further
- [A similar tool](https://archive.is/)
- Save page as an image or pdf format (maybe)
- Add option to view cached page before redirect