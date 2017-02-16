from tensorflow.contrib.learn.python.learn.estimators._sklearn import NotFittedError

## NeuNetOperator method decorators

def hungry(fn):
    def _hungry(self, food=None):
        if food is None:
            return { "error": "No food available or incorrect meal form" }
        return fn(self, food)
    return _hungry

def feedmethod(fn):
    def _feed(self, food=None):
        _meal = None
        if food is not None and 'meals' in food and type(food['meals']) is list:
            _meal = food['meals']
        result = fn(self, _meal)
        return result
    return _feed

def trained(fn):
    def _fitted(self, meal):
        try:
            return fn(self, meal)
        except NotFittedError:
            error = "Network {} needs to be trained before usage".format(self.__class__.__name__)
            self._logger.warn(error)
            return { 'error': error }
    return _fitted

def accurate(fn):
    def _accurate(self, meal):
        with self._lock:
            if self._lastKnownAccuracy < self._config['usageThreshold']:
                error = "Network {} needs more training, {} is below the accuracy threshold of {}".format(self.__class__.__name__, self._lastKnownAccuracy, self._config['usageThreshold'])
                self._logger.warn(error)
                return { 'error': error }
        return fn(self, meal)
    return _accurate

## NeuNetWatcher method decorators

def loaded(fn):
    def _loaded(self, isReloading=False):
        with self._lock:
            if not self.isLoaded:
                raise RuntimeError("Network {0} is not loaded".format(self._name))
            return fn(self, isReloading)
    return _loaded

def stopped(fn):
    def _stopped(self, args=None):
        with self._lock:
            if self.file is None:
                raise RuntimeError("Tried to start the network {0} but the file wasn't loaded".format(self._name))
            if self.isRunning:
                raise RuntimeError("Network {0} is already running".format(self._name))
            return fn(self, args) if args is not None else fn(self)
    return _stopped

def running(fn):
    def _running(self, args=None):
        with self._lock:
            if self.file is None:
                raise RuntimeError("Tried to stop the network {0} but the file wasn't loaded".format(self._name))
            if not self.isRunning:
                raise RuntimeError("Network {0} is already stopped".format(self._name))
            return fn(self, args) if args is not None else fn(self)
    return _running
