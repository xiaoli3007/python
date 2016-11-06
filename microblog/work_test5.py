# -*- coding: utf-8 -*-
'''
 百度中批量下载某歌手的歌(目前只下载第一页，可以自行拓展)
 @author:admin
 @qq: 1243385033
'''
import threading, urllib2, os, re, sys
from bs4 import BeautifulSoup
from Queue import Queue

'''目标歌手'''
SINGER = u'江美琪'
'''保存路径'''
SAVE_FOLDER = 'F:/music/'
# 查询url
search_url = "http://music.baidu.com/search/song?key=%s&s=1"
# 百度音乐播放盒url
song_url = "http://box.zhangmen.baidu.com/x?op=12&count=1&mtype=1&title="


class Downloader(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task

    def run(self):
        '''覆盖父类的run方法'''
        while True:
            url = self.task.get()
            self.download(url)
            self.task.task_done()

    def build_path(self, filename):
        join = os.path.join
        parentPath = join(SAVE_FOLDER, SINGER)
        filename = filename + '.mp3'
        myPath = join(parentPath, filename)
        return myPath

    def download(self, url):
        '''下载文件'''
        sub_url = url.items()
        f_name = sub_url[0][0]
        req_url = sub_url[0][1]
        handle = urllib2.urlopen(req_url)
        # 保存路径
        save_path = self.build_path(f_name)
        with open(save_path, "wb") as handler:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                handler.write(chunk)
                msg = u"已经从  %s下载完成" % req_url
            sys.stdout.write(msg)
            sys.stdout.flush()


class HttpRequest:
    def __init__(self):
        self.task = []
        self.reg_decode = re.compile('<decode>.*?CDATA\[(.*?)\]].*?</decode>')
        self.reg_encode = re.compile('<encode>.*?CDATA\[(.*?)\]].*?</encode>')
        self.init()
        self.target_url = search_url % urllib2.quote(self.encode2utf8(SINGER))

    def encode2utf8(self, source):
        if source and isinstance(source, (str, unicode)):
            source = source.encode("utf8")
            return source
        return source

    def mkDir(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def init(self):
        self.mkDir(SAVE_FOLDER)
        subPath = os.path.join(SAVE_FOLDER, SINGER)
        self.mkDir(subPath)

    def http_request(self):
        global song_url
        '''发起请求'''
        response = urllib2.urlopen(self.target_url)
        # 获取头信息
        content = response.read()
        response.close()
        # 使用BeautifulSoup
        html = BeautifulSoup(content, from_encoding="utf8")
        # 提取HTML标签
        span_tag = html.find_all('div', {"monkey": "song-list"})[0].find_all('span', class_='song-title')
        # 遍历List
        for a_tag in span_tag:
            song_name = unicode(a_tag.find_all("a")[0].get_text())
            song_url = song_url + urllib2.quote(self.encode2utf8(song_name))
            song_url = song_url + '$$' + urllib2.quote(self.encode2utf8(SINGER)) + '$$$$&url=&listenreelect=0&.r=0.1696378872729838'
            xmlfile = urllib2.urlopen(song_url)
            xml_content = xmlfile.read()
            xmlfile.close()
            url1 = re.findall(self.reg_encode, xml_content)
            url2 = re.findall(self.reg_decode, xml_content)
            if not url1 or not url2:
                continue
            url = url1[0][:url1[0].rindex('/') + 1] + url2[0]
            self.task.append({song_name: url})
        return self.task


def start_download(urls):
    # 创建一个队列
    quene = Queue()
    # 获取list的大小
    size = len(urls)
    # 开启线程
    for _ in xrange(size):
        t = Downloader(quene)
        t.setDaemon(True)
        t.start()
    # 入队列
    for url in urls:
        quene.put(url)

    quene.join()


if __name__ == '__main__':
    http = HttpRequest()
    urls = http.http_request()
    print(urls)
    exit()
    start_download(urls)


