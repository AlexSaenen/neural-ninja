class SubRouter(object):

    def __init__(self):
        self._handlerMapping = []
        self._routesServed = []

    def addHandler(self, route, handler):
        if route in self._routesServed:
            raise RuntimeError("Route {} is already handled".format(route))
        self._routesServed.append(route)
        self._handlerMapping.append({ 'route': route, 'handler': handler })

    def servesRoute(self, route):
        return route in self._routesServed

    def getHandler(self, route):
        if not self.servesRoute(route):
            raise RuntimeError("Route {} is not handled".format(route))
        return next(( handler['handler'] for handler in self._handlerMapping if handler['route'] == route), None)
