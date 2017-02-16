import checksumdir
import os
import hashlib

class FolderScanner(object):

    def __init__(self, folder):
        self._path = folder
        self._folderHash = None
        self.folderNeedsUpdate = True

    def scan(self):
        hashedDir = checksumdir.dirhash(self._path, 'md5')
        self.folderNeedsUpdate = (hashedDir is not self._folderHash)

    def clear(self):
        self._folderHash = None
        self.folderNeedsUpdate = True

    @staticmethod
    def _md5hash(path, scannedFile):
        hashedFile = hashlib.md5()
        try:
            with open(os.path.join(path, scannedFile), 'rb') as fd:
                for chunk in iter(lambda: fd.read(4096), b""):
                    hashedFile.update(chunk)
            return hashedFile.hexdigest()
        except OSError as error:
            return None

    @staticmethod
    def _removeInvalidFiles(filesAvailable, hashedFiles):
        for idx, hashed in enumerate(hashedFiles):
            if hashed is None:
                del filesAvailable[idx]

    def analyseScan(self, registeredFiles):
        elements = os.listdir(self._path)
        filesAvailable = [el for el in elements if os.path.isfile(os.path.join(self._path, el))]
        hashedFiles = [FolderScanner._md5hash(self._path, el) for el in filesAvailable]
        FolderScanner._removeInvalidFiles(filesAvailable, hashedFiles)
        scannedNames = [os.path.splitext(el)[0] for el in filesAvailable]
        registeredNames = [str(el) for el in registeredFiles]
        newFiles = [el for el in scannedNames if el not in registeredNames]
        filesToRemove = [el for el in registeredNames if el not in scannedNames]
        filesToReload = []
        for el in registeredFiles:
            if str(el) not in newFiles and str(el) not in filesToRemove and el.hash not in hashedFiles:
                filesToReload.append(el)
        fileAnalysis = []
        fileAnalysis.extend([(el, 'new') for el in newFiles])
        fileAnalysis.extend([(el, 'remove') for el in filesToRemove])
        fileAnalysis.extend([(el, 'reload') for el in filesToReload])
        return fileAnalysis
