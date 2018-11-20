import common.util.FileFunction as FF
import os
from scipy import stats
from xlwt import *
import xlrd

def getRank(inPath,outDir):
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    line_iter=FF.getArrByPath(inPath)
    head=line_iter.__next__()
    bwArr=[]
    for i in range(int((len(head)-1)/2)):
        bwArr.append(FF.getWriter(os.path.join(outDir,head[i+1][0:-1]+".txt"),False))
    for line in line_iter:
        for j in range(len(bwArr)):
            FF.gzWrite(bwArr[j],line[0]+"\t"+line[j+1]+"\n",".txt")
    for k in range(len(bwArr)):
        bwArr[k].close()
def mergeGenes(noPath, rankPath, outPath):
    no_arr=[]
    out_wt=FF.getWriter(outPath,False)
    out_wtc = FF.getWriter(outPath+".count", False)
    FF.gzWrite(out_wt,"Disease\tNoRankGenes\tRankGenes\n",outPath)
    FF.gzWrite(out_wtc, "Disease\tAllNoGenes\tAllRankGenes\tNoRankGenes\tRankGenes\n", outPath)
    no_iter=FF.getArrByPath(noPath)
    rank_iter=FF.getArrByPath(rankPath)
    no_iter.__next__()
    rank_iter.__next__()
    for arr in no_iter:
        no_arr.append(arr)
    for arrr in rank_iter:
        for arrn in no_arr:
            if arrr[0]==arrn[0]:
                FF.gzWrite(out_wt, arrr[0]+"\t", outPath)

                gener=arrr[1].split(",")
                genen=arrn[1].split(",")
                FF.gzWrite(out_wtc, arrr[0] + "\t"+str(len(genen))+"\t"+str(len(gener))+"\t", outPath)
                tmpgenes=[]
                for gene1 in genen:
                    goto=False
                    for gene2 in gener:
                        if gene1==gene2:
                            goto=True
                            break
                    if goto==True:
                        continue
                    else:
                        tmpgenes.append(gene1)
                FF.gzWrite(out_wt, ",".join(tmpgenes)+"\t", outPath)
                FF.gzWrite(out_wtc, str(len(tmpgenes))+ "\t", outPath)
                ##
                tmpgenes = []
                for gene1 in gener:
                    goto=False
                    for gene2 in genen:
                        if gene1==gene2:
                            goto=True
                            break
                    if goto==True:
                        continue
                    else:
                        tmpgenes.append(gene1)
                FF.gzWrite(out_wt, ",".join(tmpgenes) + "\n", outPath)
                FF.gzWrite(out_wtc, str(len(tmpgenes)) + "\n", outPath)
            continue
        continue
    out_wt.close()
def analysis(inPath,outPath):
    line_iter=FF.getArrByPath(inPath)
    wt=FF.getWriter(outPath,False)
    FF.gzWrite(wt,"\t".join(line_iter.__next__())+"\n",outPath)
    for line in line_iter:
        FF.gzWrite(wt,line[0],outPath)
        for idx in range(len(line)-1):
            genes = line[idx+1].split(",")
            hit=0
            nonhit=0
            for gene in genes:
                pubmed=gene.split(":")[1]
                if pubmed:
                    hit+=1
                else:
                    nonhit+=1
            FF.gzWrite(wt,"\t"+str(hit)+"/"+str(nonhit),outPath)
        FF.gzWrite(wt, "\t" + "\n", outPath)
    wt.close()

def getGenePvalueFromKGGXls(geneSymbol,wb):
    re="-"
    sh = wb.sheet_by_index(0)
    for rownum in range(1,sh.nrows):
        if sh.cell(rownum,1).value==geneSymbol:
            re= sh.cell(rownum,8).value
    return str(re)
def getKGGXlsPath(dir,disease,pattern="ECS-rank-Cond"):
    for file in os.listdir(os.path.join(dir,disease)):
        if file.__contains__(pattern):
            return os.path.join(dir, disease,file)


