from config.scrapperDefaults import getYamlConfigFile
from queryEngine.queryEngine import ArxivQueryEngine
from arxivXMLParser.arxivXMLParser import ArxivXMLParser
import argparse

# Wrapper class that handlers executing
# the main logic of the Arxiv Scrapper.


class ScrapperHandler(object):
    def __init__(self, scrapperArgs):
        self.scrapperArgs = scrapperArgs

    def __call__(self):
        yamlConfig = self.getYamlConfigFileWrapper(self.scrapperArgs)
        print('The yaml config I read in: \n')
        print(yamlConfig)
        arxivQueryEngineObject = self.getArxivQueryEngineWrapper(
            yamlConfig.queryEngine.maxResults, yamlConfig.queryEngine.queryFile)
        print('Query file search terms I read in: \n')
        print(arxivQueryEngineObject.queriesToFetch)
        sampleQueryResult = arxivQueryEngineObject.fetchSingleSearchQuery(
            queryString=arxivQueryEngineObject.queriesToFetch[0])
        parsedQueryResult = self.getArxivXMLParserWrapper(
            sampleQueryResult, yamlConfig.queryEngine.maxResults, arxivQueryEngineObject.queriesToFetch[0])
        summaryQuery = parsedQueryResult.extractSummariesFromEntries(
            parsedQueryResult.xmlElementTree)
        return

    def getYamlConfigFileWrapper(self, scrapperArgs):
        return getYamlConfigFile(scrapperArgs.scrapperYaml)

    def getArxivQueryEngineWrapper(self, maxResults, queriesFilePath):
        return ArxivQueryEngine(maxResults=maxResults, queriesFilePath=queriesFilePath)

    def getArxivXMLParserWrapper(self, sampleQueryResult, maxResults, queryEntry):
        return ArxivXMLParser(rawXMLContents=sampleQueryResult, maxResults=maxResults, queryEntry=queryEntry)


def getScrapperArguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scrapperYaml', type=str, default='config/scrapperConfig.yaml',
                        help='Path to the yaml file describing the scrapper configuration.')
    return parser.parse_args()


def scrapperRunner():
    scrapperArgs = getScrapperArguments()
    scrapperHandlerObject = ScrapperHandler(scrapperArgs)
    scrapperHandlerObject()
    return


if __name__ == "__main__":
    scrapperRunner()
