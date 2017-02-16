from kernet.queue import Queue
from kernet.classLoader import ClassLoader
from kernet.pathTools import Path
from kernet.serializer import Serializer
from netKit.config.bindingGenerator import BindingGenerator
import string

class Compiler(object):

    def __init__(self, stream):
        self._serializer = stream

    def compile(self, buildSpecs):
        templateLoader = ClassLoader(path='netKit/templates', instantiate=False)
        templateName = 'basic'
        templateFile = '{}.py'.format(templateName)
        templateSource = templateLoader.loadSource(templateFile, templateName)
        template = string.Template(templateSource)

        binder = BindingGenerator(buildSpecs)
        substitutes = binder.getBindings()
        if buildSpecs['overrideBindings'] is not None:
            substitutes = binder.overrideBindigs(substitutes, buildSpecs['overrideBindings'])
        bindedTemplate = template.substitute(substitutes)

        self._serializer.serialize(bindedTemplate)
