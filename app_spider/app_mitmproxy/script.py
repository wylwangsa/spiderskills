import json
import pymongo
from mitmproxy import ctx

MONGO_URL ='localhost'
MONGO_DB = 'igetget'
MONGO_COLLECTION = 'books'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def response(flow):
	url = 'https://dedao.igetget.com/v3/discover/bookList'
	if flow.request.url.startswith(url):
		text = flow.response.text
		data = json.loads(text)
		books = data.get('c').get('list')
		for book in books:

			data = {
				'title':book.get('operating_title'),
				'cover':book.get('cover'),
				'summary':book.get('other_share_summary'),
				'price':book.get('price')
			}
			ctx.log.info(str(data))
			db[MONGO_COLLECTION].insert(data)
