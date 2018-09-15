from scrapy import Request, Spider
from urllib.parse import urlencode
import json


class WalmartSpider(Spider):
    name = "WalmartSpider"
    targetURL = 'https://www.walmart.com/search/api/preso?'

    def __init__(self):
        self._parameters = {
            'cat_id': '3944_1060825_447913',
            'prg': 'desktop',
            'page': 1,
            'stores': '2568,5605,5686,2526,5152',
        }

    def getParameters(self):
        return self._parameters

    def start_requests(self):
        return [Request(WalmartSpider.targetURL + urlencode(self._parameters))]

    def parse(self, response):
        responseDict = json.loads(response.text)
        for item in responseDict['items']:
            yield item
        # yield responseDict['requestContext']['itemCount']

        pages = divmod(responseDict['requestContext']['itemCount']['total'],
                       responseDict['requestContext']['itemCount']['pageSize'])
        pages = pages[0] if pages[1] == 0 else pages[0]+1
        page = responseDict['requestContext']['itemCount']['page']

        if page < pages:
            self._parameters['page'] += 1
            yield Request(WalmartSpider.targetURL + urlencode(self._parameters))
