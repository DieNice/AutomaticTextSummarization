import os
import re


class FileReader:
    def read(self, filepath='', pathdir=os.getcwd() + "/textexamples/", namepattern=r"\w+\.txt"):
        '''The method reads one file using a path "filpath and returns string"
        or reads all files from a directory "pathdir" using a template "namepattern" and returns list of strings'''
        if os.path.isfile(filepath):
            if not filepath.endswith('.txt'):
                return "File {} is not text file".format(os.path.basename(filepath))
            return [os.path.basename(filepath), self.__readfile(filepath)]
        elif filepath == '':
            pathdir = os.path.abspath(pathdir)
            if os.path.isdir(pathdir):
                try:
                    fitem = re.search(namepattern, '')
                except:
                    return "Incorect regular expression \"{}\"".format(namepattern)
                filelist = os.listdir(pathdir)
                validnameslist = []
                for i in filelist:
                    fitem = re.search(namepattern, i)
                    if fitem is not None:
                        validnameslist.append(i)
                if not validnameslist:
                    return "Text files with \"{}\" regex not founded in {}".format(namepattern, pathdir)
                resultdata = []
                for i in validnameslist:
                    resultdata.append([i, self.__readfile(pathdir + '/' + i)])
                return resultdata

            else:
                return "Directory not exist"
        else:
            return "File \"{}\" does not exist".format(os.path.basename(filepath))

    def __readfile(self, filepath):
        fin = open(filepath, 'r')
        data = fin.read()
        return data