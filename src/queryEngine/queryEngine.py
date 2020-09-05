import urllib
from urllib import request


class ArxivQueryEngine(object):
    def __init__(self, maxResults, queriesFilePath):
        self.maxResults = maxResults
        self.queriesFilePath = queriesFilePath
        # Reads in queries from the query file specified
        # in the yaml config.
        self.queriesToFetch = self.openQueriesFile(self.queriesFilePath)

    def openQueriesFile(self, path):
        allQueryTerms = []
        with open(path, 'r') as fileObj:
            for currLine in fileObj:
                # Remove end of line (enter) character.
                currLine = currLine.strip('\n')
                allQueryTerms.append(currLine)
        return allQueryTerms

    def fetchSingleSearchQuery(self, queryString):
        sampleUrl = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(
            queryString, self.maxResults)
        return self.queryContentsFromUrl(sampleUrl)

    def queryContentsFromUrl(self, urlString):
        # May need to wrap this later in a try/except to handle
        # connection errors.
        urlContents = request.urlopen(urlString).read()
        return urlContents.decode('utf-8')
