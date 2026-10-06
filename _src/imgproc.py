from PIL import Image, ImageDraw, ImageFilter
import numpy as np
def round_mask(im, r):
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],r,fill=255)
    out=im.convert("RGBA"); out.putalpha(m); return out
def crop_card(im, bg=(245,245,247), thr=12):
    a=np.asarray(im.convert("RGB")).astype(int)
    ys,xs=np.where(np.abs(a-np.array(bg)).sum(2)>thr)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
def norm(im, w=535, h=1160):
    # fit all screenshots to a common canvas so they line up on the page
    return im.convert("RGB").resize((w,h),Image.LANCZOS)
def save_shot(im, path):
    round_mask(im,int(im.width*0.085)).save(path,"WEBP",quality=86,method=6)
def save_icon(im, path, r=58):
    round_mask(im.convert("RGB").resize((256,256),Image.LANCZOS),r).save(path,"WEBP",quality=90)
