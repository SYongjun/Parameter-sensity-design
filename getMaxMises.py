#-*-coding: UTF-8-*-
from odbAccess import *
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Author：Yongjun Song(Wuhan Institute of Technology)
#The function to get Max-Mises Stress 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getMaxMises(odbName,elsetName):
    elemset = elsetName
    odb = openOdb(path=odbName)
    assembly = odb.rootAssembly
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Inital the stress
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    maxMises = -0.1
    maxElem = 0
    maxFrame = -1
    Stress = 'S'
    isStressPresent = 0
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#find and compare the Mises Stress
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for step in odb.steps.values():
        for frame in step.frames:
            allFields = frame.fieldOutputs
            if (allFields.has_key(Stress)):
                isStressPresent = 1
                stressSet = allFields[Stress]
                if elemset:
                    stressSet = stressSet.getSubset(
                        region=elemset)      
                for stressValue in stressSet.values:                
                    if (stressValue.mises > maxMises):
                        maxMises = stressValue.mises
    odb.close()
    return maxMises
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#The odb name and the Element set name
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
odbName = 'test.odb'
elsetName = 'ALLE'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Output the result in the file 'outMaxMises.txt'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
maxMises = getMaxMises(odbName,elsetName)
f=file('outMaxMises.txt','w')
f.write(str(maxMises))
f.close