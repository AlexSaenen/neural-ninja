from kernet.logger import Logger
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.ERROR)

config = {
    'autoRun': True,
    # 'autoTrainable': False,
    # 'batchSize': 50,
    'usageThreshold': 0.8,
    'progressive': True
}

class NeuNet(object):

    def __init__(self, atomicLock):
        self._logger = Logger(self.__class__.__name__)
        self._lock = atomicLock
        self.session = tf.Session()
        init = tf.initialize_all_variables()

        self._declareNetwork()
        self.session.run(init)
        self._logger.info("Network {} was started".format(self.__class__.__name__))

    def _declareNetwork(self):
        raise NotImplementedError("Class %s doesn't implement class method _declareNetwork()" % (self.__class__.__name__))

    def stop(self):
        self.session.close()
        self._logger.info("Network {} has been stopped".format(self.__class__.__name__))
