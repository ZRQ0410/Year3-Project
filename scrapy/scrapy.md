# Scrapy

- From small to large scale
- Lots of built in features: data extraction from HTML, automatic data formatting, use middlewares to save data into databases, concurrency, run a spider on a regular basis

**Virtual environment**
For each project, the third party libraries installed with certain version are specific to that project. (not affected by other projects)
1. Create virtual environment: `% python -m venv envName`
2. Activate the encironment: `%  envName/Scripts/activate` (for Windows)
3. Then download scrapy: `% pip install scrapy`
4. Check download success: `% scrapy`

### Scrapy project
Start a new scrapy project: `% scrapy startproject projectName`
Create a spider: go to scraper/spiders `% scrapy genspider spiderName URL`
Use scrapy shell: `% scrapy shell` `% exit`

Useful:
- Scrape the page: `fetch(URL)`
- Get the reponse: `response`
- Get some element (object) from the response: `response.css(cssSelector)` 
eg. (tag1 tag2.className) or (.className) `response.css('article.product_pod')` `response.css('h3 a::text')` `response.css('.product_price .price_color::text')`
- Get the html from the object: `.get()`
- Get the attribute of the object: `.attrib['href']`

Run the spider: go to the scraper folder where config file resides `% scrapy crawl spiderName`
Store into csv: `% scrapy crawl spiderName -O name.csv`
To json: `% scrapy crawl spiderName -O name.json`