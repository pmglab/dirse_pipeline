def log(string,LOG_PATH):
    logs=open(LOG_PATH,"w")
    logs.write(str(string))
    logs.close()
    print(str(string))
def getArrByPath(filePath,sep="\t"):
    import gzip
    import filetype as ft
    isGzip = True
    try:
        if str(ft.guess(filePath).extension) == "gz":
            isGzip=True
    except:
        isGzip = False
    if isGzip:
        reader = gzip.GzipFile(filePath, "r")
    else:
        reader=open(filePath,"r")
    while True:
        line=reader.readline()
        if not line:
            reader.close()
            break
        if isGzip:
            lineArr=line.decode().strip().split(sep)
        else:
            lineArr = line.strip().split(sep)
        yield lineArr

def getLineByPath(filePath):
    import gzip
    import filetype as ft
    isGzip = True
    try:
        if str(ft.guess(filePath).extension) == "gz":
            isGzip = True
    except:
        isGzip = False
    if isGzip:
        reader = gzip.GzipFile(filePath, "r")
    else:
        reader = open(filePath, "r")
    while True:
        line = reader.readline()
        if not line:
            reader.close()
            break
        if isGzip:
            lineArr = line.decode().strip()
        else:
            lineArr = line.strip()
        yield lineArr

def getWriter(filePath,isAdd):
    import gzip
    if isAdd:
        if filePath.endswith(".gz"):
            expr = gzip.GzipFile(filePath, "a")
        else:
            expr=open(filePath,"a")
    else:
        if filePath.endswith(".gz"):
            expr = gzip.GzipFile(filePath, "w")
        else:
            expr=open(filePath,"w")
    return expr
def gzWrite(writer,str,isGz=".txt"):
    if isGz.endswith(".gz"):
        writer.write(str.encode())
    else:
        writer.write(str)

def readTxt(path,lineNum=5):
    iter=getLineByPath(path)
    for i in range(lineNum):
        print(iter.__next__())

if __name__=="__main__":
    readTxt("F:\Resources\GeneAnnotation\Homo_sapiens.GRCh37.75.gtf.gz",lineNum=20)