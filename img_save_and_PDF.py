#카드뉴스의 이미지 저장하기
#pip install requests
import requests

#이미지 url 생성하기
# http://menu.mt.co.kr/ttimes/img/201510/2015102314167722908_66575_0.jpg

#이미지는 몇장인지 구하기 -----200은 정상, 404는  not found
# for i in range(20):
#     url = f'http://menu.mt.co.kr/ttimes/img/201510/2015102314167722908_66575_{i}.jpg'
#     res=requests.get(url)
#     print(i,url,res)

for i in range(13):
    url = f'http://menu.mt.co.kr/ttimes/img/201510/2015102314167722908_66575_{i}.jpg'
    res=requests.get(url)
    fpath=f'TTnews_img{i:03d}.jpg'
    open(fpath,'wb').write(res.content)


#pdf로 저장하기
#pip install reportlab
import glob
import os
from reportlab.pdfgen import canvas
from PIL import Image

flist = glob.glob('TTnews_img*.jpg')

im=Image.open(flist[0])
imgsize=im.size
w,h=imgsize
c=canvas.Canvas('TTnews.pdf',pagesize=imgsize)
for fpath in flist:
    c.drawImage(fpath,0,0,w,h)
    c.showPage()
c.save()
