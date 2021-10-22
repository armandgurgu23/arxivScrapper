from yacs.config import CfgNode as CN


def getScrapperDefaults():
    _C = CN()
    _C.queryEngine = CN()
    _C.queryEngine.queryFile = ""
    _C.queryEngine.maxResults = 10
    _C.queryEngine.requestPauseTime = 1
    _C.datasetGenerator = CN()
    _C.datasetGenerator.outputPath = ""
    _C.datasetGenerator.generatePdfData = False
    return _C


def getScrapperYamlConfigFile(yamlFilePath):
    _C = getScrapperDefaults()
    rawCfg = _C.clone()
    rawCfg.merge_from_file(yamlFilePath)
    rawCfg.freeze()
    return rawCfg
