import re
import time

import cv2
import easyocr
import numpy as np
import pyautogui as pg
from PIL import Image
from PIL import ImageGrab

# pg.moveTo(1513,908)
# pg.click()
# pg.write("handsome man!")
# #time.sleep(1)
# pg.hotkey("win","space")
# pg.write("zhuer1 ")
# pg.press("enter")

#hwnd=win32gui.FindWindow(None,"企业微信-通讯录")
#rectwnd=win32gui.GetWindowRect(hwnd)
#b=win32gui.ShowWindow(hwnd,1)

scroll_start_pos=(332,80)
scroll_end_pos=(332,1394)
pic_rect=(0,70,330,1400)

reader = easyocr.Reader(['ch_sim','en'])

def ScrollDown():
    pg.moveTo(scroll_end_pos[0],1400)
    pg.moveTo(scroll_end_pos)
    pg.click()
    pg.scroll(100)

def ScrollUp():
    pg.moveTo(scroll_start_pos[0],1400)
    pg.moveTo(scroll_start_pos)
    pg.click()
    pg.scroll(-100)

def TakePic():
    return ImageGrab.grab(pic_rect)

def get_width_height(mat):
    return len(mat[0]),len(mat)

def compute_diff(mat1, mat2):
    w,h=get_width_height(mat1)
    diff=0
    for i in range(w):
        for j in range(h):
            for k in range(3):
                diff+=abs(mat1[j][i][k]-mat2[j][i][k])
    return diff

