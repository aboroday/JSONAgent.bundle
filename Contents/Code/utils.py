import os

class Mediafile:
    """
    Parsed Mediafile path


    """
    def __init__(self, path):
        self.path = path
        self.folder, self.file = os.path.split(self.path)
        self.filename, self.ext = os.path.splitext(self.file)
