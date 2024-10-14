#this Script was wrote by Yongjun Song
#use Python3 to run this script
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#the function is output the parameters in 'par.inp'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def outPar(inpX):
    a=['*parameter \n']
    a.append(f'BF1 = {inpX[0]} \n')
    a.append(f'HF1 = {inpX[1]} \n')
    a.append(f'BF2 = {inpX[2]} \n')
    a.append(f'HF2 = {inpX[3]} \n')
    a.append(f'BF3 = {inpX[4]} \n')
    a.append(f'HF3 = {inpX[5]} \n')
    a.append(f'TF1 = {inpX[6]} \n')
    a.append(f'ShellT = {inpX[7]} \n')
    with open('par.inp','w') as f1:
        for i in a:
            f1.write(i) 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#the function is call abaqus2022 to calculate
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
def runCal():
    os.system('call abq2022 job=test cpus=6 user=Load2case.for int ask=off')
    os.system('call abq2022 cae noGui=getMaxMises.py ')
    with open('outMaxMises.txt',encoding='UTF-8') as outSf:
        outS = outSf.readlines()
    MaxMises = float(outS[0])
    return MaxMises
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#the function is calculate the all sensities of parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
def getDelt(inpX):
    global S 
    global bound1
    delt = []
    for i in range(len(inpX)):
        inpXtemp = inpX.copy()
        if inpX[i] <=bound1[i]:
            delt.append(9999)
            continue        
        if i < 6 :
            kappa = -1
        else:
            kappa = -0.1        
        inpXtemp[i] = inpXtemp[i] + kappa
        outPar(inpXtemp)
        S2 = runCal()
        tmpD = -(S2-S)/kappa
        delt.append(tmpD)
    return delt
def optM(inpX):
    MM=2*inpX[6]*(73015*(inpX[1]+inpX[0])+25900*(inpX[2]+inpX[3])+94948*(inpX[4]+inpX[5])) \
        +24749891*inpX[7]
    return MM
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#the intital parameter
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
b1 = 100
h1 = 200
b2 = 200
h2 = 200
b3 = 200
h3 = 300
t1 = 10
t2 = 20
inpX=[b1,h1,b2,h2,b3,h3,t1,t2]
bound1 = [60,100,150,150,150,250,6.0,8.0]
Vlog = []
Slog = []
outPar(inpX)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#begin the script
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
ir=1
while True:
    S = runCal()
    V = optM(inpX)
    v_log=f'{ir}    {V}\n'
    s_log=f'{ir}    {S}\n'
    Vlog.append(v_log)
    Slog.append(s_log) 
    ir = ir+1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    delt = getDelt(inpX)
    deltSort = delt.copy()
    deltSort.sort()
    for k in deltSort:
        idx=8
        idx1=delt.index(k)
        if inpX[idx1]>bound1[idx1]:    
            idx = idx1
            break
    if idx==8:
        break
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
    if idx < 6:
        inpX[idx]= inpX[idx]-5
    else:
        inpX[idx]= inpX[idx]-0.5
    outPar(inpX)
    
    if S >200:
        break    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Output the object fuction and Mises Stress in every calculate steps
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
with open('V.log','w') as f2:
    for i in Vlog:
        f2.write(i)
with open('S.log','w') as f3:
    for i in Slog:
        f3.write(i)