def find_logo_with_sliding_window(src,logo):
    tsrc=src[::,::,:3]
    tlogo=logo[::,::,:3]
    res = cv2.matchTemplate(tsrc,tlogo,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    ret=[]
    #h,w = logo.shape[:2]
    for pt in zip(*loc[::-1]):
        #cv.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        ret.append(pt)
    #img=Image.fromarray(src)
    #img.show()
    return ret

def find_all_logos_in_region(src,logo):
    r=[]
    for l in find_logo_with_sliding_window(src,logo):
        r.append(l)
    return r

def get_folder_stat(src,x,y):
    tri_rect=src[y:y+15,x-15:x]
    #show_array_img(tri_rect)
    if len(find_logo_with_sliding_window(tri_rect,downTriMat))!=0:
        return "open"
    if len(find_logo_with_sliding_window(tri_rect,rightTriMat))!=0:
        return "close"

def get_matr_from_img_file(fn):
    src=Image.open(fn)
    mat=np.array(src)
    return mat

srcMat=get_matr_from_img_file("a.png")
folderMat=get_matr_from_img_file("folder.png")
jointFolderMat=get_matr_from_img_file("folder_joint.png")
downTriMat=get_matr_from_img_file("down_tri.png")
rightTriMat=get_matr_from_img_file("right_tri.png")

def find_all_folder_logos(src):
    ret1=[]
    ret2=[]
    ret=[]
    f_rect=(40,0,160,len(src))
    time_start=time.time()
    for r in find_logo_with_sliding_window(src, folderMat):
        ret1.append(r)
    for r in find_logo_with_sliding_window(src,jointFolderMat):
        ret2.append(r)
    time_end=time.time()
    cost=time_end-time_start
    i=0
    j=0
    while i<len(ret1) and j<len(ret2):
        if ret1[i][0]<ret2[j][0]:
            ret.append(ret1[i])
            i+=1
        else:
            ret.append(ret2[j])
            j+=1
    while i<len(ret1):
        ret.append(ret1[i])
        i+=1
    while j<len(ret2):
        ret.append(ret2[j])
        j+=1
    return ret

def test_find_logo():

    time_start=time.time()

    rs1=find_logo_with_sliding_window(srcMat, folderMat)
    rs2=find_logo_with_sliding_window(srcMat,jointFolderMat)

    time_end=time.time()
    cost=time_end-time_start
    print('time cost',cost,'s')

def show_array_img(src):
    img=Image.fromarray(src)
    img.show()

def find_first_folder_logo(pic):
    for r in find_logo_with_sliding_window(pic, folderMat):
        return r
    for r in find_logo_with_sliding_window(pic,jointFolderMat):
        return r

def circle_target(src,locs,logo):
    h,w = logo.shape[:2]
    tsrc=np.copy(src)
    for l in locs:
        cv2.rectangle(tsrc, l, (l[0] + w, l[1] + h), (255,0,0), 1)
    img=Image.fromarray(tsrc)
    img.show()

def open_folders_shown():
    has_close=False
    pic= np.array(TakePic())
    fs=find_logo_with_sliding_window(pic, folderMat)
    fs.reverse()
    if len(fs)>0:
        fs.pop(0)
    # circle_target(pic,fs,tarMat)
    for r in fs:
        stat=get_folder_stat(pic,r[0],r[1])
        if stat=="close":
            pg.moveTo(r[0]+pic_rect[0],r[1]+pic_rect[1])
            pg.click()
            has_close=True
    return has_close

# def test_get_folder_stat():
#     folders=[
#         (62, 76), (300, 76),
#         (538, 76), (572, 62), (810, 76), (844, 76),(878, 62),
#        ]
#     fst=[]
#     for f in folders:
#         fst.append(get_folder_stat(srcMat,f[0],f[1]))
#     print("he")

def open_all_folders():
    while 1:
        b=open_folders_shown()
        if not b:
            ScrollDown()

def get_column_img(src,x,y):
    anchor_range=(-100,-2,300,20)
    return
# def get_folder_stat(src,x,y)
#
# def test_take_pic():
#     img =TakePic()
#     img.save("a.png","png")
#     img.show()
# pix = np.array(img)
#
# thresh = 200
# fn = lambda x : 255 if x > thresh else 0
# img = img.convert('L').point(fn, mode='1')
#
# np.linalg.norm()
#
# img.show()
row_height=35

def read_text_row(pic):
    res=reader.readtext(pic, detail = 0)
    return res[0]

def get_people_name(pic):
    text=read_text_row(pic)
    pat=re.compile(r"(\w+)[\(\[]*(\w+)[\)\]]*")
    match=pat.match(text)
    return match.group(1),match.group(2)

def get_row(pic,h):
    row=pic[h:h+row_height]
    return row

def read_folder(pic,hs,he):
    rf=get_row(pic,hs)
    fn=read_text_row(rf)
    for h in range(hs+row_height,he,row_height):
        r=get_row(pic,h)
        en,cn=get_people_name(r)

def test_read_folder():
    pic=get_matr_from_img_file("read_folder.png")
    read_folder(pic,0,len(pic))

def test_ocr():
    time_start=time.time()
    time_end=time.time()
    cost1=time_end-time_start
    result = reader.readtext(srcMat, detail = 0)
    time_end=time.time()
    cost=time_end-time_start
    print("kkk")

def split_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(gray, 200, 255)
    mask=255-mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    bboxes = []
    bboxes_img = img.copy()
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cntr in contours:
        x,y,w,h = cv2.boundingRect(cntr)
        bboxes.append((x,y,w,h))

    bboxes.sort(key=lambda b:b[1])
    i=0
    while i < len(bboxes) - 1:
        if abs(bboxes[i][1] - bboxes[i + 1][1]) <= 3 :
            neww=max(bboxes[i][0]+bboxes[i][2],bboxes[i+1][0]+bboxes[i+1][2])- \
                 min(bboxes[i][0],bboxes[i+1][0])
            newh=max(bboxes[i][1]+bboxes[i][3],bboxes[i+1][1]+bboxes[i+1][3])- \
                min(bboxes[i][1],bboxes[i+1][1])
            t = (min(bboxes[i][0],bboxes[i+1][0]),
               min(bboxes[i][1],bboxes[i+1][1]),
               neww,newh)
            del bboxes[i+1]
            del bboxes[i]
            bboxes.insert(i,t)
        else:
            i+=1

    for b in bboxes:
        x,y,w,h=b
        cv2.rectangle(bboxes_img, (x, y), (x+w, y+h), (0, 0, 255), 1)

    return bboxes,bboxes_img

def parse_box(box):
    type="people"
    stat="open"
    if len(find_logo_with_sliding_window(box, folderMat))!=0 or \
        len(find_logo_with_sliding_window(box, jointFolderMat))!=0:
        type="folder"
        if len(find_logo_with_sliding_window(box,downTriMat))!=0:
            stat="open"
        if len(find_logo_with_sliding_window(box,rightTriMat))!=0:
            stat="close"
    if type=="people":
        en,cn=get_people_name(box)
        return type,en,cn
    if type=="folder":
        fn=read_text_row(box)
        return type,stat,fn

groupStack=[]
allPeopleMap={}

#找到当前要遍历的文件夹位置
def get_folder_pos(folderName):
    src=np.array(TakePic())
    boxes,bimg=split_img(src)
    stat=None
    targetb=None
    for b in boxes:
        type,stat,fn=parse_box(src[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])
        if type=="folder" and fn==folderName:
            targetb=b
            break
    if not targetb:
        return None,None
    return targetb,stat

def read_folder_recur(folderName):
    pos,stat=get_folder_pos(folderName)
    if stat=="close":
        pg.moveTo(pos[0],pos[1]+pic_rect[1])
        pg.click()

    groupStack.append(folderName)

    src=np.array(TakePic())
    boxes,bimg=split_img(src)
    folders=[]
    for b in boxes:
        #不是这个文件夹内的跳过
        if b[1]<=pos[1] or\
           b[0]<=pos[0]-5:
            continue
        type,statOrEn,fnOrCn=parse_box(src[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])
        if type=="folder" :
            if b[0]>=pos[0]+5:
                folders.append(fnOrCn)
        else:
            if b[0]>=pos[0]+22:
                continue
            t=allPeopleMap
            for s in groupStack:
                if s not in t:
                    t[s]={}
                t=t[s]
            t[statOrEn]=(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    #folders=folders[:1]
    for f in folders:
        read_folder_recur(f)

    if stat=="open":
        pg.moveTo(pos[0],pos[1]+pic_rect[1])
        pg.click()

    print("kkk")

read_folder_recur("总办")
print("hek")


test_read_folder()
print("hlelo")