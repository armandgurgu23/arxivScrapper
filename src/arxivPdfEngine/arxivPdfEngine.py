# Used to fetch the raw PDF contents from the arxiv
# PDF URL.
import urllib
import tika
from urllib import request
from tika import parser


class ArxivPdfEngine(object):
    def __init__(self):
        pass

    def fetchRawPdfContentsFromUrl(self, urlString):
        # May need to wrap this later in a try/except to handle
        # connection errors.
        urlPdfContents = request.urlopen(urlString).read()
        return urlPdfContents

    def extractPdfTextFromDocument(self, pdfFilePath):
        parsedPdf = parser.from_file(pdfFilePath)
        return parsedPdf['content']
