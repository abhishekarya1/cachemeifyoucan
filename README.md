# 📓 cachemeifyoucan
Simple link shortener with powerful and efficient webpage archive.

<span style="display:inline-block;">
<!-- <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"> &emsp;&ensp; -->
<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" width="300px"> &emsp;&ensp;
<img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Redis_Logo.svg" width="295px"> &emsp;&ensp;
</span>

### About
Shortened links that redirects to the original. If the original is down, a cached version of the webpage is displayed.

### Built With
- Flask
- Redis
- Heroku

### Libraries used
- [Hashids](https://pypi.org/project/hashids/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Concepts and working
- In-memory data store
- Webpage scraping
- HTML templating
- Character encodings

### Endpoints
`/` : A link is input on the page by the user and all `style` and `scripts` are stripped from it, only plain HTML is there, hyperlinks are disabled too. The plain HTML code is then encoded using [base64encoding](https://docs.python.org/3/library/base64.html). The link is lookedup in data store and if found, a previously generated shortid is returned to the user. If this is the first time that link is being shortened, then a shortid is generated (using Hashids library) based on the current timestamp. 

The link, shortid, and base64code is stored to redis following the given schema:
![redis_schema]()

`/shortid` : shortid from the link is lookedup in data store and if not found an "Invalid shortlink!" message is shown to the user. If a valid shortid is found, then the corresponding link value is fetched. If this link is up (returns a success response code) then user is redirected to it, else base64code is fetched from store and decoded to display cached version of the page.


### References
- [Hashes in Redis](https://pythontic.com/database/redis/hash%20-%20add%20and%20remove%20elements)
- [RedisLabs Doc on Redis](https://redislabs.com/ebook/part-1-getting-started/chapter-1-getting-to-know-redis/1-2-what-redis-data-structures-look-like/1-2-4-hashes-in-redis/)
- [Hashids Doc](https://pypi.org/project/hashids/)
- [Guide to Parsing HTML with BeautifulSoup in Python](https://stackabuse.com/guide-to-parsing-html-with-beautifulsoup-in-python)

### Acknowledgements
- [Original idea on HN](https://bit.ly/2H8hMOI)
- [URL shortener design and hashids usage](https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite)
- [original bs4 method - bumpkin's answer](https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text)
- [A similar tool](https://archive.is/)


### Further
- Save page as an image or pdf format (maybe)
- Add option to view cached page before redirect
- No shortid change for duplicate URLs can be a problem