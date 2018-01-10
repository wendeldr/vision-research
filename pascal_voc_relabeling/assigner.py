import untangle
import glob
import os
import subprocess
import pickle
import psutil
import time


from PIL import Image, ImageDraw

#load in dic of already labeled images
with open('images.pickle', 'rb') as handle:
    images = pickle.load(handle)


def appd(x, lbl):
    if x in images:
        images[x].append(lbl)
    else:
        images[x] = [lbl]

#load in list of images
with open('imgLst.pickle', 'rb') as handle:
    imgLst = pickle.load(handle)


#for images in image list
cnt = 0
imgListCount = len(imgLst)
while len(imgLst) != 0:
    cnt += 1
    img = imgLst.pop(0)
    xml = untangle.parse('/home/dan/git/pascal_voc/VOCdevkit/VOC2007/Annotations/' + img[:-3] + 'xml')

    # determine the bb of the ppl in the image
    box = []
    for obj in xml.annotation.object:
        if obj.name.cdata == 'person':
            box.append(((int(obj.bndbox.xmin.cdata), int(obj.bndbox.ymin.cdata)),
                        (int(obj.bndbox.xmax.cdata), int(obj.bndbox.ymax.cdata))))
    subCount = 1 
    # for each person in image
    for i, x in enumerate(box):
        im = Image.open('/home/dan/git/pascal_voc/VOCdevkit/VOC2007/JPEGImages/' + img)

        draw = ImageDraw.Draw(im)
        draw.rectangle([x[0], x[1]], outline='fuchsia')
        del draw
        im.show()
        time.sleep(.100)
        subprocess.Popen(['wmctrl', '-a', 'blobcom'])

        labeled = False
        fail = False
        while labeled == False:
            lbl = input("{0}/{1} | {2}/{3} | {4} (1:standing, 2:sitting, 3:inbetween, 9:na): ".format(subCount, len(box), cnt, imgListCount, img))

            if lbl == '1':
                labeled = True
                appd(img[:-4], 'standing')
            elif lbl == '2':
                labeled = True
                appd(img[:-4], 'sitting')
            elif lbl == '3':
                labeled = True
                appd(img[:-4], 'inbetween')
            elif lbl == '9':
                labeled = True
                appd(img[:-4], 'na')

            elif lbl == 'redo':
                num = input('#:')
                if num in images:
                    images[num] = []
                    images[img[:-4]] = []
                    imgLst.insert(0, img)
                    imgLst.insert(0, num + '.jpg')
                else:
                    images[img[:-4]] = []
                    imgLst.insert(0, img)
                imgListCount += 1
                fail = True
                break
            if labeled == True:
                subCount += 1


        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

        if fail:
            break

    with open('imgLst.pickle', 'wb') as handle:
        pickle.dump(imgLst, handle)

    with open('images.pickle', 'wb') as handle:
        pickle.dump(images, handle)
