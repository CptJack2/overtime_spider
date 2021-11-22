import pyautogui as pg
import time
import win32gui
from PIL import ImageGrab
from PIL import Image
import numpy as np

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

scroll_start_pos=(325,74)
scroll_end_pos=(325,1398)
pic_rect=(0,70,330,1400)

def moveToScrollDownPos():
    pg.moveTo(scroll_end_pos[0],1400)
    pg.moveTo(scroll_end_pos)

def moveToScrollUpPos():
    pg.moveTo(scroll_start_pos[0],1400)
    pg.moveTo(scroll_start_pos)

def TakePic(posFunc=None):
    if posFunc!=None:
        posFunc()
        pg.click()
        pg.scroll(100)
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

def find_logo_with_sliding_window(src,logo,step=2,srcRatio=2,down_sample_step=3):
    lw,lh=get_width_height(logo)
    sw,sh=get_width_height(src)
    threshold=5
    for j in range(0,sh-lh+1,step):
        for i in range(0,
               int(sw/srcRatio-lw+1),
            step):
            partSrc=src[j:j+lh:down_sample_step,i:i+lw:down_sample_step,:3]
            tlogo=logo[::down_sample_step,::down_sample_step,:3]
            tlogo=tlogo[:len(partSrc),:len(partSrc[0])]
            dif= np.sum(np.absolute(partSrc-tlogo))  #compute_diff(logo,src[i:i+lw,j:j+lh])
            if dif < threshold:
                yield j,i

def find_all_logos_in_region(src,logo):
    r=[]
    for l in find_logo_with_sliding_window(src,logo,1,1,1):
        r.append(l)
    return r

def get_folder_stat(src,x,y):
    tri_rect=src[x:x+15,y-15:y]
    #show_array_img(tri_rect)
    if len(find_all_logos_in_region(tri_rect,downTriMat))!=0:
        return "open"
    if len(find_all_logos_in_region(tri_rect,rightTriMat))!=0:
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
    ret=[]
    for r in find_logo_with_sliding_window(src,tarMat):
        ret.append(r)
    for r in find_logo_with_sliding_window(src,jointFolderMat):
        ret.append(r)
    return ret

def test_find_logo():

    time_start=time.time()

    rs=[]
    rs2=[]
    for r in find_logo_with_sliding_window(srcMat,tarMat):
        rs.append(r)
    for r in find_logo_with_sliding_window(srcMat,jointFolderMat):
        rs2.append(r)

    time_end=time.time()
    assert(len(rs)==6)
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

def open_folders_shown():
    pic= np.array(TakePic())
    def openFunc(r):
        stat=get_folder_stat(pic,r[0],r[1])
        if stat=="close":
            pg.moveTo(r[1]+pic_rect[0],r[0]+pic_rect[1])
            pg.click()
            return True
        return False
    for r in find_logo_with_sliding_window(pic,tarMat):
        if openFunc(r):
            return
    for r in find_logo_with_sliding_window(pic,jointFolderMat):
        if openFunc(r):
            return


def test_get_folder_stat():
    folders=[
        (62, 76), (300, 76),
        (538, 76), (572, 62), (810, 76), (844, 76),(878, 62),
       ]
    fst=[]
    for f in folders:
        fst.append(get_folder_stat(srcMat,f[0],f[1]))
    print("he")

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

open_folders_shown()
print("hlelo")