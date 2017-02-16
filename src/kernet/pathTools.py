class Path(object):

    @staticmethod
    def convert(name, toClass):
        if name is None:
            return ''

        _firstLetter = name[:1].upper() if toClass else name[:1].lower()
        _rest = name[1:]
        return (_firstLetter + _rest)

    @staticmethod
    def fusion(path, module, separator='.'):
        return '{}{}{}'.format(path, separator, module)

    @staticmethod
    def extractModuleName(modulePath, separator='.'):
        return modulePath.split(separator)[-1]
