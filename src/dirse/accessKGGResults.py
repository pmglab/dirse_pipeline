#!/bin/python
# script for TEA project
import os
def getConditionalGeneList(dir,outPath,outPathGC,pattern):
    fdr=getFDR()
    import os
    import common.util.FileFunction as FF
    if not os.path.exists(os.path.dirname(outPath)):
        os.mkdir(os.path.dirname(outPath))
    wt=FF.getWriter(outPath,False)
    wtgc = FF.getWriter(outPathGC, False)
    FF.gzWrite(wt,"DiseaseName\tAssociatedGenes\n",outPath)
    FF.gzWrite(wtgc, "DiseaseName\tAssociatedGenesCounts\n", outPathGC)
    import os
    print(len(os.listdir(dir)))
    for disDir in os.listdir(dir):
        for file in os.listdir(os.path.join(dir,disDir)):
            if file.__contains__(pattern):
                print(os.path.join(dir,disDir,file))
                pcut=fdr[file.split("-")[0]]
                genelist=getGeneListFromKGGxlsx(os.path.join(dir,disDir,file),pcut)
                FF.gzWrite(wt,file.split("-")[0]+"\t"+",".join(genelist)+"\n",outPath)
                FF.gzWrite(wtgc, file.split("-")[0] + "\t" + str(len(genelist)) + "\n", outPathGC)
    wt.close()
    print("\n"+str(len(os.listdir(dir)))+" files finish!")
def getKGGparameter(dir,outPath):
    import common.util.FileFunction as FF
    wt=FF.getWriter(outPath,False)
    FF.gzWrite(wt,"DiseaseName\tErrorRate\n",outPath)
    import os
    for disDir in os.listdir(dir):
        for file in os.listdir(os.path.join(dir,disDir)):
            if file.__contains__("ECS-Cond"):
                if len(file.split("-")[2].split("_"))==1:
                    error="0.05"
                else:
                    error=file.split("-")[2].split("_")[1].replace(".xlsx","")
                FF.gzWrite(wt,file.split("-")[0]+"\t"+error+"\n",outPath)
    wt.close()

def getGeneListFromKGGxlsx(path,pcut):
    # ref: https://blog.csdn.net/bladecoder/article/details/8052746
    geneList=[]
    import xlrd
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    for rownum in range(1,sh.nrows):
        if sh.cell(rownum,8).value=="-":
            continue
        if float(sh.cell(rownum,8).value)<pcut:
            geneList.append(sh.cell(rownum,1).value)
    #print(geneList)
    #print(str(len(geneList))+" vs "+str(sh.nrows-1))
    return geneList
def main():
    dir="F:\Projects\TEA\GWAS_tmp\\analysis\\tmp"
    pattern="ECS-rmHLA-Cond"
    #pattern = "ECS-Cond"
    outDir="F:\Projects\TEA\GWAS_tmp\\analysis\sum_tmp\\pvalue-rmHLA-Cond"

    outPathAG=outDir+"\\associatedGenes.txt"
    outPathER = "F:\Projects\TEA\\Diseases10Sum\\errorRate.txt"
    outPathGC = outDir+"\\associatedGenesCount.txt"
    pcut=0.05
    getConditionalGeneList(dir,outPathAG,outPathGC,pattern)
def mergeCondtionalGenes(dir,pattern):
    outPathAG=os.path.join(dir,"TSBGene","associatedGenes.txt")
    outPathGC=os.path.join(dir,"TSBGene","associatedGenes.count.txt")
    genesDir=os.path.join(dir,"TSBGene","DiseaseBased")
    getConditionalGeneList(genesDir, outPathAG, outPathGC, pattern)

def getFDR():
    fdr={}
    fdr["BD"] =7.427493748198251E-4
    fdr["CAD"] =5.323412038368041E-4
    fdr["Height"] = 3.9181882297625576E-11
    fdr["RA"]=1.869648132221516E-6
    fdr["TC"] =1.966027052532243E-6

    ##fdr["PD"] =1.0797026464043295E-4
    fdr["PD"] =3.0367061153470945E-4
    fdr["MDD"] =7.394161680887774E-4
    #fdr["MDD"] = 2.417610232116086E-4
    fdr["MDD2"] = 7.394161680887774E-4


    fdr["CD"]=2.0641539033150313E-6
    fdr["Insomnia"] =9.590230176407788E-5
    fdr["Intelligence"] =3.110908738681682E-4
    #fdr["RA"] =2.08837882758982E-6
    #fdr["RA"] =1.869648132221516E-6
    fdr["ALS"]=9.45494291568992E-5
    fdr["T2D"] =5.953508464552114E-4

    fdr["VAT"] =2.2E-5
    fdr["T2Dadjust"]=4.7564031061113224E-4
    #fdr["Height"]= 3.918188229762558E-22

    fdr["ASD"]=3.834649896464453E-6
    return fdr
def singleDiseaseDeal():
    #path="F:\Projects\TEA\GWAS_tmp\BD\BD-ECS-Cond-0.01.xlsx"
    path = "F:\Projects\TEA\GWAS_tmp\BD\\noCondGenes.txt"
    pcut=7.427493748198251E-4
    outPath="F:\Projects\TEA\GWAS_tmp\BD\\noCondAssociatedGenes.txt"
    import os
    import common.util.FileFunction as FF
    if not os.path.exists(os.path.dirname(outPath)):
        os.mkdir(os.path.dirname(outPath))
    wt=FF.getWriter(outPath,False)
    FF.gzWrite(wt,"DiseaseName\tAssociatedGenes\n",outPath)
    #genes=getGeneListFromKGGxlsx(path, pcut)
    genes=getGeneListFromKGGtxt(path,pcut)
    FF.gzWrite(wt,"BD\t"+",".join(genes)+"\n",outPath)
    wt.close()
def getGeneListFromKGGtxt(path,pcut):
    regenelist=[]
    import common.util.FileFunction as FF
    line_iter=FF.getLineByPath(path)
    line_iter.__next__()
    for line in line_iter:
        cell=line.split("\t")
        if float(cell[1])<pcut:
            regenelist.append(cell[0])
    return regenelist

def changeName(dir,pattern):
    for disDir in os.listdir(dir):
        for file in os.listdir(os.path.join(dir,disDir)):
            if file.__contains__(pattern):
                os.rename(os.path.join(dir,disDir,file),os.path.join(dir,disDir,file.replace(pattern.split(".")[0],disDir)))




if __name__=="__main__":
    pass
    main()
    #singleDiseaseDeal()
    #getGeneListFromKGGxlsx("F:\Projects\TEA\GWAS_10_diseases\Amyotrophic_lateral_sclerosis\ALS-ECS-Cond_0.1.xlsx", 1)