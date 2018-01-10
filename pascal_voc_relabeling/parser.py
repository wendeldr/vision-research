import untangle
import glob
import os
import pickle


imgLst = []
names = []
pose = []

os.chdir("/home/dan/git/pascal_voc/VOCdevkit/VOC2007/Annotations/")
for file in glob.glob("*.xml"):
    xml = untangle.parse('/home/dan/git/pascal_voc/VOCdevkit/VOC2007/Annotations/'+file)

    for obj in xml.annotation.object:
        names.append(obj.name.cdata)
        if obj.name.cdata == 'person':
            imgLst.append(xml.annotation.filename.cdata)
            pose.append(obj.pose.cdata)

imgLst = sorted(list(set(imgLst)))
os.chdir("/home/dan/blobcom/python/research/pascal_voc_relabeling")

with open('imgLst.pickle', 'wb') as handle:
    pickle.dump(imgLst, handle)

images = {}
with open('images.pickle', 'wb') as handle:
    pickle.dump(images, handle)
