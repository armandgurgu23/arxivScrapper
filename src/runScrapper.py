from config.scrapperDefaults import getYamlConfigFile
from queryEngine.queryEngine import ArxivQueryEngine
from arxivXMLParser.arxivXMLParser import ArxivXMLParser
from datasetGenerator.datasetGenerator import DatasetGenerator
import argparse

# Wrapper class that handlers executing
# the main logic of the Arxiv Scrapper.


class ScrapperHandler(object):
    def __init__(self, scrapperArgs):
        self.scrapperArgs = scrapperArgs

    def __call__(self):
        yamlConfig = self.getYamlConfigFileWrapper(self.scrapperArgs)
        # print('The yaml config I read in: \n')
        # print(yamlConfig)
        arxivQueryEngineObject = self.getArxivQueryEngineWrapper(
            yamlConfig.queryEngine.maxResults, yamlConfig.queryEngine.queryFile)
        datasetGeneratorObject = self.getDatasetGeneratorWrapper(
            outputPath=yamlConfig.datasetGenerator.outputPath)
        self.runScraperAndGenerateDataset(
            yamlConfig, arxivQueryEngineObject, datasetGeneratorObject)
        # print('Query file search terms I read in: \n')
        # print(arxivQueryEngineObject.queriesToFetch)
        # sampleQueryResult = arxivQueryEngineObject.fetchSingleSearchQuery(
        #     queryString=arxivQueryEngineObject.queriesToFetch[0])
        # parsedQueryResult = self.getArxivXMLParserWrapper(
        #     sampleQueryResult, yamlConfig.queryEngine.maxResults, arxivQueryEngineObject.queriesToFetch[0])
        # summaries, entries = parsedQueryResult.extractSummariesFromEntries(
        #     parsedQueryResult.xmlElementTree)
        # pdfLinks = parsedQueryResult.extractPaperPdfURLsFromEntries(entries)
        # print(summaries)
        # print(summaries.keys())
        # print('The summaries are above! ')
        # print(pdfLinks)
        # print('The pdf links are above! ')
        # print(summaries['electron_0'])
        # print(pdfLinks['electron_0'])
        # print('Sample summary and URL above! ')
        return

    def runScraperAndGenerateDataset(self, yamlConfig, arxivQueryEngineObject, datasetGeneratorObject):
        for rawQueryResult, currentQuery in arxivQueryEngineObject:
            parsedQueryResult = self.getArxivXMLParserWrapper(
                rawQueryResult, yamlConfig.queryEngine.maxResults, currentQuery)
            summaries, entries = parsedQueryResult.extractSummariesFromEntries(
                parsedQueryResult.xmlElementTree)
            pdfLinks = parsedQueryResult.extractPaperPdfURLsFromEntries(entries)
            # TO DO: implement arxiv pdf engine logic and run it inside data
            # generator __call__ method.
            datasetGeneratorObject(summaries, generatePdfData=False, arxivPdfEngine=None)
        print('Finished running scraper and generated dataset at {}!'.format(
            yamlConfig.datasetGenerator.outputPath))
        return

    def getYamlConfigFileWrapper(self, scrapperArgs):
        return getYamlConfigFile(scrapperArgs.scrapperYaml)

    def getArxivQueryEngineWrapper(self, maxResults, queriesFilePath):
        return ArxivQueryEngine(maxResults=maxResults, queriesFilePath=queriesFilePath)

    def getArxivXMLParserWrapper(self, sampleQueryResult, maxResults, queryEntry):
        return ArxivXMLParser(rawXMLContents=sampleQueryResult, maxResults=maxResults, queryEntry=queryEntry)

    def getDatasetGeneratorWrapper(self, outputPath):
        return DatasetGenerator(outputPath=outputPath)


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
