import common.util.FileFunction as FF
def classTissues():
    tissueClass={}
    tissueClass['Brain']='Brain-Amygdala	Brain-Anteriorcingulatecortex(BA24)	Brain-Caudate(basalganglia)	' \
                         'Brain-CerebellarHemisphere	Brain-Cerebellum	Brain-Cortex	Brain-FrontalCortex(BA9)	' \
                         'Brain-Hippocampus	Brain-Hypothalamus	Brain-Nucleusaccumbens(basalganglia)	' \
                         'Brain-Putamen(basalganglia)	Brain-Spinalcord(cervicalc-1)	' \
                         'Brain-Substantianigra'.split("\t")
    tissueClass['Adipose']='Adipose-Subcutaneous\tAdipose-Visceral(Omentum)'.split('\t')
    tissueClass['Circulatory']='Artery-Aorta\tArtery-Coronary\tArtery-Tibial\tHeart-AtrialAppendage\tHeart-LeftVentricle'.split('\t')
    tissueClass['Reproductive (Female)']='FallopianTube\tCervix-Ectocervix\tCervix-Endocervix\tUterus\tVagina\tOvary\tBreast-MammaryTissue'.split('\t')
    tissueClass['Digestive']='MinorSalivaryGland\tStomach\tLiver\tEsophagus-GastroesophagealJunction\tEsophagus-Mucosa\tEsophagus-Muscularis\tSmallIntestine-TerminalIleum\tColon-Sigmoid\tColon-Transverse'.split('\t')

    tissueClass['Endocrine']='AdrenalGland,Thyroid'.split(',')
    tissueClass['Urinary']='Bladder,Kidney-Cortex'.split(',')
    tissueClass['Immune']='Cells-EBV-transformedlymphocytes,Spleen'.split(',')
    tissueClass['Connective']=['Cells-Transformedfibroblasts']
    tissueClass['Respiratory']=['Lung']

    tissueClass['Muscular']=['Muscle-Skeletal']
    tissueClass['Nerve']=['Nerve-Tibial']
    tissueClass['Reproductive (Male)']='Prostate,Testis'.split(',')
    tissueClass['Skin']='Skin-NotSunExposed(Suprapubic),Skin-SunExposed(Lowerleg)'.split(',')


    #orgpath='F:\Projects\TEA\GWAS_tmp\\analysis\Rplot\\NGdata.txt'
    #outpath='F:\Projects\TEA\GWAS_tmp\\analysis\Rplot\\NGdataAddCategories2.txt'

    orgpath='F:\Projects\TEA\GWAS_tmp\\analysis\Rplot\\tea.enrich_v3.tpm_0.01.txt'
    outpath='F:\Projects\TEA\GWAS_tmp\\analysis\Rplot\\tea.enrich_v3.tpm_0.01.forRplot.txt'
    line_iter=FF.getLineByPath(orgpath)
    wt=FF.getWriter(outpath,False)
    FF.gzWrite(wt,line_iter.__next__()+'\tCategories\n')
    for line in line_iter:
        break_loop=False
        tissue=line.split("\t")[1]
        for cata in tissueClass.keys():
            for tis in tissueClass[cata]:
                if tis==tissue:
                    FF.gzWrite(wt,line+'\t'+cata+'\n')
                    break_loop=True
                    break
            if break_loop==True:
                break
    wt.close()

def compareMethods():
    orign='D:\\Users\\xuechao\\Desktop\\orign.txt'
    dict_path='D:\\Users\\xuechao\\Desktop\\overlap.txt'
    out='D:\\Users\\xuechao\\Desktop\\out.txt'
    dic_iter=FF.getLineByPath(dict_path)
    dict={}
    dict['our']=[]
    dict['their']=[]
    for line in dic_iter:
        arr=line.split('\t')
        dict['our'].append(arr[0])
        dict['their'].append(arr[1])
    print(len(dict['our']))
    print(len(dict['their']))
    wt=FF.getWriter(out,False)
    ori_iter=FF.getLineByPath(orign)
    for line in ori_iter:
        arr=line.split('\t')
        for tis in arr:
            if tis in dict['our']:
                FF.gzWrite(wt,tis+'\t')
                continue
            if tis in dict['their']:
                FF.gzWrite(wt,dict['our'][dict['their'].index(tis)]+'\t')
                continue
            else:
                FF.gzWrite(wt,'\t')
        FF.gzWrite(wt,'\n')
    wt.close()

