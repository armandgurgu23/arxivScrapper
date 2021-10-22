class DatasetPartitioner(object):
    def __init__(self, partitionerConfig, datasetPath):
        self.partitionerConfig = partitionerConfig
        self.datasetPath = datasetPath

    def __call__(self):
        print(self.partitionerConfig)
        print(self.datasetPath)
        raise NotImplementedError("STOP ME HERE!!! PREPING THE PARTITION!")
