import codecs
import json

class JsonWithEncoding(object):

    def __init__(self):
        #使用codecs模块的打开方式，可以指定编码打开，避免很多编码问题
        self.file = codecs.open("test.json","w",encoding="utf-8")

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        #注意别忘返回Item给下一个管道
        return item

    def spider_closed(self,spider):
        self.file.close()