def getFinalResultXlsx(dir,noDir,removeNoPebmed=False):
    inPath=os.path.join(dir,"compareNCBI.txt")
    outPath = os.path.join(dir,"compareNCBI.stat.rmNoNCBI.print.xls")
    style1 = XFStyle()
    style2 = XFStyle()
    style3 = XFStyle()
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['gray25']
    algn1=Alignment()
    algn1.wrap=algn1.WRAP_AT_RIGHT
    algn1.horz=algn1.HORZ_LEFT
    algn1.vert=algn1.VERT_CENTER
    style2.alignment=algn1
    style1.alignment = algn1
    style1.pattern = pattern
    import xlwt
    wb = xlwt.Workbook()
    ncbi=FF.getArrByPath(inPath)
    head=ncbi.__next__()
    for arr in ncbi:
        rank_dir=os.path.join(dir, "TSBGene", "DiseaseBased")
        #rank_dir ="F:\Projects\TEA\GWAS_10_diseases"
        wb_rank = xlrd.open_workbook(getKGGXlsPath(rank_dir,arr[0],"ECS-rank-Cond"))
        wb_no =xlrd.open_workbook(getKGGXlsPath(noDir,arr[0],"ECS-rmHLA-Cond"))

        fisher=[]
        ws=wb.add_sheet(arr[0],True)
        ws.col(0).width= 256 * 15
        ws.col(1).width = 256 * 15
        ws.col(2).width = 256 * 15
        ws.col(3).width = 256 * 100
        rn=0
        ws.write(rn, 0, "Gene", style=style2)
        ws.write(rn, 1, "P1", style=style2)
        ws.write(rn, 2, "P2", style=style2)
        ws.write(rn, 3, "PubMedID", style=style2)
        rn += 1
        for i in range(len(arr)-1):
            ws.write_merge(rn,rn,0,3,getRightColName(head[i+1]),style=style1)
            rn+=1
            pubmeds=arr[i+1].split(",")
            fisher.append(len(pubmeds))
            hit=0
            for pm in pubmeds:
                gpm = pm.split(":")
                if gpm[1]:
                    hit+=1
                    ws.write(rn,0, gpm[0],style=style2)
                    ws.write(rn, 3,gpm[1],style=style2)
                    ws.write(rn,1,getGenePvalueFromKGGXls(gpm[0],wb_no),style2)
                    ws.write(rn, 2, getGenePvalueFromKGGXls(gpm[0], wb_rank), style2)
                    rn += 1
                else:
                    if not removeNoPebmed:
                        ws.write(rn, 0, gpm[0],style=style2)
                        ws.write(rn, 1, getGenePvalueFromKGGXls(gpm[0], wb_no), style2)
                        ws.write(rn, 2, getGenePvalueFromKGGXls(gpm[0], wb_rank), style2)
                        rn += 1
            fisher.append(hit)
        fisher[0]=fisher[0]-fisher[1]
        fisher[2] = fisher[2] - fisher[3]
        no_bigger_rank=stats.fisher_exact([fisher[0:2],fisher[2:4]],alternative="less")[1]
        no_smaller_rank = stats.fisher_exact([fisher[0:2],fisher[2:4]],alternative="greater")[1]
        ws.write_merge(rn, rn+1, 0, 3,"STATISTIC (hit counts/non-hit counts):  By p-value ranking:"+str(fisher[1])+"/"+str(fisher[0])+"; By selective expression ranking:"+str(fisher[3])+"/"+str(fisher[2])+"\n"
                       +"Fisher's exact test: P(H1=p-value>selective expression)="+str(no_bigger_rank)+"; P(H1=selective expression>p-value)="+str(no_smaller_rank), style=style1)
        rn+=2
        ws.write_merge(rn, rn+2, 0, 3,"Note: P1: This is a conditional gene-based association p-value according "
                                    "to statistical significance order. \nP2: This is a conditional gene-based "
                                    "association p-value according to tissue-specific pathogenic potential. "
                                    "\nThe papers co-mentioning the gene and diseases/traits in the titles or "
                                    "abstracts in PubMed database were searched by the API function.", style=style2)
    wb.save(outPath)

def getRightColName(name):
    colname={}
    colname["NoGenesNCBI"]="By p-value ranking"
    colname["RankGenesNCBI"] = "By selective expression ranking"
    return colname[name]


def makeDir(dir):
    if not os.path.exists(os.path.join(dir,"TSBGene","DiseaseBased")):
        os.makedirs(os.path.join(dir,"TSBGene","DiseaseBased"))

def sepRankFile(dir):
    inPath = os.path.join(dir, "tea", "tea.disease.gene.rank.txt")
    outDir=os.path.join(dir,"rank")
    getRank(inPath,outDir)
    makeDir(dir)
def getCompareGenes(dir,pattern="ECS-rank-rmHLA-Cond",noPath="F:\Projects\TEA\GWAS_tmp\\analysis\sum_associatedGenes\pvalue-rmHLA-Cond\\associatedGenes.txt"):
    import common.tmp.Tea as TEA
    TEA.mergeCondtionalGenes(dir,pattern)

    rankPath=os.path.join(dir,"TSBGene","associatedGenes.txt")
    megeredPath=os.path.join(dir,"comparedGenes.txt")
    mergeGenes(noPath,rankPath,megeredPath)


def compareAnalyze(dir):
    ncbi_Path=os.path.join(dir,"compareNCBI.txt")
    ncbi_stat_Path=os.path.join(dir,"compareNCBI.stat.txt")
    analysis(ncbi_Path, ncbi_stat_Path)

    noDir="F:\Projects\TEA\GWAS_tmp\\analysis\GWAS_associatedGenes"
    getFinalResultXlsx(dir,noDir,True)

def checkASD():
    candGenes="Il17, Il17f, Rorc, Rora, Irf4, Ahr, stat3, Il22, Il23, Il23r, Il6, Il1b".upper().split(", ")
    wb=xlrd.open_workbook(getKGGXlsPath("F:\Projects\TEA\GWAS_tmp\\analysis\GWAS_associatedGenes","ASD","ECS-org-1"))
    for gene in candGenes:
        p=getGenePvalueFromKGGXls(gene, wb)
        if p:
            print(gene+": "+p)


if __name__=="__main__":
    pass
    dir="F:\Projects\TEA\GWAS_tmp\\analysis\TEA_analysis\pvalue-rmHLA-Cond-fi\\transcript_tmp_0.01"
    #sepRankFile(dir)
    #getCompareGenes(dir)
    compareAnalyze(dir)
    #checkASD()

