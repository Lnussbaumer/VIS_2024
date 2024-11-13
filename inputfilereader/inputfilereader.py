import mbsObject


f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()                               # braucht man nicht zwingend 

#numOfRigidBodies = 0
#numOfConstraint = 0
currentBlockType ="" #
currentTextBlock = [] #
searchForObjects = ["RIGID_BODY", "CONSTRAINT"] #
listOfMbsObjects = [] #

for line in fileContent:
    if(line.find("$") >= 0):            #new block found
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.mbsObkect("body",currentTextBlock))
            currentBlockType = ""
            
    for type_i in searchForObjects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break
    currentTextBlock.append(line)
print(len(listOfMbsObjects))            