def getDataFrame():
    input='F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\compare.txt'
    out='F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\compareDataFrame.txt'
    wt=FF.getWriter(out,False)
    iter=FF.getLineByPath(input)
    dataframe={}
    diseases='BD,CAD,Height,RA,TC'.split(',')
    for dis in diseases:
        dataframe[dis]={}
        dataframe[dis]['our']=[]
        dataframe[dis]['their'] = []
    for line in iter:
        arr=line.split('\t')
        dataframe['BD']['our'].append(arr[0])
        dataframe['BD']['their'].append(arr[1])
        dataframe['CAD']['our'].append(arr[2])
        dataframe['CAD']['their'].append( arr[3])
        dataframe['Height']['our'].append( arr[4])
        dataframe['Height']['their'].append( arr[5])
        dataframe['RA']['our'].append(arr[6])
        dataframe['RA']['their'].append( arr[7])
        dataframe['TC']['our'].append(arr[8])
        dataframe['TC']['their'].append( arr[9])
    wt.write('TraitDisease\tMethod\tTissueCellType\tRank\n')
    tissueSet=sorted(dataframe['BD']['our'])
    for dis in dataframe.keys():
        for met in dataframe[dis].keys():
            for tis in tissueSet:
                wt.write(dis+'\t'+met+'\t'+tis+'\t'+str(len(dataframe[dis][met])-dataframe[dis][met].index(tis))+'\n')
    wt.close()

def getNGData():
    overlap = 'F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\overlap.txt'
    out='F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\NGdata.txt'
    input='F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\NGresults.txt'
    dic_iter=FF.getLineByPath(overlap)
    dict={}
    dict['our']=[]
    dict['their']=[]
    for line in dic_iter:
        arr=line.split('\t')
        dict['our'].append(arr[0])
        dict['their'].append(arr[1])
    ng_iter=FF.getLineByPath(input)
    dis_tis={}
    tiss=[]
    diss=ng_iter.__next__().split('\t')[1:]
    print(diss)
    for dis in diss:
        dis_tis[dis]=[]
    for line in ng_iter:
        arr=line.split('\t')
        if arr[0] in dict['their']:
            tiss.append(dict['our'][dict['their'].index(arr[0])])
            for i in range(len(diss)):
                dis_tis[diss[i]].append(arr[i+1])
    wt=FF.getWriter(out,False)
    wt.write('TraitDisease\tTissueCellType\tValue\n')
    for dis in dis_tis.keys():
        for i in range(len(dis_tis[dis])):
            wt.write(dis+'\t'+tiss[i]+'\t'+str(dis_tis[dis][i])+'\n')
    wt.close()



def filterOurResult():
    overlap = 'F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\overlap.txt'
    out='F:\\Projects\\TEA\\GWAS_tmp\\analysis\\Rplot\\OurData_v3.tpm_0.01.AddCategories2.txt'
    input='F:\Projects\TEA\GWAS_tmp\\analysis\Rplot\\tea.enrich_v3.tpm_0.01.forRplot.txt'
    dic_iter=FF.getLineByPath(overlap)
    dict={}
    dict['our']=[]
    dict['their']=[]
    for line in dic_iter:
        arr=line.split('\t')
        dict['our'].append(arr[0])
        dict['their'].append(arr[1])
    ng_iter=FF.getLineByPath(input)
    wt=FF.getWriter(out,False)
    wt.write(ng_iter.__next__()+'\n')
    for line in ng_iter:
        if line.split('\t')[1] in dict['our']:
            wt.write(line+'\n')
    wt.close()

if __name__=="__main__":
    pass
    #getDataFrame()
    #getNGData()
    classTissues()
    filterOurResult()
