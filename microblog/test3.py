#coding=utf-8

from pillow_image import IsValidImage


file ="E:\python_project\microblog\uploads2\photo5\\7b6caebf488be798eb483629eb2a11a2.jpg"
file2 ="http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMeFhyTHc2V2t2YUFJZU5uN2pnTExIRFppUFI4bmVGWWVnPT0.jpg"
if IsValidImage(file2):
    print('1111')
else:
    print('22222')
