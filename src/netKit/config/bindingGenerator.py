from kernet.pathTools import Path

class BindingGenerator(object):

    def __init__(self, buildSpecs):
        self._buildSpecs = buildSpecs

    def getBindings(self):
        columns = str([featureName for featureName in self._buildSpecs['features']])

        return {
            'networkType': 'Regressor' if self._buildSpecs['isRegression'] else 'Classifier',
            'networkDepth': 'DNN' if self._buildSpecs['isDeep'] else 'Linear',
            'usageThreshold': 0.8,
            'inputSelector': '{}TrainingInput'.format(self._buildSpecs['name']),
            'columns': columns,
            'networkName': Path.convert(self._buildSpecs['name'], toClass=True),
            'features': self._getFeatures(),
            'labels': 'tf.placeholder({}, [None, 1])'.format('tf.float32' if self._buildSpecs['isRegression'] else 'tf.int'),
            'columnsWithoutApostrophe': columns.replace('\'', ''),
            'neuronLayers': self._getNeuronLayers(),
            'optimizer': 'RMSPropOptimizer',
            'learningRate': 0.01
        }

    def overrideBindigs(self, bindings, overriders):
        if type(overriders) is not dict:
            raise RuntimeError('The templateBindings is not of type \'dict\'')

        for overrider in overriders:
            if overrider in bindings:
                bindings[overrider] = overriders[overrider]

        return bindings

    def _getFeatures(self):
        featureGenerator = '{0}{1} = tf.contrib.layers.real_valued_column(\'{1}\')\n'
        featureBlob = str()
        for featureName in self._buildSpecs['features']:
            featureBlob += featureGenerator.format(8 * ' ', featureName)
        return featureBlob

    def _getNeuronLayers(self):
        if not self._buildSpecs['isDeep']:
            return 8 * ' '

        neuronLayers = []
        neuronsPerLayer = self._buildSpecs['neuronStarters']
        for layer in range(self._buildSpecs['layerScale']):
            neuronLayers.append(int(neuronsPerLayer))
            neuronsPerLayer *= 0.6
        return '{}, hidden_units={}'.format(12 * ' ', neuronLayers)
