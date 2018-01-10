import pickle
import subprocess


#load in dic of already labeled images
with open('images_classified.pickle', 'rb') as handle:
    images = pickle.load(handle)

toPath = '/home/dan/blobcom/python/research/pascal_voc_relabeling/classified/'
fromPath = '/home/dan/git/pascal_voc/VOCdevkit/VOC2007/'

for key in images:
    subprocess.Popen(['mv', fromPath + 'Annotations/' + key + '.xml', toPath + 'reAnnotated/'])
    subprocess.Popen(['mv', fromPath + 'JPEGImages/' + key + '.jpg', toPath + 'imgs/'])