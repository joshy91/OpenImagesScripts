import pandas as pd
object_segs = pd.read_csv('challenge-2019-train-segmentation-masks.csv')
object_labels = pd.read_csv('challenge-2019-classes-description-segmentable.csv',header=None)
object_val_segs = pd.read_csv('challenge-2019-validation-segmentation-masks.csv')

object_labels = pd.DataFrame(object_labels)

label_dic = {}
for index, row in object_labels.iterrows():
    label_dic[row[0]]=row[1]
    
object_segs = pd.DataFrame(object_segs)
object_segs = object_segs.sort_values(by=['ImageID', 'LabelName'])

object_val_segs = pd.DataFrame(object_val_segs)
object_val_segs = object_val_segs.sort_values(by=['ImageID', 'LabelName'])

Name = []
for row in object_segs['LabelName']:
    Name.append(label_dic[row])
    
Name_val = []
for row in object_val_segs['LabelName']:
    Name_val.append(label_dic[row])
    
object_segs['Name']=Name
my_list = list(set(object_segs['ImageID']))
num = 0
for item in object_segs['ImageID']:
    if item.startswith('1'):
        num += 1
num

object_val_segs['Name']=Name_val

object_segs.to_csv(r'./instanceSegmentationData.csv',index=False)

object_val_segs.to_csv(r'./instanceSegmentationValData.csv',index=False)

import csv
import imagesize

csvFile = 'instanceSegmentationData.csv'


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
    if row[1].startswith('1'):
        if row[1] != picId and rowNum2 == 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('</annotation>' + "\n")
            rowNum2 = 1
        if row[1] != picId and rowNum != 0:
            xmlFile = './training/annots/' + row[1] + '.xml'
            xmlData = open(xmlFile, 'w')
            rowNum2 = 2


        if row[1] != picId and rowNum != 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('<annotation>' + "\n")
            xmlData.write('    ' +'<filename>'+row[1] +'.jpg'+'</filename>'+ "\n")
            width, height = imagesize.get('./training/images/'+row[1] +'.jpg')
            xmlData.write('    ' +'<size>'+ "\n")
            xmlData.write('    ' +'    '+'<height>'+str(height) +'</height>'+ "\n")
            xmlData.write('    ' +'    '+'<width>'+str(width) +'</width>'+ "\n")
            xmlData.write('    ' +'    '+'<depth>'+'3' +'</depth>'+ "\n")
            xmlData.write('    ' +'</size>'+ "\n")

        if row[1] == picId or rowNum2 ==2:
            xmlData = open(xmlFile, 'a')
            xmlData.write('    ' +'<object>'+ "\n")
            xmlData.write('    ' +'    '+'<MaskPath>'+row[0] +'</MaskPath>'+ "\n")
            xmlData.write('    ' +'    '+'<Name>'+row[-1] +'</Name>'+ "\n")
            xmlData.write('    ' +'    ' +'<bndbox>'+ "\n")    
            for i in range(3,8):
                xmlData.write('    ' + '    ' + '    ' +'<' + tags[i+1] + '>' \
                              + row[i+1] + '</' + tags[i+1] + '>' + "\n")
            xmlData.write('    ' +'    ' +'</bndbox>'+ "\n")
            xmlData.write('    ' +'    '+'<PredictedIOU>'+row[8] +'</PredictedIOU>'+ "\n")
            xmlData.write('    ' +'</object>'+ "\n")
            rowNum2 = 0


        if rowNum !=0:
            picId = row[1]
        rowNum +=1
    else:
        rowNum +=1
    
import csv
import imagesize

csvFile = 'instanceSegmentationValData.csv'


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
            
    if row[1].startswith('1'):
        if row[1] != picId and rowNum2 == 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('</annotation>' + "\n")
            rowNum2 = 1
        if row[1] != picId and rowNum != 0:
            xmlFile = './test/annots/' + row[1] + '.xml'
            xmlData = open(xmlFile, 'w')
            rowNum2 = 2


        if row[1] != picId and rowNum != 0:
            xmlData = open(xmlFile, 'a')
            xmlData.write('<annotation>' + "\n")
            xmlData.write('    ' +'<filename>'+row[1] +'.jpg'+'</filename>'+ "\n")
            width, height = imagesize.get('./test/images/'+row[1] +'.jpg')
            xmlData.write('    ' +'<size>'+ "\n")
            xmlData.write('    ' +'    '+'<height>'+str(height) +'</height>'+ "\n")
            xmlData.write('    ' +'    '+'<width>'+str(width) +'</width>'+ "\n")
            xmlData.write('    ' +'    '+'<depth>'+'3' +'</depth>'+ "\n")
            xmlData.write('    ' +'</size>'+ "\n")

        if row[1] == picId or rowNum2 ==2:
            xmlData = open(xmlFile, 'a')
            xmlData.write('    ' +'<object>'+ "\n")
            xmlData.write('    ' +'    '+'<MaskPath>'+row[0] +'</MaskPath>'+ "\n")
            xmlData.write('    ' +'    '+'<Name>'+row[-1] +'</Name>'+ "\n")
            xmlData.write('    ' +'    ' +'<bndbox>'+ "\n")    
            for i in range(3,8):
                xmlData.write('    ' + '    ' + '    ' +'<' + tags[i+1] + '>' \
                              + row[i+1] + '</' + tags[i+1] + '>' + "\n")
            xmlData.write('    ' +'    ' +'</bndbox>'+ "\n")
            xmlData.write('    ' +'    '+'<PredictedIOU>'+row[8] +'</PredictedIOU>'+ "\n")
            xmlData.write('    ' +'</object>'+ "\n")
            rowNum2 = 0


        if rowNum !=0:
            picId = row[1]
        rowNum +=1
    else:
        pizza = 0
        rowNum +=1
    
    