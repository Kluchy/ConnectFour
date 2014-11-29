processedData= []
with open("connect-4.data", 'r') as f:
    for line in f:
        line= line.split(",")
        newLine=[]
        for entry in line:
            if entry == "o":
                newLine.append("2")
            elif entry == "x":
                newLine.append("1")
            elif entry == "b":
                newLine.append("0")
            else:
                newLine.append(entry)
        newLine= ','.join( newLine )
        processedData.append( newLine )
        
with open("Connect4Train.data",'w+') as f:
    for line in processedData:
        f.write(line)