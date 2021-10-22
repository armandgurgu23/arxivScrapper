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
            if "entry" in currElement.tag:
                entryElements.append(currElement)
        assert (
            len(entryElements) == self.maxResults
        ), "Number of entry elements found != max results. # Entry elements = {} and max results = {}".format(
            len(entryElements), self.maxResults
        )
        return entryElements

    def extractPaperPdfURLsFromEntries(self, entries):
        allPdfElements = self.findLinkElements(entries)
        return self.extractPdfUrlsFromPdfElements(allPdfElements)

    def extractPdfUrlsFromPdfElements(self, allPdfElements):
        pdfUrlDict = {}
        for elemIndex, currPdfElem in enumerate(allPdfElements):
            pdfUrlDict["{}_{}".format(self.queryEntry, elemIndex)] = [
                currPdfElem.attrib["href"]
            ]
        return pdfUrlDict

    def findLinkElements(self, entries):
        linkElements = []
        for currEntry in entries:
            currEntryChildren = self.getEntryElementChildren(currEntry)
            candidateLinks = self.findElementTypeFromChildren(currEntryChildren, "link")
            selectedLink = self.selectValidLinkElement(candidateLinks)
            linkElements.append(selectedLink)
        return linkElements

    def selectValidLinkElement(self, candidateLinks):
        validLinkElements = []
        for currLink in candidateLinks:
            linkAttributes = currLink.attrib
            if "href" in linkAttributes and "pdf" in linkAttributes["href"]:
                validLinkElements.append(currLink)
        assert (
            len(validLinkElements) == 1
        ), "Something went wrong! Filtering produced these many valid link elements = {}".format(
            validLinkElements
        )
        return validLinkElements[0]

    def extractSummariesFromEntries(self, elementTree, returnEntries=True):
        entryElements = self.findAllEntryElements(elementTree)
        summaryElements = self.findSummaryElements(entryElements)
        if returnEntries:
            return self.extractSummaryTextFromSummary(summaryElements), entryElements
        else:
            return self.extractSummaryTextFromSummary(summaryElements)

    def extractSummaryTextFromSummary(self, summaryElements):
        summaryDict = {}
        for elemIndex, currSummary in enumerate(summaryElements):
            summaryDict["{}_{}".format(self.queryEntry, elemIndex)] = [currSummary.text]
        return summaryDict

    def findSummaryElements(self, entryElements):
        summaryElements = []
        for currEntry in entryElements:
            currEntryChildren = self.getEntryElementChildren(currEntry)
            currSummary = self.findElementTypeFromChildren(currEntryChildren, "summary")
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
            raise AttributeError(
                "Could not find any children matching {}!".format(type)
            )
