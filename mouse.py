import re
import pyautogui as pg
import time
import win32gui
from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
import easyocr

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

def replace_color(img, src_clr, dst_clr):
    ''' 通过矩阵操作颜色替换程序
    @param	img:	图像矩阵
    @param	src_clr:	需要替换的颜色(r,g,b)
    @param	dst_clr:	目标颜色		(r,g,b)
    @return				替换后的图像矩阵
    '''
    img_arr = np.asarray(img, dtype=np.double)

    r_img = img_arr[:,:,0].copy()
    g_img = img_arr[:,:,1].copy()
    b_img = img_arr[:,:,2].copy()

    img = r_img * 256 * 256 + g_img * 256 + b_img
    src_color = src_clr[0] * 256 * 256 + src_clr[1] * 256 + src_clr[2] #编码

    r_img[img == src_color] = dst_clr[0]
    g_img[img == src_color] = dst_clr[1]
    b_img[img == src_color] = dst_clr[2]

    dst_img = np.array([r_img, g_img, b_img], dtype=np.uint8)
    dst_img = dst_img.transpose(1,2,0)

    return dst_img

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
tarMat=get_matr_from_img_file("folder.png")
jointFolderMat=get_matr_from_img_file("folder_joint.png")
downTriMat=get_matr_from_img_file("down_tri.png")
rightTriMat=get_matr_from_img_file("right_tri.png")

def find_all_folder_logos(src):
    ret1=[]
    ret2=[]
    ret=[]
    f_rect=(40,0,160,len(src))
    time_start=time.time()
    for r in find_logo_with_sliding_window(src,tarMat):
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

    rs1=find_logo_with_sliding_window(srcMat,tarMat)
    rs2=find_logo_with_sliding_window(srcMat,jointFolderMat)

    time_end=time.time()
    cost=time_end-time_start
    print('time cost',cost,'s')

def show_array_img(src):
    img=Image.fromarray(src)
    img.show()

def find_first_folder_logo(pic):
    for r in find_logo_with_sliding_window(pic,tarMat):
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
    fs=find_logo_with_sliding_window(pic,tarMat)
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
    #bboxes_img = img.copy()
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cntr in contours:
        x,y,w,h = cv2.boundingRect(cntr)
        #cv2.rectangle(bboxes_img, (x, y), (x+w, y+h), (0, 0, 255), 1)
        bboxes.append((x,y,w,h))
    return bboxes

split_img(np.array(TakePic()))

test_read_folder()
print("hlelo")