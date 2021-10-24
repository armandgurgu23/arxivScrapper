from config.scrapperDefaults import getScrapperYamlConfigFile
from config.partitionerDefaults import getPartitionerYamlConfigFile
from queryEngine.queryEngine import ArxivQueryEngine
from arxivXMLParser.arxivXMLParser import ArxivXMLParser
from datasetGenerator.datasetGenerator import DatasetGenerator
from arxivPdfEngine.arxivPdfEngine import ArxivPdfEngine
from datasetPartitioner.datasetPartitioner import DatasetPartitioner
import argparse
import os

# Wrapper class that handlers executing
# the main logic of the Arxiv Scrapper.


class ScrapperHandler(object):
    def __init__(self, scrapperArgs):
        self.scrapperArgs = scrapperArgs

    def __call__(self):
        yamlConfig = self.getYamlConfigFileWrapper(self.scrapperArgs)
        arxivQueryEngineObject = self.getArxivQueryEngineWrapper(
            yamlConfig.queryEngine.maxResults, yamlConfig.queryEngine.queryFile
        )
        datasetGeneratorObject = self.getDatasetGeneratorWrapper(
            outputPath=yamlConfig.datasetGenerator.outputPath
        )
        arxivPdfEngineObject = self.getArxivPdfEngineWrapper()
        if self.scrapperArgs.partitionDataset and os.path.exists(
            yamlConfig.datasetGenerator.outputPath
        ):
            partitionerYamlConfig = self.getYamlConfigFileWrapper(
                self.scrapperArgs, yamlType="partitioner"
            )
            partitionerObject = self.getDatasetPartitionerWrapper(
                partitionerYamlConfig,
                yamlConfig.datasetGenerator.outputPath,
                arxivQueryEngineObject.queriesToFetch,
            )
            partitionerObject()
        elif self.scrapperArgs.partitionDataset and not os.path.exists(
            yamlConfig.datasetGenerator.outputPath
        ):
            self.runScraperAndGenerateDataset(
                yamlConfig,
                arxivQueryEngineObject,
                datasetGeneratorObject,
                arxivPdfEngineObject,
            )
            partitionerYamlConfig = self.getYamlConfigFileWrapper(
                self.scrapperArgs, yamlType="partitioner"
            )
            partitionerObject = self.getDatasetPartitionerWrapper(
                partitionerYamlConfig,
                yamlConfig.datasetGenerator.outputPath,
                arxivQueryEngineObject.queriesToFetch,
            )
            partitionerObject()
        else:
            # Extract all raw data without any sort of partitioning.
            self.runScraperAndGenerateDataset(
                yamlConfig,
                arxivQueryEngineObject,
                datasetGeneratorObject,
                arxivPdfEngineObject,
            )
        return

    def runScraperAndGenerateDataset(
        self,
        yamlConfig,
        arxivQueryEngineObject,
        datasetGeneratorObject,
        arxivPdfEngineObject,
    ):
        for rawQueryResult, currentQuery in arxivQueryEngineObject:
            parsedQueryResult = self.getArxivXMLParserWrapper(
                rawQueryResult, yamlConfig.queryEngine.maxResults, currentQuery
            )
            summaries, entries = parsedQueryResult.extractSummariesFromEntries(
                parsedQueryResult.xmlElementTree
            )
            pdfLinks = parsedQueryResult.extractPaperPdfURLsFromEntries(entries)
            datasetGeneratorObject(
                summaries,
                generatePdfData=True,
                arxivPdfEngine=arxivPdfEngineObject,
                pdfLinks=pdfLinks,
            )
        print(
            "Finished running scraper and generated dataset at {}!".format(
                yamlConfig.datasetGenerator.outputPath
            )
        )
        return

    def getDatasetPartitionerWrapper(
        self, partitionerConfig, datasetPath, queriesToPartition
    ):
        return DatasetPartitioner(
            partitionerConfig=partitionerConfig,
            datasetPath=datasetPath,
            queriesToPartition=queriesToPartition,
        )

    def getYamlConfigFileWrapper(self, scrapperArgs, yamlType="scrapper"):
        if yamlType == "scrapper":
            return getScrapperYamlConfigFile(scrapperArgs.scrapperYaml)
        elif yamlType == "partitioner":
            return getPartitionerYamlConfigFile(scrapperArgs.partitionerConfig)

    def getArxivQueryEngineWrapper(self, maxResults, queriesFilePath):
        return ArxivQueryEngine(maxResults=maxResults, queriesFilePath=queriesFilePath)

    def getArxivXMLParserWrapper(self, sampleQueryResult, maxResults, queryEntry):
        return ArxivXMLParser(
            rawXMLContents=sampleQueryResult,
            maxResults=maxResults,
            queryEntry=queryEntry,
        )

    def getDatasetGeneratorWrapper(self, outputPath):
        return DatasetGenerator(outputPath=outputPath)

    def getArxivPdfEngineWrapper(self):
        return ArxivPdfEngine()


def getScrapperArguments():
    parser = argparse.ArgumentParser(
        description="Program that scrapes research papers natural language text from arxiv.org."
    )
    parser.add_argument(
        "--scrapperYaml",
        type=str,
        default="config/scrapperConfig.yaml",
        help="Path to the yaml file describing the scrapper configuration.",
    )
    parser.add_argument(
        "--partitionDataset",
        type=bool,
        default=True,
        help="Whether to partition the dataset into a train-valid-test split.",
    )
    parser.add_argument(
        "--partitionerConfig",
        type=str,
        default="config/partitionerConfig.yaml",
        help="Configuration settings for the dataset partitioner to use.",
    )
    return parser.parse_args()


def scrapperRunner():
    scrapperArgs = getScrapperArguments()
    scrapperHandlerObject = ScrapperHandler(scrapperArgs)
    scrapperHandlerObject()
    return


if __name__ == "__main__":
    scrapperRunner()
