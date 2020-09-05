import urllib
from urllib import request


class ArxivQueryEngine(object):
    def __init__(self, maxResults, queriesFilePath):
        self.maxResults = maxResults
        self.queriesFilePath = queriesFilePath

    def openQueriesFile(self, path):
        pass

    def fetchSingleSearchQuery(self, queryString):
        sampleUrl = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(
            queryString, self.maxResults)
        return self.queryContentsFromUrl(sampleUrl)

    def queryContentsFromUrl(self, urlString):
        # May need to wrap this later in a try/except to handle
        # connection errors.
        urlContents = request.urlopen(urlString).read()
        return urlContents.decode('utf-8')
