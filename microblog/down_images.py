#coding=utf-8
import os
import urllib2,cookielib,requests
from config import basedir
from app.string import md5
from app.models import PhotoData
from app import db
from pillow_image import IsValidImage

def downimage(urllist,dir):

 for url in urllist:
    path = os.path.join(basedir, 'uploads2\\')
    #url = "http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMeFhyTHc2V2t2YUFJZU5uN2pnTExIRFppUFI4bmVGWWVnPT0.jpg"

    filepath = path+dir+"\\"
    if os.path.exists(filepath) is False:
        os.makedirs(filepath)
    name = md5(url)+".jpg"
    imgaefile = filepath +name
    '''
    response = requests.get(url, stream=True)
    data = response.content
    '''
    if os.path.exists(imgaefile) is False or IsValidImage(imgaefile) is False:
       try:
          # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
          cj = cookielib.LWPCookieJar()
          opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
          urllib2.install_opener(opener)

          req = urllib2.Request(url)
          operate = opener.open(req)
          data = operate.read()
       except:
          print('网络发生异常'+imgaefile)
          continue
       else:
          f = open(imgaefile, 'wb')
          f.write(data)
          f.close()
    detail = PhotoData.query.filter_by(thumb=url).first()
    detail.filepath = name;
    db.session.add(detail)
    db.session.commit()