import sys

class Logger(object):

    def __init__(self, moduleName):
        self._module = moduleName

    def _log(self, level, message):
        print('[{0}] > {1}::{2}'.format(level.upper(), self._module, message))

    def info(self, message):
        fnName = sys._getframe().f_back.f_code.co_name
        self._log('info', '{0}() > {1}'.format(fnName, message))

    def warn(self, message):
        fnName = sys._getframe().f_back.f_code.co_name
        self._log('warn', '{0}() > {1}'.format(fnName, message))

    def error(self, message):
        fnName = sys._getframe().f_back.f_code.co_name
        self._log('error', '{0}() > {1}'.format(fnName, message))
