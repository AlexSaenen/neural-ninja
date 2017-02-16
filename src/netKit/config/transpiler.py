from pydoc import locate
import math

class ConfigTranspiler(object):
    acceptedOutputSchemes = [ 'classification', 'regression' ]

    def __init__(self, config):
        self._config = config
        self._transpiledConfig = None

    def digest(self):
        config = {
            'features': self._config['input'],
            'isRegression': (self._config['output'] == 'regression'),
            'layerScale': 1,
            'isDeep': False,
            'name': self._config['netName'],
            'overrideBindings': self._config['templateBindings'] if 'templateBindings' in self._config else None
        }

        config['layerScale'] = int(math.log2(len(config['features']) / 2))
        if config['overrideBindings'] is not None and 'layerScale' in config['overrideBindings']:
            config['layerScale'] = config['overrideBindings']['layerScale']
        config['isDeep'] = (config['layerScale'] > 0)

        if config['isDeep']:
            config['neuronStarters'] = (50 * config['layerScale'])

        self._transpiledConfig = config

    def extract(self):
        return self._transpiledConfig
