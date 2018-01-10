import untangle
import glob
import os
import pickle


stand = []
sit = []
ibt = []


os.chdir("/home/dan/blobcom/python/research/pascal_voc_relabeling/classified/reAnnotated/")
for file in glob.glob("*.xml"):
    xml = untangle.parse('/home/dan/blobcom/python/research/pascal_voc_relabeling/classified/reAnnotated/' + file)

    for obj in xml.annotation.object:
        if obj.name.cdata == 'standing':
            stand.append(file)
        if obj.name.cdata == 'sitting':
            sit.append(file)
        if obj.name.cdata == 'inbetween':
            ibt.append(file)


print('standing')
print(stand)
print('=============')

print('sitting')
print(sit)
print('=============')

print('inbetween')
print(ibt)
print('=============')
