# -*- coding:utf-8 -*-
"""
调用云畅快转转码
视频转换为mp4,1个文件支持转换多个,标清,高清,超清
文档转换为swf
支持平滑过渡,迁移,离线三种模式
"""
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import ConfigParser
import random
# import re
import getopt
from datetime import datetime
import logging
import subprocess
import urlparse
import Image
import ImageChops
import ImageOps
import shutil
import glob
import platform
import guanfu_common_task as task

process_path = ''


def addslashes(s):
    # l = ["\\", '"', "'", "\0", ]
    l = ["$", '"', ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\' + i)
    return s


def autoCrop(image, backgroundColor=None):
    '''Intelligent automatic image cropping.
       This functions removes the usless "white" space around an image.

       If the image has an alpha (tranparency) channel, it will be used
       to choose what to crop.

       Otherwise, this function will try to find the most popular color
       on the edges of the image and consider this color "whitespace".
       (You can override this color with the backgroundColor parameter)

       Input:
            image (a PIL Image object): The image to crop.
            backgroundColor (3 integers tuple): eg. (0,0,255)
                 The color to consider "background to crop".
                 If the image is transparent, this parameters will be ignored.
                 If the image is not transparent and this parameter is not
                 provided, it will be automatically calculated.

       Output:
            a PIL Image object : The cropped image.
    '''

    def mostPopularEdgeColor(image):
        ''' Compute who's the most popular color on the edges of an image.
            (left,right,top,bottom)

            Input:
                image: a PIL Image object

            Ouput:
                The most popular color (A tuple of integers (R,G,B))
        '''
        im = image
        if im.mode != 'RGB':
            im = image.convert("RGB")

        # Get pixels from the edges of the image:
        width, height = im.size
        left = im.crop((0, 1, 1, height - 1))
        right = im.crop((width - 1, 1, width, height - 1))
        top = im.crop((0, 0, width, 1))
        bottom = im.crop((0, height - 1, width, height))
        pixels = left.tostring() + right.tostring() + top.tostring() + bottom.tostring()

        # Compute who's the most popular RGB triplet
        counts = {}
        for i in range(0, len(pixels), 3):
            RGB = pixels[i] + pixels[i + 1] + pixels[i + 2]
            if RGB in counts:
                counts[RGB] += 1
            else:
                counts[RGB] = 1

                # Get the colour which is the most popular:
        mostPopularColor = sorted([(count, rgba) for (rgba, count) in counts.items()], reverse=True)[0][1]
        return ord(mostPopularColor[0]), ord(mostPopularColor[1]), ord(mostPopularColor[2])

    bbox = None

    # If the image has an alpha (tranparency) layer, we use it to crop the image.
    # Otherwise, we look at the pixels around the image (top, left, bottom and right)
    # and use the most used color as the color to crop.

    # --- For transparent images -----------------------------------------------
    if 'A' in image.getbands():  # If the image has a transparency layer, use it.
        # This works for all modes which have transparency layer
        bbox = image.split()[list(image.getbands()).index('A')].getbbox()
    # --- For non-transparent images -------------------------------------------
    elif image.mode == 'RGB':
        if not backgroundColor:
            backgroundColor = mostPopularEdgeColor(image)
        # Crop a non-transparent image.
        # .getbbox() always crops the black color.
        # So we need to substract the "background" color from our image.
        bg = Image.new("RGB", image.size, backgroundColor)
        diff = ImageChops.difference(image, bg)  # Substract background color from image
        bbox = diff.getbbox()  # Try to find the real bounding box of the image.
    else:
        raise NotImplementedError, "Sorry, this function is not implemented yet for images in mode '%s'." % image.mode

    if bbox:
        image = image.crop(bbox)

    return image


def resize_ratio_img(src, dst, dst_w, dst_h, quality):
    im = Image.open(src)
    if im.mode != 'RGB':
        im = im.convert("RGB")

    ori_w, ori_h = im.size
    width_ratio = height_ratio = None
    ratio = 1
    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            width_ratio = float(dst_w) / ori_w  # 正确获取小数的方式
        if dst_h and ori_h > dst_h:
            height_ratio = float(dst_h) / ori_h

        if width_ratio and height_ratio:
            if width_ratio < height_ratio:
                ratio = width_ratio
            else:
                ratio = height_ratio

        if width_ratio and not height_ratio:
            ratio = width_ratio
        if height_ratio and not width_ratio:
            ratio = height_ratio

        new_width = int(ori_w * ratio)
        new_height = int(ori_h * ratio)
    else:
        new_width = ori_w
        new_height = ori_h

    im.resize((new_width, new_height), Image.ANTIALIAS).save(dst, 'JPEG', quality=100)

    '''
    image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''


def list_files(curr_dir='.', ext='*.*'):
    """当前目录下的文件"""
    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i


def remove_files(rootdir, ext, show=False, exclude=''):
    """删除rootdir目录下的符合的文件"""
    for i in list_files(rootdir, ext):
        if show:
            print i
        try:
            if exclude and i.find(exclude) != -1:
                continue
            else:
                os.remove(i)
        except:
            pass


class ThumbnailTask():
    def __init__(self):
        self.logger_object = None
        self.create_date = datetime.now()
        self.log_level = 'warn'
        self.log_console_show_flag = 1

        self.cmd_video_duration_fmt = ''
        self.cmd_tn_video_fmt = ''
        self.cmd_tn_pdf_fmt = ''
        self.cmd_tn_image_size_fmt = ''
        self.cmd_tn_image_backcolor_fmt = ''
        self.cmd_color_threshold_fmt = ''

        self.color_threshold = 120
        self.try_times = 10
        self.poster_ext = '.png'

    def __init_logger(self, log_file_path):
        logger = logging.getLogger()
        logger.setLevel(task.LOG_LEVEL_DICT[self.log_level])
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        file_log_handle = logging.FileHandler(log_file_path)
        file_log_handle.setFormatter(formatter)
        file_log_handle.setLevel(task.LOG_LEVEL_DICT[self.log_level])
        logger.addHandler(file_log_handle)

        if self.log_console_show_flag:
            console_log_handle = logging.StreamHandler()
            console_log_handle.setFormatter(formatter)
            console_log_handle.setLevel(task.LOG_LEVEL_DICT[self.log_level])
            logger.addHandler(console_log_handle)

        self.logger_object = logger

    def init(self, config_file, param_dict):
        global file_charset, process_path
        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        log_file_path = config.get('thumbnail', 'log_file_path')
        self.log_level = config.get('thumbnail', 'log_level')
        self.log_console_show_flag = config.getint('thumbnail', 'log_console_show_flag')

        self.cmd_video_duration_fmt = config.get('thumbnail', 'cmd_video_duration_fmt')
        self.cmd_color_threshold_fmt = config.get('thumbnail', 'cmd_color_threshold_fmt')
        self.cmd_tn_video_fmt = config.get('thumbnail', 'cmd_tn_video_fmt')
        self.cmd_tn_pdf_fmt = config.get('thumbnail', 'cmd_tn_pdf_fmt')
        self.cmd_tn_image_size_fmt = config.get('thumbnail', 'cmd_tn_image_size_fmt')
        self.cmd_tn_image_backcolor_fmt = config.get('thumbnail', 'cmd_tn_image_backcolor_fmt')

        self.try_times = config.getint('thumbnail', 'try_times')
        self.color_threshold = config.getint('thumbnail', 'color_threshold')

        if config.has_option('thumbnail', 'poster_ext'):
            self.poster_ext = config.get('thumbnail', 'poster_ext')

        if 'force' not in param_dict.keys():
            param_dict['force'] = config.get('thumbnail', 'force')

        task.file_charset = config.get('config', 'file_charset')

        self.__init_logger(log_file_path)
        return True

    def get_video_duration(self, input_filepath):
        duration = 0
        cmd = self.cmd_video_duration_fmt % addslashes(input_filepath)
        # self.logger_object.info('get duration cmd (%s)' % cmd.decode('utf8'))
        try:
            p = subprocess.Popen(task.utf8_to_file_charset(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = p.stdout.readlines()
            if not lines:
                return 0
            out = lines[0]
            retval = p.wait()
            if retval:
                return duration
            # 00:05:52.60
            # dlist = re.split(':|.', out)
            dlist = out.split(':')
            duration = int(dlist[0]) * 3600 + int(dlist[1]) * 60 + int(dlist[2].split('.')[0])
            self.logger_object.info('get duration (%d)' % duration)
        except:
            self.logger_object.exception('get duration (%s) failed', cmd.decode('utf8'))
        return duration

    def get_image_color(self, input_filepath):
        """通过样本方差，检测颜色的丰富程度"""
        color_threshold = 0
        cmd = self.cmd_color_threshold_fmt % addslashes(input_filepath)
        self.logger_object.info('cmd (%s)' % cmd.decode('utf8'))
        try:
            p = subprocess.Popen(task.utf8_to_file_charset(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.stdout.readlines()[0]
            # print out
            retval = p.wait()
            if retval:
                return color_threshold
            color_threshold = int(float(out))
        except:
            self.logger_object.exception('check_image_color (%s) failed', cmd.decode('utf8'))
        return color_threshold

    def make_one_video_thumbnail(self, pos, video_path, tn_video_image_path):

        cmd = self.cmd_tn_video_fmt % (pos, addslashes(video_path), addslashes(tn_video_image_path))
        self.logger_object.info('cmd (%s)' % cmd.decode('utf8'))

        try:
            p = subprocess.Popen(task.utf8_to_file_charset(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            if task.check_file_exist(tn_video_image_path):
                return True
            else:
                return False
        except:
            self.logger_object.exception('(%s) failed', cmd.decode('utf8'))
        return False

    def make_video_thumbnail(self, video_path, tn_video_image_path, stime=0, etime=0):
        max_color = 0
        max_color_position = 0

        # 多次尝试，有可能源文件被删除了, 优先采用原清
        fix_video_path = ''
        if task.check_file_exist(video_path + "_yq.mp4"):
            fix_video_path = video_path + "_yq.mp4"
        elif task.check_file_exist(video_path + "_cq.mp4"):
            fix_video_path = video_path + "_cq.mp4"
        elif task.check_file_exist(video_path):
            fix_video_path = video_path
        else:
            self.logger_object.info('video_path not exist (%s) ' % video_path.decode('utf8'))
            return False
        duration = self.get_video_duration(fix_video_path)
        print  (fix_video_path)
        if duration == 0:
            return False
        if etime > 0:
            duration = min(etime, duration)
        for i in range(1, self.try_times):
            pos = random.randint(stime, duration)
            if self.make_one_video_thumbnail(pos, fix_video_path, tn_video_image_path):
                color = self.get_image_color(tn_video_image_path)
                if color >= self.color_threshold:
                    return True
                else:
                    if color > max_color:
                        max_color_position = pos
                        max_color = color
        # 挑一张最好的
        return self.make_one_video_thumbnail(max_color_position, fix_video_path, tn_video_image_path)

    def auto_crop(self, output_path):
        try:
            im = Image.open(task.utf8_to_file_charset(output_path))
            if im.mode != 'RGB':
                im = im.convert("RGB")

            cropped = autoCrop(im)
            cropped.save(task.utf8_to_file_charset(output_path), 'JPEG', quality=100)
        except:
            self.logger_object.exception('auto crop (%s) failed', output_path.decode('utf8'))

    def make_pdf_thumbnail(self, input_path, output_path):
        cmd = self.cmd_tn_pdf_fmt % (addslashes(output_path), addslashes(input_path))
        self.logger_object.info('cmd (%s)' % cmd.decode('utf8'))
        ret = False
        try:
            p = subprocess.Popen(task.utf8_to_file_charset(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            if task.check_file_exist(output_path):
                ret = True
            else:
                ret = False
        except:
            self.logger_object.exception('make pdf thumbnail (%s) failed', cmd.decode('utf8'))
        if ret:
            self.auto_crop(output_path)
        return ret

    def make_image_size_thumbnail(self, input_filepath, output_filepath, size, mode):
        size_xy = size.split('x')
        if mode == 'resize':
            im = Image.open(task.utf8_to_file_charset(input_filepath))
            if im.mode != 'RGB':
                im = im.convert("RGB")

            nim = im.resize((int(size_xy[0]), int(size_xy[1])), Image.BILINEAR)
            nim.save(task.utf8_to_file_charset(output_filepath), 'JPEG', quality=100)
        elif mode == 'ratio':
            resize_ratio_img(task.utf8_to_file_charset(input_filepath), task.utf8_to_file_charset(output_filepath),
                             int(size_xy[0]), int(size_xy[1]), 75)
        elif mode == 'pad':
            im = Image.open(task.utf8_to_file_charset(input_filepath))
            if im.mode != 'RGB':
                im = im.convert("RGB")

            size = (int(size_xy[0]), int(size_xy[1]))
            im.thumbnail(size, Image.ANTIALIAS)  # generating the thumbnail from given size

            offset_x = max((size[0] - im.size[0]) / 2, 0)
            offset_y = max((size[1] - im.size[1]) / 2, 0)
            offset_tuple = (offset_x, offset_y)  # pack x and y into a tuple

            final_thumb = Image.new(mode='RGB', size=size, color=(0, 0, 0))  # create the image object to be the final product
            final_thumb.paste(im, offset_tuple)  # paste the thumbnail into the full sized image
            final_thumb.save(task.utf8_to_file_charset(output_filepath), 'JPEG', quality=100)

        elif mode == 'crop':
            im = Image.open(task.utf8_to_file_charset(input_filepath))
            if im.mode != 'RGB':
                im = im.convert("RGB")

            nim = ImageOps.fit(im, (int(size_xy[0]), int(size_xy[1])), Image.ANTIALIAS)
            nim.save(task.utf8_to_file_charset(output_filepath), 'JPEG', quality=100)
        else:
            return False
        if task.check_file_exist(output_filepath):
            return True

        return False

    def make_image_backcolor_thumbnail(self, input_filepath, output_filepath, backcolor):
        cmd = self.cmd_tn_image_backcolor_fmt % (backcolor, addslashes(input_filepath), addslashes(output_filepath))

        self.logger_object.info('cmd (%s)' % cmd.decode('utf8'))

        try:
            p = subprocess.Popen(task.utf8_to_file_charset(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            if task.check_file_exist(output_filepath):
                return True
            else:
                return False
        except:
            self.logger_object.exception('(%s) failed', cmd.decode('utf8'))
        return False

    def make_thumbnail(self, param_dict):
        """video- thumbnail-size-color"""

        mediaformat = param_dict['mediaformat']
        # 检测图片是否存在 1 video 2 image
        # thumbnail

        # 随着裁剪会发生改变

        # 0x0表示原始图像
        # 不同尺寸的海报都基于此生成
        # 命名规则 orgfilename lb _poster|tposter time size backcoror ext

        if (mediaformat == task.URL_TYPE_VIDEO) and ('time' in param_dict) and (param_dict['time'] not in ['0-0', '0']):
            stime, etime = param_dict['time'].split('-')
            name_lb = "_lb"
            name_time = "_" + param_dict['time']
        else:
            name_lb = ''
            name_time = ''
            stime = 0
            etime = 0

        crop_base_poster_path = "%s%s_poster%s%s" % (param_dict['input'], name_lb, name_time, self.poster_ext)
        # print '海报：%s' % (crop_base_poster_path)
        self.logger_object.info('海报：%s' % (crop_base_poster_path))
        if mediaformat != task.URL_TYPE_IMAGE:
            # 未裁剪的海报
            poster_path = "%s%s_tposter%s_0x0_0.png" % (param_dict['input'], name_lb, name_time)
            if param_dict['force'] == 1 or (not os.path.exists(task.utf8_to_file_charset(poster_path))):
                if mediaformat == task.URL_TYPE_DOCUMENT:
                    ext = os.path.splitext(param_dict['input'])[1][1:].lower()
                    if ext == 'pdf' and os.path.exists(task.utf8_to_file_charset(param_dict['input'])):
                        pdf_file = param_dict['input']
                    elif os.path.exists(task.utf8_to_file_charset(param_dict['input'] + "_text.pdf")):
                        pdf_file = param_dict['input'] + "_text.pdf"

                    else:
                        print "format not support"
                        return False
                    if not self.make_pdf_thumbnail(pdf_file, poster_path):
                        print "make pdf thumbnail failed"
                        return False
                elif mediaformat == task.URL_TYPE_VIDEO:
                    # print 'poster_path：%s' % (poster_path)
                    self.logger_object.info('poster_path：%s' % (poster_path))
                    if not self.make_video_thumbnail(param_dict['input'], poster_path, int(stime), int(etime)):
                        return False
                # todo 三分频课件，从目录中找到视频文件
                elif mediaformat == task.URL_TYPE_ONLINE_COURSE:
                    return False
                else:  # unsupport format
                    return False

                shutil.copyfile(task.utf8_to_file_charset(poster_path), task.utf8_to_file_charset(crop_base_poster_path))
                poster_dir, file_name = os.path.split(param_dict['input'])
                remove_files(task.utf8_to_file_charset(poster_dir),
                             task.utf8_to_file_charset("%s%s_tposter%s*%s" % (file_name, name_lb, name_time, self.poster_ext)),
                             False,
                             "%s%s_tposter%s_0x0_0.png" % (file_name, name_lb, name_time))

        else:
            # 图像文件，未裁剪海报就是他本身
            poster_path = param_dict['input']

        if param_dict['end'] not in ['0x0', '0']:
            start = param_dict['start'].split('x')
            end = param_dict['end'].split('x')
            im = Image.open(task.utf8_to_file_charset(poster_path))
            if im.mode != 'RGB':
                im = im.convert("RGB")
            nim = im.crop((int(start[0]), int(start[1]), int(end[0]), int(end[1])))
            nim.save(task.utf8_to_file_charset(crop_base_poster_path), 'JPEG', quality=100)
            #     批量移除生成的其他缩略图
            poster_dir, file_name = os.path.split(param_dict['input'])
            remove_files(task.utf8_to_file_charset(poster_dir),
                         task.utf8_to_file_charset("%s%s_tposter%s*%s" % (file_name, name_lb, name_time, self.poster_ext)),
                         False,
                         "%s%s_tposter%s_0x0_0.png" % (file_name, name_lb, name_time))
        # 为了兼容性考虑，如果之前生成了.png格式，则还是采用png
        if not os.path.exists(task.utf8_to_file_charset(crop_base_poster_path)):
            if mediaformat == task.URL_TYPE_IMAGE:
                crop_base_poster_path = param_dict['input']
            else:
                crop_base_poster_path = "%s%s_poster%s.png" % (param_dict['input'], name_lb, name_time)

        # size
        if param_dict['size'] in ['0x0', '0']:
            tn_size_image_path = crop_base_poster_path
        else:
            tn_size_image_path = "%s%s_tposter%s_%s_0%s" % (param_dict['input'], name_lb, name_time, param_dict['size'], self.poster_ext)
            if (param_dict['force'] == 1 or
                    not task.check_file_exist(tn_size_image_path)):
                if not self.make_image_size_thumbnail(crop_base_poster_path, tn_size_image_path, param_dict['size'],
                                                      param_dict['mode']):
                    return False

        # unsupport todo 通过pil 而不是 vignette2来生成背景色
        # if param_dict['backcolor'] != '0':
        #     if param_dict['tnfmt'] == 1:
        #         tn_backcolor_image_path = "%s%s_tposter%s_%s_%s%s" % (
        #             param_dict['input'], name_lb, name_time, param_dict['size'], param_dict['backcolor'], self.poster_ext)
        #     if (param_dict['force'] == 1 or
        #             not task.check_file_exist(tn_backcolor_image_path)):
        #         if not self.make_image_backcolor_thumbnail(tn_size_image_path, tn_backcolor_image_path, param_dict['backcolor']):
        #             return False
        return True

def functhumb(input_filepath='', output_filepath=''):
    global process_path

    sysstr = platform.system()
    if (sysstr == "Windows"):
        config_file = "task.ini"
    else:
        config_file = "linux_task.ini"


    param_dict = {'backcolor': '0', 'size': '180x135', 'tnfmt': 1, 'mode': 'crop', 'end': '0x0', 'mediaformat': task.URL_TYPE_UNKNOW}

    if input_filepath:
        param_dict['input'] = input_filepath
    if output_filepath:
        param_dict['output'] = output_filepath
    # adjust param
    if param_dict['mode'] == '1':
        param_dict['mode'] = 'crop'
    elif param_dict['mode'] == '2':
        param_dict['mode'] = 'pad'
    elif param_dict['mode'] == '3':
        param_dict['mode'] = 'resize'
    elif param_dict['mode'] == '4':
        param_dict['mode'] = 'ratio'  # 等比例缩放

    param_dict['tnfmt'] = int(param_dict['tnfmt'])

    if 'force' in param_dict:
        param_dict['force'] = int(param_dict['force'])

    # print param_dict
    if not param_dict['input']:
        return -1

    my_task = ThumbnailTask()
    if not my_task.init(config_file, param_dict):
        return -2

    # param_dict['input'] = task.file_charset_to_utf8(param_dict['input'])
    # param_dict['output'] = task.file_charset_to_utf8(param_dict['output'])

    param_dict['mediaformat'] = task.get_media_format_import(param_dict['input'])
    if param_dict['mediaformat'] not in [task.URL_TYPE_VIDEO, task.URL_TYPE_ISO, task.URL_TYPE_DOCUMENT, task.URL_TYPE_IMAGE]:
        my_task.logger_object.info('meidaformat not support %d' % (param_dict['mediaformat']))
        return -3
    try:
        ret = my_task.make_thumbnail(param_dict)
        if ret:
            my_task.logger_object.info(
                    'make_thumbnail success -i %s -o %s ' % (param_dict['input'], param_dict['output']))
            return 1
    except:
        my_task.logger_object.exception(
                'make_thumbnail failed -i %s -o %s ' % (param_dict['input'], param_dict['output']))
        return -4
    return 0

def main(input_filepath='', output_filepath=''):
    global process_path


    sysstr = platform.system()
    if (sysstr == "Windows"):
        config_file = "task.ini"
    else:
        config_file = "linux_task.ini"

    param_dict = {'backcolor': '0', 'size': '0', 'tnfmt': 1, 'mode': 'crop', 'end': '0x0', 'mediaformat': task.URL_TYPE_UNKNOW}
    query = ''
    process_path = os.path.dirname(sys.argv[0])
    if not process_path:
        process_path = os.getcwd()
    os.chdir(process_path)

    print 'start thumbnail task...'
    if not input_filepath:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "f:i:o:s:b:F:t:m:q:", ["file=", "input=", "output=", "size=", "backcolor=",
                                                                            "force=", "tnfmt=", "mode=", "query="])

        except getopt.GetoptError, err:
            # print help information and exit:
            print err
            return -1
        for o, a in opts:
            if o in ("-f", "--file"):
                config_file = a
            elif o in ("-i", "--input"):
                param_dict['input'] = a
            elif o in ("-o", "--output"):
                param_dict['output'] = a
            elif o in ("-s", "--size"):
                param_dict['size'] = a
            elif o in ("-t", "--tnfmt"):
                param_dict['tnfmt'] = a
            elif o in ("-m", "--mode"):
                param_dict['mode'] = a
            elif o in ("-b", "--backcolor"):
                param_dict['backcolor'] = a
            elif o in ("-F", "--force"):
                param_dict['force'] = a
            elif o in ("-q", "--query"):
                query = a

    if input_filepath:
        param_dict['input'] = input_filepath
    if output_filepath:
        param_dict['output'] = output_filepath

    if query:
        query_dict = urlparse.parse_qsl(query)
        param_dict.update(query_dict)
    # adjust param
    if param_dict['mode'] == '1':
        param_dict['mode'] = 'crop'
    elif param_dict['mode'] == '2':
        param_dict['mode'] = 'pad'
    elif param_dict['mode'] == '3':
        param_dict['mode'] = 'resize'
    elif param_dict['mode'] == '4':
        param_dict['mode'] = 'ratio'  # 等比例缩放

    param_dict['tnfmt'] = int(param_dict['tnfmt'])

    if 'force' in param_dict:
        param_dict['force'] = int(param_dict['force'])

    # print param_dict
    if not param_dict['input']:
        return -1

    my_task = ThumbnailTask()
    if not my_task.init(config_file, param_dict):
        print 'init failed!\n'
        return -1
    else:
        print 'init success!\n'

    param_dict['input'] = task.file_charset_to_utf8(param_dict['input'])
    param_dict['output'] = task.file_charset_to_utf8(param_dict['output'])

    param_dict['mediaformat'] = task.get_media_format_import(param_dict['input'])
    if param_dict['mediaformat'] not in [task.URL_TYPE_VIDEO, task.URL_TYPE_ISO, task.URL_TYPE_DOCUMENT, task.URL_TYPE_IMAGE]:
        my_task.logger_object.info('meidaformat not support %d' % (param_dict['mediaformat']))
        return -1

    try:
        ret = my_task.make_thumbnail(param_dict)
        if ret:
            my_task.logger_object.info(
                'make_thumbnail success -i %s -o %s ' % (param_dict['input'].decode('utf8'), param_dict['output'].decode('utf8')))
            return 0
    except:
        my_task.logger_object.exception(
            'make_thumbnail failed -i %s -o %s ' % (param_dict['input'].decode('utf8'), param_dict['output'].decode('utf8')))
    return -1


def test_pdf():
    rate = 40
    img = Image.open(r"e:\gitroot\build\QuickCoder\test_media\pdf\1.pdf")
    img.thumbnail((img.size[0] * rate / 100,
                   img.size[1] * rate / 100)
                  )
    img.save(r"e:\gitroot\build\QuickCoder\test_media\pdf\1.jpg", 'JPEG', quality=100)


# test python guanfu_thumbnail.py -i f:/MVI_0833.MOV -q size=222x310&backcolor=0&mode=1&tnfmt=1&force=0&magic=08c7290a&time=1-20
if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
    # test_pdf()
