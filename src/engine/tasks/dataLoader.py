from kernet.asyncTask import AsyncTask
from engine.moduleManager import ModuleManager
from engine.dataPacket import DataPacket
import os
import requests

class DataLoader(AsyncTask):

    def __init__(self, net, timeout=2):
        self._net = net
        super().__init__(timeout)

    def _fetchData(self, urlToHit, body):
        self._logger.info("Sending GET request on {0} to fetch data for {1}".format(urlToHit, self._net))
        try:
            return requests.get(urlToHit, data=body, timeout=self._timeout).json()
        except Exception as error:
            self._logger.error("Encountered an error during the request : {0}".format(error))
            return None

    def _handleResponse(self, json):
        if json is None:
            return
        if json['error']:
            self._logger.error("Network {0} encountered {1} while fetching data".format(self._net, json['error']))
        else:
            packet = DataPacket(json=json['batch'])
            try:
                self._net.getNetworkInstance().store.push(packet)
            except Exception as error:
                self._logger.warn("Network {0} lost its instance with pending data : {1}".format(self._net, error))

    def execute(self):
        neuNetConfig = self._net.getConfig()
        systemConfig = ModuleManager.instance.get('SystemConfig')
        urlToHit = os.path.join(systemConfig.get('apiUrl'), neuNetConfig['route'])
        body = {'batchSize': neuNetConfig['batchSize'], 'engineKey': systemConfig.get('engineKey'), 'plugin': neuNetConfig['plugin']}
        json = self._fetchData(urlToHit, body)
        self._handleResponse(json)
