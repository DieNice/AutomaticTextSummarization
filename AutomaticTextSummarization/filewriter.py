import os


class FileWriter:
    def write(self, pathdir=os.getcwd() + "/output/", data=None):
        if not os.path.exists(pathdir):
            os.mkdir(pathdir)
        for n, v in data:
            f = open(pathdir + n, 'w')
            f.write(v)
