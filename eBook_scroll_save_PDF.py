#교보문고 e북 캡쳐하기
#pip install pyautogui

import pyautogui
import time

#화면전환 (alt+tab으로 전환, 해당 e북페이지만 실행된 상태여야함)
pyautogui.keyDown('altleft')
pyautogui.press(['tab'])
time.sleep(1)
pyautogui.keyUp('altleft') 
# pyautogui.scroll('634') #스크롤정도 조정


for i in range(3): #저장할 페이지 수 수정
	screen = pyautogui.screenshot()
	page = screen.crop((635,175,1269,968))  #미리 페이지 캡쳐해서 그림판에서 좌표기록 (상,하,좌,우)
	page.save(f'page{i:03d}.png')
	# pyautogui.press(['right']) #오른쪽으로넘기는구조일경우
	pyautogui.scroll('300') #스크롤로내리는구조일경우
  
 
 
#PDF로 저장하기
#pip install reportlab

import glob
import os
from reportlab.pdfgen import canvas
from PIL import Image

flist = glob.glob('page*.png')

im = Image.open(flist[0])
pgsize = im.size
w,h = pgsize

c=canvas.Canvas('kyobo.pdf',pagesize=pgsize)
for fpath in flist:
	c.drawImage(fpath,0,0,w,h)
	c.showPage()
c.save()
