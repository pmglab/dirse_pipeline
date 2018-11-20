#!/bin/python
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
def gzWrite(writer,str,isGz):
    if isGz.endswith(".gz"):
        writer.write(str.encode())
    else:
        writer.write(str)

def main():
    path="F:\Projects\TEA\GWAS_10_diseases\Total_cholesterol\jointGwasMc_TC.txt.gz"
    out="F:\Projects\TEA\GWAS_10_diseases\Total_cholesterol\jointGwasMc_TC-add-hg19-chr.txt.gz"
    iterline=getArrByPath(path)
    wt=getWriter(out,False)
    gzWrite(wt,"hg19-chr\thg19-bp\t"+"\t".join(iterline.__next__())+"\n",out)
    for line in iterline:
        gzWrite(wt,line[1].split(":")[0].replace("chr","")+"\t"+line[1].split(":")[1]+"\t"+"\t".join(line)+"\n",out)
    wt.close()

def testPort(ip,port):
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip, port))
        print(str(ip)+':'+str(port)+' OK!')
    except Exception:
        print
        print(str(ip)+':'+str(port)+' not connected!')
    sk.close()

if __name__=="__main__":
    import common.util.FileFunction as FF
    #FF.readTxt('D:\Data\Local\Lab\Program_data\java\projects\\netbeans\\tea\\resources\\getx.transcript.weight.mean.txt.gz')
    testPort('ali.snplife.com',1194)
