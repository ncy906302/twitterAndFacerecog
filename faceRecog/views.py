from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from faceRecog.models import *

from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier
import cv2
import numpy as np
import os

import json

from django.views.decorators.csrf import csrf_exempt

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None
def feat_match(feat1,feat2):
    a=np.array(feat1)
    b=np.array(feat2)
    sim = np.sum(a*b)/((np.sum(a*a) ** 0.5)*(np.sum(b*b) ** 0.5))
    return sim




@csrf_exempt
def readModel(request):
    global avdata
    avdata = {}
    fp = open("feat_list.txt", "r",encoding='shift_jis')
    name = fp.readline().strip('\n')
    

    while(name!= ''):
        feat_list = []
        num = fp.readline()
        for i in range(int(num)):
            feat = fp.readline()
            feat = feat.split(',')
            feat = np.array(feat,dtype=float)
            feat_list.append(feat)
        avdata[name]=feat_list
        name = fp.readline().strip('\n')
    fp.close()
    return render(request, 'faceRecog/match.html')


@csrf_exempt
def match(request):


    return render(request, 'faceRecog/match.html')



@csrf_exempt
def recog(request):
    global avdata

    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    detector.set_min_face_size(30)


    if request.method == 'POST':
        print(request.FILES['img'])
        path = tempIMG(
            img=request.FILES['img'],
        )
        path.save()
        image_color_A = imread(str(path.img))
        image_gray_A = cv2.cvtColor(image_color_A, cv2.COLOR_BGR2GRAY)
        faces_A = detector.detect(image_gray_A)
        length_list = []
        if len(faces_A) or 0:
            landmarks_A = aligner.align(image_gray_A, faces_A[0])
            feat_test = identifier.extract_feature_with_crop(image_color_A, landmarks_A)



        average_sim_list = []
        name_list = []
        sim_list=[]

        for cla in avdata:    
            simlist = []
            name_list.append(cla)
            weight =0
            for fea in avdata[cla]:
                sim = feat_match(feat_test,fea)
                simlist.append(sim)
                if sim > 0.5:
                    simlist.append(sim)
                if sim > 0.55:
                    simlist.append(sim)
                if sim > 0.6:
                    simlist.append(sim)
            sim_list.append(simlist)
            if len(simlist) == 0:
                average_sim_list.append(0)
            else:
                average_sim = sum(simlist)/len(simlist)
                average_sim_list.append(average_sim)

        # print(average_sim_list)    
        max_index = average_sim_list.index(max(average_sim_list))
        
        sort_list = sorted(average_sim_list)
        result_list =[]
        for j in range(5):
            result_list.append(name_list[average_sim_list.index(sort_list[-(j+1)])])
    
        print(name_list[max_index])
        print(average_sim_list[max_index])
    identifier.release()
    aligner.release()
    detector.release()
    content = {'result_list':result_list}

    return HttpResponse(json.dumps(content,ensure_ascii=False))