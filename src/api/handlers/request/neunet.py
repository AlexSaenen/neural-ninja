from api.handlers.engine.modelNeuNet import Train, Predict, Accuracy, Usable
from api.handlers.engine.activityNeuNet import Stop, Start
from api.handlers.engine.watcherNeuNet import Load, Unload, GetDetails, Delete
from api.handlers.routerHandler import RouterHandler
from api.handlers.request._genericSecured import GenericSecuredRequestHandler

class NeuNetHandler(GenericSecuredRequestHandler):

    def initialize(self):
        modelRouter = RouterHandler()
        activityRouter = RouterHandler()
        watcherRouter = RouterHandler()
        modelRouter.addHandler('train', Train())
        modelRouter.addHandler('predict', Predict())
        modelRouter.addHandler('accuracy', Accuracy())
        modelRouter.addHandler('usable', Usable())
        activityRouter.addHandler('stop', Stop())
        activityRouter.addHandler('start', Start())
        watcherRouter.addHandler('load', Load())
        watcherRouter.addHandler('unload', Unload())
        watcherRouter.addHandler('details', GetDetails())
        watcherRouter.addHandler('delete', Delete())
        self.routers = [ modelRouter, activityRouter, watcherRouter ]
