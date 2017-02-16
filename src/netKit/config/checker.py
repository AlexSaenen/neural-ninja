from netKit.config.transpiler import ConfigTranspiler

class ConfigChecker(object):
    expectedComponents = [ 'input', 'output', 'netName' ]

    def __init__(self, configBody):
        self._config = configBody

    def check(self):
        try:
            self._checkComponents()
            ConfigChecker._testInput(self._config['input'])
            ConfigChecker._testOutput(self._config['output'])
            ConfigChecker._testName(self._config['netName'])
        except RuntimeError as error:
            raise RuntimeError('config check failed : {}'.format(error))

    def _checkComponents(self):
        if type(self._config) is not dict:
            raise RuntimeError('The config is not of type \'dict\'')
        if not all(component in self._config for component in ConfigChecker.expectedComponents):
            raise RuntimeError('A component from {} is missing in the config'.format(ConfigChecker.expectedComponents))

    @staticmethod
    def _testInput(_input):
        if type(_input) is not list:
            raise RuntimeError('The input part is not of type \'list\'')
        if len(_input) == 0:
            raise RuntimeError('The input part needs at least 1 feature')

    @staticmethod
    def _testOutput(_output):
        outputSchemes = ConfigTranspiler.acceptedOutputSchemes
        if _output not in outputSchemes:
            raise RuntimeError('The output scheme \'{}\' needs to be among {}'.format(_output, outputSchemes))

    @staticmethod
    def _testName(_name):
        nameAttributeType = type(_name)
        if nameAttributeType is not str:
            raise RuntimeError('The type of name should be {}, not {}'.format(str, nameAttributeType))
