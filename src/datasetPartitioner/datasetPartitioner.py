import os
from shutil import copytree
from random import sample
from datasetGenerator.datasetGenerator import DatasetGenerator


class DatasetPartitioner(DatasetGenerator):
    def __init__(self, partitionerConfig, datasetPath, queriesToPartition):
        self.partitionerConfig = partitionerConfig
        self.datasetPath = datasetPath
        self.queriesToPartition = queriesToPartition
        self.excludeFiles = {".DS_Store"}
        self.trainSplit = self.partitionerConfig.partitioner.totalTrainSplit
        self.validSplit = self.partitionerConfig.partitioner.totalValidSplit
        self.testSplit = self.partitionerConfig.partitioner.totalTestSplit
        self.createFolder(self.partitionerConfig.partitioner.partitionOutputPath)

    def __call__(self):
        paperPaths, totalPapers = self.getTotalPapersExtractedInfo(self.datasetPath)
        categorySplits = self.computePerPaperCategorySplits(totalPapers)
        categorySplits, paperPaths = self.selectPapersForSplits(
            categorySplits, paperPaths
        )
        categorySplits, paperPaths = self.assignRemainingPapersAtRandom(
            categorySplits, paperPaths
        )
        self.validateSplitsAndCounts(categorySplits, totalPapers)
        self.writeDatasetSplitsToPath(
            self.partitionerConfig.partitioner.partitionOutputPath,
            categorySplits,
            osMethodForWriting=copytree,
        )
        return

    def writeDatasetSplitsToPath(
        self, partitionedDatasetPath, categorySplits, osMethodForWriting
    ):
        for currSplit in categorySplits:
            splitBasePath = os.path.join(partitionedDatasetPath, currSplit)
            self.createFolder(splitBasePath)
            for currCategory in categorySplits[currSplit]["paths"]:
                for currPaperIndex, currPaperPath in enumerate(
                    categorySplits[currSplit]["paths"][currCategory]
                ):
                    paperSplitOutPath = os.path.join(
                        splitBasePath, f"{currCategory}_{currPaperIndex}"
                    )
                    osMethodForWriting(src=currPaperPath, dst=paperSplitOutPath)
        return

    def validateSplitsAndCounts(self, categorySplits, totalPapers):
        # Sanity check to ensure partitioning has gone well and no paper was shared
        # between splits.
        totalCategoryCount = 0
        for currCategory in self.queriesToPartition:
            currCategoryPathsTrain = set(categorySplits["train"]["paths"][currCategory])
            currCategoryPathsValid = set(categorySplits["valid"]["paths"][currCategory])
            currCategoryPathsTest = set(categorySplits["test"]["paths"][currCategory])
            assert (
                currCategoryPathsTrain.intersection(currCategoryPathsValid) == set()
            ), "Found overlapping papers between train-valid splits!"
            assert (
                currCategoryPathsTrain.intersection(currCategoryPathsTest) == set()
            ), "Found overlapping papers between train-test splits!"
            totalPerCategory = (
                len(currCategoryPathsTrain)
                + len(currCategoryPathsValid)
                + len(currCategoryPathsTest)
            )
            totalCategoryCount += totalPerCategory
        # Lastly, check that there are no remaining papers to be assigned!
        assert (
            totalCategoryCount == totalPapers
        ), f"{totalPapers - totalCategoryCount} papers from dataset have not been to a partition!"
        print("All validation checks for partitioning have passed successfully!")
        return

    def assignRemainingPapersAtRandom(self, categorySplits, paperPaths):
        splitChoices = list(categorySplits.keys())
        for currCategory in paperPaths:
            for currPaperIndex in range(paperPaths[currCategory]["count"]):
                # Select which dataset current paper will go to.
                splitTypeChosen = sample(splitChoices, 1)[0]
                paperPathToAssign = paperPaths[currCategory]["paths"][currPaperIndex]
                categorySplits[splitTypeChosen]["paths"][currCategory].append(
                    paperPathToAssign
                )
            paperPaths[currCategory]["count"] = 0
            paperPaths[currCategory]["paths"] = []
        return categorySplits, paperPaths

    def selectPapersForSplits(self, categorySplits, paperPaths):
        for currSplitType in categorySplits:
            for currCategory in paperPaths:
                papersPerCategory = min(
                    categorySplits[currSplitType]["perCategory"],
                    paperPaths[currCategory]["count"]
                    - self.partitionerConfig.partitioner.minCategorySamplesPerSplit,
                )
                categorySplits[currSplitType]["paths"][currCategory] = []
                for currentIndex in range(papersPerCategory):
                    currPaperPathSelected = paperPaths[currCategory]["paths"][
                        currentIndex
                    ]
                    categorySplits[currSplitType]["paths"][currCategory].append(
                        currPaperPathSelected
                    )
                # Remove the selected examples from the full paper paths dictionary to avoid
                # sharing examples between partitions.
                newPathsForCat = set(paperPaths[currCategory]["paths"]) - set(
                    categorySplits[currSplitType]["paths"][currCategory]
                )
                paperPaths[currCategory]["paths"] = list(newPathsForCat)
                paperPaths[currCategory]["count"] = len(newPathsForCat)
        return categorySplits, paperPaths

    def computePerPaperCategorySplits(self, totalPapers):
        categorySplitsDict = {"train": {}, "valid": {}, "test": {}}
        totalTrain = self.trainSplit * totalPapers
        totalValid = self.validSplit * totalPapers
        totalTest = self.testSplit * totalPapers
        perCategoryTrain = int(totalTrain / len(self.queriesToPartition))
        perCategoryValid = int(totalValid / len(self.queriesToPartition))
        perCategoryTest = int(totalTest / len(self.queriesToPartition))
        categorySplitsDict["train"]["total"] = totalTrain
        categorySplitsDict["train"]["perCategory"] = perCategoryTrain
        categorySplitsDict["train"]["paths"] = {}
        categorySplitsDict["valid"]["total"] = totalValid
        categorySplitsDict["valid"]["perCategory"] = perCategoryValid
        categorySplitsDict["valid"]["paths"] = {}
        categorySplitsDict["test"]["total"] = totalTest
        categorySplitsDict["test"]["perCategory"] = perCategoryTest
        categorySplitsDict["test"]["paths"] = {}
        return categorySplitsDict

    def getTotalPapersExtractedInfo(self, datasetPath):
        currPath = os.getcwd()
        allPaperPaths = self.initializePaperSamplesDicts(self.queriesToPartition)
        datasetPathAbs = os.path.join(currPath, datasetPath)
        totalPapersCount = 0
        for currentQueryType in os.listdir(os.chdir(datasetPathAbs)):
            if currentQueryType not in self.queriesToPartition:
                continue
            queryTypeDataPath = os.path.join(datasetPathAbs, currentQueryType)
            for currentPaperPath in os.listdir(os.chdir(queryTypeDataPath)):
                if currentPaperPath in self.excludeFiles:
                    continue
                allPaperPaths[currentQueryType]["paths"].append(
                    os.path.join(queryTypeDataPath, currentPaperPath)
                )
                allPaperPaths[currentQueryType]["count"] += 1
            totalPapersCount += allPaperPaths[currentQueryType]["count"]
        os.chdir(currPath)
        return allPaperPaths, totalPapersCount

    def initializePaperSamplesDicts(self, queriesToPartition):
        outputDict = {}
        for currentQuery in queriesToPartition:
            outputDict[currentQuery] = {}
            outputDict[currentQuery]["paths"] = []
            outputDict[currentQuery]["count"] = 0
        return outputDict
