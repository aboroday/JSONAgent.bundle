import os
from logging import PlexLogAdapter as log

def open_file(path, binary=True):
    if os.path.exists(path):
        try:
            log.debug('Opening file:  {name}'.format(name=path))
            data = Core.storage.load(path, binary=binary)
            return data
        except Exception as e:
            log.debug('Could not open the file {name}:  {exc}'.format(name=path, exc=e))
            raise

class Mediafile:
    """
    Parsed Mediafile path


    """
    def __init__(self, path):
        self.path = path
        self.folder, self.file = os.path.split(self.path)
        self.filename, self.ext = os.path.splitext(self.file)

        log.debug('full path: {name}'.format(name=self.path))
        log.debug('folder path: {name}'.format(name=self.folder))
        log.debug('full filename: {name}'.format(name=self.filename))
        log.debug('file name: {name}'.format(name=self.file))
        log.debug('file ext: {name}'.format(name=self.ext))