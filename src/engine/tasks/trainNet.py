from kernet.asyncTask import AsyncTask

class TrainNet(AsyncTask):

    def __init__(self, net, timeout=3):
        self._net = net
        super().__init__(timeout)

    def execute(self):
        batchSize = self._net.getConfig('batchSize')
        netInstance = self._net.getNetworkInstance()
        dataPacket = netInstance.store.pop()
        if dataPacket is not None:
            if len(dataPacket) is not batchSize:
                self._logger.warn("{0}: DataPacket of length {1} is not equal to expected batchSize {2}".format(self._net, len(dataPacket), batchSize))
            netInstance.train(dataPacket.get())
        else:
            self._logger.warn("{0}: no DataPacket available to feed and train".format(self._net))
