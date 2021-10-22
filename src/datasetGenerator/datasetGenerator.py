# Used to generate the output dataset schema
# based on parameters specified in the yaml
# configuration file.
import os


class DatasetGenerator(object):
    def __init__(self, outputPath):
        self.outputPath = outputPath
        # Used to initialize the root folder
        # where the dataset will be generated.
        self.createFolder(self.outputPath)

    def __call__(
        self, summaries, generatePdfData=False, arxivPdfEngine=None, pdfLinks=None
    ):
        queryFoldersInfo = self.createFolderStructureQuery(summaries)
        self.writeSummariesToDatasetPath(summaries, queryFoldersInfo)
        if generatePdfData:
            print("Starting to generate PDFs for: {}".format(queryFoldersInfo))
            self.writePdfContentsToDatasetPath(
                arxivPdfEngine, pdfLinks, queryFoldersInfo
            )
        return

    def writePdfContentsToDatasetPath(self, arxivPdfEngine, pdfLinks, queryFoldersInfo):
        for currQueryFolderName in queryFoldersInfo:
            currLinkPdf = pdfLinks[currQueryFolderName][0]
            # Insert logic to run the arxivPdfEngine on
            # the current PDF link here.
            currPdfContents = arxivPdfEngine.fetchRawPdfContentsFromUrl(currLinkPdf)
            summaryStorePath = self.makeQuerySubFolderPath(currQueryFolderName)
            pdfFilePath = self.writeStringContentsToRawFile(
                currPdfContents,
                summaryStorePath,
                suffixPath="paper.pdf",
                writeMode="wb",
            )
            # Parse the natural language text from the PDF.
            pdfTextContents = arxivPdfEngine.extractPdfTextFromDocument(pdfFilePath)
            self.writeStringContentsToRawFile(
                pdfTextContents, summaryStorePath, suffixPath="paper.txt", writeMode="w"
            )
        return

    def makeQuerySubFolderPath(self, currQueryFolderName):
        queryName, subFolderIndex = currQueryFolderName.split("_")
        summaryStorePath = os.path.join(self.outputPath, queryName, subFolderIndex)
        return summaryStorePath

    def writeSummariesToDatasetPath(self, summaries, queryFoldersInfo):
        for currQueryFolderName in queryFoldersInfo:
            summaryText = summaries[currQueryFolderName][0]
            summaryStorePath = self.makeQuerySubFolderPath(currQueryFolderName)
            self.writeStringContentsToRawFile(summaryText, summaryStorePath)
        return

    def writeStringContentsToRawFile(
        self, fileContents, prefixPath, suffixPath="summary.txt", writeMode="w"
    ):
        outputFilePath = os.path.join(prefixPath, suffixPath)
        with open(outputFilePath, writeMode) as fileObject:
            fileObject.write(fileContents)
        return outputFilePath

    def createFolder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return

    def createFolderStructureQuery(self, summaries):
        # Given the summaries for a particular query term.
        # this method creates the folder structure for that query.
        return self.createDefaultFolderStructure(summaries)

    def createDefaultFolderStructure(self, summaries):
        queryFoldersInfo = list(summaries.keys())
        queryFolderPath = self.createQueryFolder(queryFoldersInfo[0])
        for subFolderName in queryFoldersInfo:
            subFolderIndex = subFolderName.split("_")[1]
            subFolderPath = os.path.join(queryFolderPath, subFolderIndex)
            self.createFolder(subFolderPath)
        return queryFoldersInfo

    def createQueryFolder(self, sampleQueryName):
        suffixPath = sampleQueryName.split("_")[0]
        queryFolderPath = os.path.join(self.outputPath, suffixPath)
        self.createFolder(queryFolderPath)
        return queryFolderPath

    # Add method to write a pdfString to disk as well as
    # the natural language string associated to a pdf to disk.
