from config.scrapperDefaults import getYamlConfigFile
import argparse


def getScrapperArguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scrapperYaml', type=str, default='config/scrapperConfig.yaml',
                        help='Path to the yaml file describing the scrapper configuration.')
    return parser.parse_args()


def scrapperRunner():
    scrapperArgs = getScrapperArguments()
    yamlConfig = getYamlConfigFile(scrapperArgs.scrapperYaml)
    return


if __name__ == "__main__":
    scrapperRunner()
