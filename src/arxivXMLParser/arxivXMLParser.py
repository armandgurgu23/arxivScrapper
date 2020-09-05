import xml.etree.ElementTree as ET


class ArxivXMLParser(object):
    def __init__(self, rawXMLContents, maxResults, queryEntry):
        self.rawXMLContents = rawXMLContents
        self.xmlElementTree = self.generateElementTree(self.rawXMLContents)
        self.maxResults = maxResults
        self.queryEntry = queryEntry

    def generateElementTree(self, rawXML):
        return ET.fromstring(rawXML)

    def findAllEntryElements(self, elementTree):
        rawElements = elementTree.getchildren()
        entryElements = []
        for currElement in rawElements:
            if 'entry' in currElement.tag:
                entryElements.append(currElement)
        assert len(entryElements) == self.maxResults, 'Number of entry elements found != max results. # Entry elements = {} and max results = {}'.format(
            len(entryElements), self.maxResults)
        return entryElements

    def extractSummariesFromEntries(self, elementTree):
        entryElements = self.findAllEntryElements(elementTree)
        # print('The entry elements for query {}: \n'.format(self.queryEntry))
        # print(entryElements)
        # print(len(entryElements))
        summaryElements = self.findSummaryElements(entryElements)
        # print('The summary elements for query {}: \n'.format(self.queryEntry))
        # print(summaryElements)
        # print(len(summaryElements))
        return

    def findSummaryElements(self, entryElements):
        summaryElements = []
        for currEntry in entryElements:
            currEntryChildren = self.getEntryElementChildren(currEntry)
            currSummary = self.findElementTypeFromChildren(currEntryChildren, 'summary')
            summaryElements.append(currSummary)
        return summaryElements

    def getEntryElementChildren(self, entryElement):
        return entryElement.getchildren()

    def findElementTypeFromChildren(self, children, type):
        matchingChildren = []
        for currChild in children:
            if type in currChild.tag:
                matchingChildren.append(currChild)
        if len(matchingChildren) == 1:
            return matchingChildren[0]
        elif len(matchingChildren) > 1:
            return matchingChildren
        else:
            raise AttributeError('Could not find any children matching {}!'.format(type))
