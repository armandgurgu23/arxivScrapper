from yacs.config import CfgNode as CN


def getPartitionerDefaults():
    _C = CN()
    _C.partitioner = CN()
    _C.partitioner.totalTrainSplit = 0.1
    _C.partitioner.totalValidSplit = 0.1
    _C.partitioner.totalTestSplit = 0.1
    _C.partitioner.partitionOutputPath = ""
    _C.partitioner.superCategory = CN()
    return _C


# TODO: Merge this method with the one in scrapper defaults
# since they rely on the same logic but different _C as inputs.
def getPartitionerYamlConfigFile(yamlFilePath):
    _C = getPartitionerDefaults()
    rawCfg = _C.clone()
    rawCfg.merge_from_file(yamlFilePath)
    rawCfg.freeze()
    return rawCfg
