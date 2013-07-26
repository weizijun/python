#encoding=utf-8

import sys
import urllib
import HTMLParser

class MyHTMLParser(HTMLParser.HTMLParser):
    _keyword_flag = False
    _phonetic = False
    _usa__phonetic = False
    _uk__phonetic_flag = False
    _uk__phonetic = ""
    _trans = False
    _trans_ul = False
    _trans_add = False
    _num = -1
    _line = 0
    _total_content = ""

    def handle_starttag(self, tag, attrs):
        if tag == "span" :
            for attr in attrs:
                #print attr[0]
                #设置单词
                if attr[0] == "class" and attr[1] == "keyword" :
                    self._keyword_flag = True
                #设置音标
                elif attr[0] == "class" and attr[1] == "pronounce" :
                    self._phonetic = True

        #设置解释
        if tag == "div" :
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "trans-container" :
                    self._trans = True
                    self._num = 0

        if self._num == 1 and tag == "ul":
            self._trans_ul = True

        self._num += 1

        if tag == "p" and self._trans == True:
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "additional" :
                    self._trans_add = True
    def handle_endtag(self, tag):
        if self._keyword_flag == True and tag == "span" :
            self._keyword_flag = False
        elif self._phonetic ==True and tag == "span"  :
            self._phonetic = False
            self._usa__phonetic = False
            self._uk__phonetic_flag = False
            self._uk__phonetic = ""
        elif self._trans == True and tag == "div" :
            self._trans = False
        elif self._trans_ul == True and tag == "ul" :
            self._trans_ul = False
        elif self._trans_add == True and tag == "p" :
            self._trans_add = False

    def handle_data(self, data):
        #设置单词
        if self._keyword_flag == True :
            if  data.strip() :
                self._total_content += data.strip()
                self._total_content += "\n"
                self._line += 1
            #print repr(self._line) + ":" + data.strip()

        #设置音标
        if self._uk__phonetic_flag == True :
            if  data.strip() :
                self._uk__phonetic = data.strip()

        if self._usa__phonetic == True :
            if  data.strip() :
                self._total_content += data.strip()
                self._total_content += "\n"
                self._line += 1
            elif  self._uk__phonetic :
                #美式发音不存在，则使用英式发音
                self._total_content += self._uk__phonetic
                self._total_content += "\n"
                self._line += 1
                pass

            #print repr(self._line) + ":" + data.strip()

        if self._phonetic == True :
            if data.strip() == "英" :
                self._uk__phonetic_flag = True
            elif data.strip() == "美" :
                self._usa__phonetic = True

        #设置解释
        if self._trans_ul == True :
            if  data.strip():
                self._total_content += data.strip()
                self._total_content += "\n"
                self._line += 1
            #print repr(self._line) + ":" + data.strip()
            pass

        if self._trans_add == True :
            if  data.strip():
                self._total_content += data.replace(' ', '').replace('\t', '').replace('\n', ',')
                self._total_content += "\n"
                self._line += 1
            #print repr(self._line) + ":" + data.replace(' ', '').replace('\n', '').replace('\t', '')
            pass

        pass
        #print "Data     :", data
    def handle_comment(self, data):
        pass
        #print "Comment  :", data
    def handle_entityref(self, name):
        pass
        #c = unichr(name2codepoint[name])
        #print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        #print "Num ent  :", c
    def handle_decl(self, data):
        #print "Decl     :", data
        pass
    def get_content(self) :
        return self._total_content

class ErrorHTMLParser(HTMLParser.HTMLParser):
    _div_flag  = False
    _a_flag = False
    _keyword = "";
    def handle_starttag(self, tag, attrs):
        if tag == "div" :
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "error-typo" :
                    self._div_flag = True

        if self._div_flag == True and tag == "a" :
            self._a_flag = True

    def handle_endtag(self, tag):
        if tag == "div" and self._div_flag == True :
            self._div_flag = False

        if  self._a_flag == True :
            self._a_flag = False
    def handle_data(self, data):
        if self._a_flag == True :
            print data.strip()
            self._keyword = data.strip()

    def get_keyword(self) :
        return self._keyword


#处理单词
def save_data() :
    r_file = open("right_data.txt")
    w_file = open ( 'power.txt', 'w' )
    word_file = open("word.txt",'w')
    word_arr =  r_file.readlines()

    for word in word_arr :
        print word
        try :
            content = urllib.urlopen('http://dict.youdao.com/search?q='+word).read()

            if not content :
                data = "该单词获取失败:" + word
                print data
                word_file.write(data)
                continue

            if content.find('您要找的是不是') != -1 :
                data = '您要找的是不是:' + word
                print data
                word_file.write(data)
                continue
            parser = MyHTMLParser()
            parser.feed(content)
            final_content = parser.get_content()
            final_content += "\n"
            w_file.write(final_content)
            parser.close()
        except:
            data = "获取单词异常:" + word
            print data
            word_file.write(data)

    r_file.close()
    w_file.close()
    word_file.close()

#找出错误的单词
def deal_error_word() :
    r_file = open("word.txt")
    w_file = open ( 'right_word.txt', 'w' )
    word_arr =  r_file.readlines()
    for word in word_arr :
        #print word
        content = urllib.urlopen('http://dict.youdao.com/search?q='+word).read()
        parser = ErrorHTMLParser()
        parser.feed(content)
        final_content = parser.get_keyword()
        final_content += "\n"
        w_file.write(final_content)
        parser.close()
    r_file.close()
    w_file.close()

#修复错误的单词
def correct_error_word() :
    r_word_file = open("word.txt")
    r_data_file = open("data.txt")
    r_right_word_file = open("right_word.txt")
    w_file = open("right_data.txt",'w')
    word_arr =  r_word_file.readlines()
    data_arr = r_data_file.readlines()
    right_data_arr =  r_right_word_file.readlines()

    word_len = len(word_arr)
    data_len = len(data_arr)

    word_index = 0
    data_index = 0
    content = ""
    while word_index < word_len and data_index < data_len:
        if data_arr[data_index] == word_arr[word_index] :
            content += right_data_arr[word_index]
            word_index += 1
        else :
            content += data_arr[data_index]

        data_index += 1

    w_file.write(content)

    r_right_word_file.close()
    r_word_file.close()
    r_data_file.close()
    w_file.close()

if __name__ == "__main__" :
    save_data()



