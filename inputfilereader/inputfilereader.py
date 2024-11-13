import mbsObject
import json

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
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))       # -*-*-*-*-*-*-*
            currentBlockType = ""
            
    for type_i in searchForObjects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break
    currentTextBlock.append(line)

modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)
jDataBase = json.dumps({"modelObjects": modelObjects})
with open("inputfilereader/test.json", "w") as outfile:
    outfile.write(jDataBase)


f = open("inputfilereader/test.json", "r")
data = json.load(f)
f.close()

fds = open("inputfilereader/test.fds","w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputFile(fds)
fds.close()


print(len(listOfMbsObjects))            
print("Nußbaumer Linda")











