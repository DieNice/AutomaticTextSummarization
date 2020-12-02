from AutomaticTextSummarization.filereader import FileReader
from AutomaticTextSummarization.filewriter import FileWriter
from AutomaticTextSummarization.summarization import Summarization

if __name__ == '__main__':
    rr = FileReader().read()
    psnt = int(input("Введите процент результирующего текста который вы хотите получить:"))
    res = []
    for n, v in rr:
        res.append((n, Summarization().extract(v, psnt)))
    FileWriter().write(data=res)
