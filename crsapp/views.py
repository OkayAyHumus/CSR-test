from curses.ascii import HT
from django.shortcuts import render, redirect
from .forms import ImageForm
from django.http import HttpResponse
from scipy.spatial import distance
from .models import ModelFile
from .forms import LoginForm, SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import os
import cv2
import copy
import numpy as np
import js2py
import math

import sys
sys.path.append('./crsapp')
sys.path.append('../Crsproject')
sys.path.append('./media')

from src import util
from src.body import Body



# def image_upload(request):
#     if request.method == 'POST':
#          form = ImageForm(request.POST, request.FILES)
#          if form.is_valid():
#             form.save()
#             image_name =request.FILES['image']
#             image_url ='media/documents/{}'.format(image_name)
#             return render(request, 'crsapp/image.html', {'image_url':image_url})
#     else:
#         form =ImageForm()
#         return render(request, 'crsapp/index.html',{'form':form})


@login_required
def image_upload(request):
        box=[]
        xbox=[]
        ybox=[]
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            
            if form.is_valid():
                form.save()
                image_name =request.FILES['image']
            
                body_estimation = Body('./model/body_pose_model.pth')
                
                target_image_path = './media/documents/{}'.format(image_name)
           
                oriImg = cv2.imread(target_image_path)  # B,G,R order
                print(type(oriImg))
                candidate, subset = body_estimation(oriImg)
                canvas = copy.deepcopy(oriImg)
                canvas = util.draw_bodypose(canvas, candidate, subset)
                # candidate から座標を取り出す部分を記述
                basename_name = os.path.splitext(os.path.basename(target_image_path))[0]
                result_image_path = "./media/result/pose_" + basename_name + ".jpeg"
                cv2.imwrite(result_image_path, canvas)
                
                # subsetとcandidateそれぞれの抜き出し（util.py　から抜き出し）
                for i in range(18):
                    for n in range(len(subset)):
                        index = int(subset[n][i])
                        if index == -1:
                            continue
                        x, y = candidate[index][0:2]
                        xbox.append(x)
                        ybox.append(y)

            
                
                

                # 上手く検出できているかの判定
                if len(subset) == 0:
                    return render(request,'crsapp/alert.html')
                else:

                
                    # subsetから、検出できなかったキーポントを判定し、xyそれぞれの座標のリストに−１を差し込む

                    sbbox=[]

                    sbbox.append(int(subset[0][0]))
                    sbbox.append(int(subset[0][1]))
                    sbbox.append(int(subset[0][2]))
                    sbbox.append(int(subset[0][3]))
                    sbbox.append(int(subset[0][4]))
                    sbbox.append(int(subset[0][5]))
                    sbbox.append(int(subset[0][6]))
                    sbbox.append(int(subset[0][7]))
                    sbbox.append(int(subset[0][8]))
                    sbbox.append(int(subset[0][9]))
                    sbbox.append(int(subset[0][10]))
                    sbbox.append(int(subset[0][11]))
                    sbbox.append(int(subset[0][12]))
                    sbbox.append(int(subset[0][13]))
                    sbbox.append(int(subset[0][14]))
                    sbbox.append(int(subset[0][15]))
                    sbbox.append(int(subset[0][16]))
                    sbbox.append(int(subset[0][17]))

                    idbox=[]
                    sbboxlist=list(enumerate(sbbox))
                    
                    for i in range(18):
                        if sbboxlist[i][1] < 0 :
                            idbox.append(sbboxlist[i][0])

                    for j in idbox:
                        xbox.insert(j, -1)
                        ybox.insert(j, -1)
                    # subsetから、検出できなかったキーポントを判定し、xyそれぞれの座標のリストに-1を差し込むのがここまで

                    hantei=[]
                    hantei.append(xbox[0:2])    
                    hantei.append(xbox[5])    
                    hantei.append(xbox[14:15])  

                    if -1 in hantei:
                        return render(request,'crsapp/alert.html')
                    else:
                        # それぞれの座標の落とし込み
                        z0 =[]
                        z0.append(xbox[0])
                        z0.append(ybox[0])
                        z1 =[]
                        z1.append(xbox[1])
                        z1.append(ybox[1])
                        z2 =[]
                        z2.append(xbox[2])
                        z2.append(ybox[2])
                        z5 =[]
                        z5.append(xbox[5])
                        z5.append(ybox[5])
                        z14 =[]
                        z14.append(xbox[14])
                        z14.append(ybox[14])
                        z15 =[]
                        z15.append(xbox[15])
                        z15.append(ybox[15])
                        z16 =[]
                        z16.append(xbox[16])
                        z16.append(ybox[16])
                        z17 =[]
                        z17.append(xbox[17])
                        z17.append(ybox[17])
                        box.append(z0)
                        box.append(z1)
                        box.append(z2)
                        box.append(z5)
                        box.append(z16)
                        box.append(z17)

                        # ユークリッド距離の測定（spicyを使用）
                        if xbox[17]=='NAN':
                            if xbox[16]=='NAN':
                                right = round(distance.euclidean(z2, z14),2)
                                left = round(distance.euclidean(z5, z15),2)
                            elif xbox[15] > 0 :
                                right = round(distance.euclidean(z2, z14),2)
                                left = round(distance.euclidean(z5, z15),2)
                            else:
                                return render(request,'crsapp/alert.html')
                        else:
                                right = round(distance.euclidean(z2, z16),2)
                                left = round(distance.euclidean(z5, z17),2)
                        nn_dis=round(distance.euclidean(z1, z0),2)
                        bd_dis=round(distance.euclidean(z2, z5),2)
                        # 角度の計算
                        # https://www.higashisalary.com/entry/numpy-angle-calc　参照サイト
                        #角度の中心位置
                        # z1
                        # #方向指定1
                        # z0
                        # #方向指定2
                        # z2,z5

                        vec1=[xbox[0]-xbox[1],ybox[0]-ybox[1]]
                        # ０、１、５
                        vec2=[xbox[5]-xbox[1],ybox[5]-ybox[1]]
                        absvec1=np.linalg.norm(vec1)
                        absvec2=np.linalg.norm(vec2)
                        inner1=np.inner(vec1,vec2)
                        cos_theta1=inner1/(absvec1*absvec2)
                        theta1=math.degrees(math.acos(cos_theta1))


                        # ０、１、２
                        vec3=[xbox[2]-xbox[1],ybox[2]-ybox[1]]
                        absvec1=np.linalg.norm(vec1)
                        absvec3=np.linalg.norm(vec3)
                        inner2=np.inner(vec1,vec3)
                        cos_theta2=inner2/(absvec1*absvec3)
                        theta2=math.degrees(math.acos(cos_theta2))
                        # それぞれの角度s

                        theta1=int(round(theta1,2))
                        theta2=int(round(theta2,2))

                        # 首の横の倒れ具合・・距離
                        right_lv=right/left
                        left_lv =left/right

                        # 首の横の倒れ具合・・角度
                        tall = theta1+theta2
                        t_right=theta2/tall
                        t_left=theta1/tall

                        # 首の前への倒れ具合
                        nnbd = nn_dis/bd_dis

                        if right_lv < 0.45 or t_right < 0.25 :
                            answer1 ='右に傾きすぎです'
                        elif left_lv < 0.45 or t_left < 0.25: 
                            answer1 ='左に傾きすぎです'
                        else:
                            answer1 ='適正'

                        if nnbd < 0.30 :
                            answer2 ='前に傾きすぎです'
                        else:
                            answer2 ='適正'


                        # 推論結果から数値取得をして、計算結果をデータベス（modelsに格納）
                        
                        Modelfile=ModelFile.objects.order_by('id').reverse()[0]
                        Modelfile.right_lv = right_lv
                        Modelfile.left_lv = left_lv
                        Modelfile.theta1 = theta1
                        Modelfile.theta2 = theta2
                        Modelfile.nnbd = nnbd
                        Modelfile.save()

                        # 最終的な出力(HTMLに表示するための変数などの出力)
                        return render(request, 'crsapp/image.html', {'image_url':result_image_path,'right':right_lv, 'a1':answer1,'a2':answer2,})
            #条件外れたら 
            else:
                form =ImageForm()
                return render(request, 'crsapp/index.html',{'form':form})
         #条件外れたら 
        else:
            form =ImageForm()
            return render(request, 'crsapp/index.html',{'form':form})


# ログイン
class Login(LoginView):
    form_class = LoginForm
    template_name='crsapp/login.html'

# ログアウト
class Logout(LogoutView):
     template_name='crsapp/base.html'

    
# サインアップ
def signup(request):
    if request.method=='POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            new_user=authenticate(username=username, password=password)
            if new_user is not None:
                login(request, new_user)
                return redirect('index')
        else:
            form=SignUpForm()
            return render(request, 'crsapp/signup.html', {'form': form})
    else:
        form=SignUpForm()
        return render(request, 'crsapp/signup.html', {'form': form})

