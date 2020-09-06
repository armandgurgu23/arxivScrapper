from config.scrapperDefaults import getYamlConfigFile
from queryEngine.queryEngine import ArxivQueryEngine
from arxivXMLParser.arxivXMLParser import ArxivXMLParser
from datasetGenerator.datasetGenerator import DatasetGenerator
from arxivPdfEngine.arxivPdfEngine import ArxivPdfEngine
import argparse

# Wrapper class that handlers executing
# the main logic of the Arxiv Scrapper.


class ScrapperHandler(object):
    def __init__(self, scrapperArgs):
        self.scrapperArgs = scrapperArgs

    def __call__(self):
        yamlConfig = self.getYamlConfigFileWrapper(self.scrapperArgs)
        arxivQueryEngineObject = self.getArxivQueryEngineWrapper(
            yamlConfig.queryEngine.maxResults, yamlConfig.queryEngine.queryFile)
        datasetGeneratorObject = self.getDatasetGeneratorWrapper(
            outputPath=yamlConfig.datasetGenerator.outputPath)
        arxivPdfEngineObject = self.getArxivPdfEngineWrapper()
        self.runScraperAndGenerateDataset(
            yamlConfig, arxivQueryEngineObject, datasetGeneratorObject, arxivPdfEngineObject)
        return

    def runScraperAndGenerateDataset(self, yamlConfig, arxivQueryEngineObject, datasetGeneratorObject, arxivPdfEngineObject):
        for rawQueryResult, currentQuery in arxivQueryEngineObject:
            parsedQueryResult = self.getArxivXMLParserWrapper(
                rawQueryResult, yamlConfig.queryEngine.maxResults, currentQuery)
            summaries, entries = parsedQueryResult.extractSummariesFromEntries(
                parsedQueryResult.xmlElementTree)
            pdfLinks = parsedQueryResult.extractPaperPdfURLsFromEntries(entries)
            datasetGeneratorObject(summaries, generatePdfData=True,
                                   arxivPdfEngine=arxivPdfEngineObject, pdfLinks=pdfLinks)
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

    def getArxivPdfEngineWrapper(self):
        return ArxivPdfEngine()


def getScrapperArguments():
    parser = argparse.ArgumentParser(
        description='Program that scrapes research papers natural language text from arxiv.org.')
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
