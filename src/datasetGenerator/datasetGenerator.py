
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

    def __call__(self, summaries, generatePdfData=False, arxivPdfEngine=None):
        self.createFolderStructureQuery(summaries)
        raise NotImplementedError('Finish implementing the actual saving schema for data here.')

    def createFolder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return

    def createFolderStructureQuery(self, summaries):
        # Given the summaries for a particular query term.
        # this method creates the folder structure for that query.
        self.createDefaultFolderStructure(summaries)
        return

    def createDefaultFolderStructure(self, summaries):
        queryFoldersInfo = list(summaries.keys())
        queryFolderPath = self.createQueryFolder(queryFoldersInfo[0])
        for subFolderName in queryFoldersInfo:
            subFolderIndex = subFolderName.split('_')[1]
            subFolderPath = os.path.join(queryFolderPath, subFolderIndex)
            self.createFolder(subFolderPath)
        return

    def createQueryFolder(self, sampleQueryName):
        suffixPath = sampleQueryName.split('_')[0]
        queryFolderPath = os.path.join(self.outputPath, suffixPath)
        self.createFolder(queryFolderPath)
        return queryFolderPath

    # Add method to write a pdfString to disk as well as
    # the natural language string associated to a pdf to disk.
