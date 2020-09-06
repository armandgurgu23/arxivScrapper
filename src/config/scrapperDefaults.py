from yacs.config import CfgNode as CN

_C = CN()
_C.queryEngine = CN()
_C.queryEngine.queryFile = ''
_C.queryEngine.maxResults = 10
_C.queryEngine.requestPauseTime = 1
_C.datasetGenerator = CN()
_C.datasetGenerator.outputPath = ''


def getYamlConfigFile(yamlFilePath):
    rawCfg = _C.clone()
    rawCfg.merge_from_file(yamlFilePath)
    rawCfg.freeze()
    return rawCfg
