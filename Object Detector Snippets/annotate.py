import pandas as pd
object_bboxs = pd.read_csv('challenge-2019-train-detection-bbox.csv')
object_val_bboxs = pd.read_csv('challenge-2019-validation-detection-bbox.csv')
object_labels = pd.read_csv('challenge-2019-classes-description-500.csv',header=None)
object_labels = pd.DataFrame(object_labels)

label_dic = {}
for index, row in object_labels.iterrows():
    label_dic[row[0]]=row[1]
    
object_bboxs = pd.DataFrame(object_bboxs)
object_val_bboxs = pd.DataFrame(object_val_bboxs)

Name = []
for row in object_bboxs['LabelName']:
    Name.append(label_dic[row])
    
Name_val = []
for row in object_val_bboxs['LabelName']:
    Name_val.append(label_dic[row])
    
object_bboxs['Name']=Name


object_val_bboxs['Name']=Name_val

object_bboxs.to_csv(r'./objectDetectionData.csv',index=False)
object_val_bboxs.to_csv(r'./objectDetectionValData.csv',index=False)

import csv
import imagesize

csvFile = 'objectDetectionData.csv'


csvData = csv.reader(open(csvFile))

# there must be only one top-level tag

rowNum = 0
rowNum2 = 1
for row in csvData:
    
    if rowNum == 0:
        tags = row
        picId = 0
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
            
    if row[0].startswith('1'):
        if row[0] != picId and rowNum2 == 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('</annotation>' + "\n")
            rowNum2 = 1
        if row[0] != picId and rowNum != 0:
            xmlFile = './training/annots/' + row[0] + '.xml'
            xmlData = open(xmlFile, 'w')
            rowNum2 = 2


        if row[0] != picId and rowNum != 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('<annotation>' + "\n")
            xmlData.write('    ' +'<filename>'+row[0] +'.jpg'+'</filename>'+ "\n")
            width, height = imagesize.get('./training/images/'+row[0] +'.jpg')
            xmlData.write('    ' +'<size>'+ "\n")
            xmlData.write('    ' +'    '+'<height>'+str(height) +'</height>'+ "\n")
            xmlData.write('    ' +'    '+'<width>'+str(width) +'</width>'+ "\n")
            xmlData.write('    ' +'    '+'<depth>'+'3' +'</depth>'+ "\n")
            xmlData.write('    ' +'</size>'+ "\n")
            for i in range(1,(len(tags)-10)):
                xmlData.write('    ' + '<' + tags[i] + '>' \
                              + row[i] + '</' + tags[i] + '>' + "\n")

        if row[0] == picId or rowNum2 ==2:
            xmlData = open(xmlFile, 'a')
            xmlData.write('    ' +'<object>'+ "\n")
            for i in range(8,len(tags)-1):
                xmlData.write('    ' + '    ' + '<' + tags[i+1] + '>' \
                              + row[i+1] + '</' + tags[i+1] + '>' + "\n")
            xmlData.write('    ' +'    ' +'<bndbox>'+ "\n")    
            for i in range(3,len(tags)-6):
                xmlData.write('    ' + '    ' + '    ' +'<' + tags[i+1] + '>' \
                              + row[i+1] + '</' + tags[i+1] + '>' + "\n")
            xmlData.write('    ' +'    ' +'</bndbox>'+ "\n")
            xmlData.write('    ' +'</object>'+ "\n")
            rowNum2 = 0



        if rowNum !=0:
            picId = row[0]
        rowNum +=1
    else:
        pizza = 0
        rowNum +=1
import csv
import imagesize

csvFile = 'objectDetectionValData.csv'


csvData = csv.reader(open(csvFile))

# there must be only one top-level tag

rowNum = 0
rowNum2 = 1
for row in csvData:
    
    if rowNum == 0:
        tags = row
        picId = 0
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
            
    if row[0] != picId and rowNum2 == 0:
        xmlData = open(xmlFile, 'a')
        xmlData.write('</annotation>' + "\n")
        rowNum2 = 1
    if row[0] != picId and rowNum != 0:
        xmlFile = './test/annots/' + row[0] + '.xml'
        xmlData = open(xmlFile, 'w')
        rowNum2 = 2


    if row[0] != picId and rowNum != 0:
        xmlData = open(xmlFile, 'a')
        xmlData.write('<annotation>' + "\n")
        xmlData.write('    ' +'<filename>'+row[0] +'.jpg'+'</filename>'+ "\n")
        width, height = imagesize.get('./test/images/'+row[0] +'.jpg')
        xmlData.write('    ' +'<size>'+ "\n")
        xmlData.write('    ' +'    '+'<height>'+str(height) +'</height>'+ "\n")
        xmlData.write('    ' +'    '+'<width>'+str(width) +'</width>'+ "\n")
        xmlData.write('    ' +'    '+'<depth>'+'3' +'</depth>'+ "\n")
        xmlData.write('    ' +'</size>'+ "\n")
        for i in range(1,(len(tags)-10)):
            xmlData.write('    ' + '<' + tags[i] + '>' \
                          + row[i] + '</' + tags[i] + '>' + "\n")

    if row[0] == picId or rowNum2 ==2:
        xmlData = open(xmlFile, 'a')
        xmlData.write('    ' +'<object>'+ "\n")
        for i in range(8,len(tags)-1):
            xmlData.write('    ' + '    ' + '<' + tags[i+1] + '>' \
                          + row[i+1] + '</' + tags[i+1] + '>' + "\n")
        xmlData.write('    ' +'    ' +'<bndbox>'+ "\n")    
        for i in range(3,len(tags)-6):
            xmlData.write('    ' + '    ' + '    ' +'<' + tags[i+1] + '>' \
                          + row[i+1] + '</' + tags[i+1] + '>' + "\n")
        xmlData.write('    ' +'    ' +'</bndbox>'+ "\n")
        xmlData.write('    ' +'</object>'+ "\n")
        rowNum2 = 0



    if rowNum !=0:
        picId = row[0]
    rowNum +=1
