from netKit.config.checker import ConfigChecker
from netKit.config.transpiler import ConfigTranspiler
from netKit.compiler import Compiler
from kernet.serializer import Serializer
from kernet.pathTools import Path
from kernet.logger import Logger
import os, requests, json

class Creator(object):

    def __init__(self):
        self._creationName = None
        self._buildSpecs = None

    def configure(self, configInput):
        checker = ConfigChecker(configInput)
        checker.check()

        transpiler = ConfigTranspiler(configInput)
        transpiler.digest()
        self._creationName = configInput['netName']
        self._buildSpecs = transpiler.extract()

    def run(self):
        serializer = Serializer()
        streamPath = Path.fusion('netKit/build', '{}.py'.format(self._creationName), '/')
        try:
            serializer.openStream(streamPath)
        except FileExistsError:
            raise RuntimeError('Cannot open stream to {}, file exists already'.format(streamPath))
        compiler = Compiler(serializer)
        compiler.compile(self._buildSpecs)
        serializer.closeStream()
        self._uploadCreation(streamPath)

    def _uploadCreation(self, creationPath):
        apiUrl = 'http://localhost:8080'
        payloadForm = { 'skynetApiKey': 'skynetSuperSecretApiKey' }
        payloadFiles = { 'networkFile': open(creationPath, 'rb') }
        try:
            response = requests.post('{}/networks/upload'.format(apiUrl), files=payloadFiles, data=payloadForm)
            body = json.loads(response.text)
            if response.status_code != 200:
                raise RuntimeError(response)
            if body['error'] is not None:
                raise RuntimeError(body['error'])
        except Exception as error:
            self._onUploadError(error)
        finally:
            os.remove(creationPath)

    def _onUploadError(self, error):
        errorMessage = 'Failed to upload newly created network {} : {}'.format(self._creationName, error)
        Logger('Creator').error(errorMessage)
        raise RuntimeError(errorMessage)
