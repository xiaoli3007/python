#coding=utf-8
import xml.sax


class MovieHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.caption = ""
        self.tag = ""
        self.photoLinks = ""
        self.publishTime = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "PostItem":
            print "*****PostItem*****"
            #title = attributes["title"]
            #print "Title:", title

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "tag":
            print "tag:", self.tag
        elif self.CurrentData == "caption":
            print "caption:", self.caption
        elif self.CurrentData == "photoLinks":
            print "photoLinks:", self.photoLinks
        elif self.CurrentData == "publishTime":
            print "publishTime:", self.publishTime
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "tag":
            self.tag = content
        elif self.CurrentData == "caption":
            self.caption = content
        elif self.CurrentData == "photoLinks":
            self.photoLinks = content
        elif self.CurrentData == "publishTime":
            self.publishTime = content

if ( __name__ == "__main__"):

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler( Handler )

    # file_xml = open('photo.xml',"r").read()
    # file_xml = unicode(file_xml, encoding='gbk').encode('utf8')

    parser.parse("photo.xml")
    #parser.parse(file_xml)