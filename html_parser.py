from bs4 import BeautifulSoup
import re
'''
https://blog.csdn.net/qq_16912257/article/details/53332474
https://blog.csdn.net/weixin_42970378/article/details/83108206
https://www.jb51.net/article/179145.htm
'''
class Parameter:
    def __init__(self):
        self.bf_tax=''
        self.af_tax=''
        self.duration=''
    def __str__(self):
        return self.bf_tax+self.af_tax+self.duration
class Profile:
    def __init__(self):
        self.proxy_company=''
        self.people=''
        self.telephone=''
    def __str__(self):
        return self.proxy_company+self.people+self.telephone
#selectResult('900026')
def _parser_id(select_result):
    ret=''
    length=len(select_result)
    i=0
    valid=False
    flag=False
    while i<length:
        next=''
        cur=select_result[i]
        if i<length-1:
            next=select_result[i+1]
        if cur=='(' and next=='\'':
            flag=True
            i=i+2
            continue
        if cur=='\'' and next==')':
            if flag:
                valid=True
            break
        if flag:
            ret=ret+cur
        i=i+1
    if valid is False:
        ret=''
    return ret
def get_onclick_info(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    tr_all=soup.find_all("tr")
    length=len(tr_all)
    dic={}
    for i in range(length):
    #{'class': [], 'onmousemove': 'cursorOver(this)', 'onmouseout': 'cursorOut(this)', 'onclick': "selectResult('901888')"}
    # type(attrs) is  dict
        if tr_all[i].attrs and 'onclick' in tr_all[i].attrs:
            id=_parser_id(tr_all[i].attrs['onclick'])
            if len(id)>0:
                ahref=tr_all[i].find("a")
                if 'title' in ahref.attrs:
                    dic.update({ahref.attrs['title']:id})
                elif len(ahref.contents)>0:
                    dic.update({ahref.contents[0]:id})
    return dic
def _get_divset_list(div_set):
    contents=[]
    for i in range(len(div_set)):
        ptag=div_set[i].find_all("p")
        for j in range(len(ptag)):
            for k in range(len(ptag[j].contents)):
                if ptag[j].contents[k].string:
                    contents.append(ptag[j].contents[k].string)
    return contents
#https://blog.csdn.net/u010687164/article/details/85320691
Regx = re.compile("(([1-9]\\d*[\\d,，]*\\.?\\d*)|(0\\.[0-9]+))(元|百万|万元|亿元|万|亿)")
RegPhone=re.compile("(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18\d{9})")
def _get_budget_text(text):
    bf_tax=''
    af_tax=''
    i=0
    length=len(text)
    pos1=text.find("不含税")
    pos2=-1
    remain=None
    if pos1>=0:
        pos2=text.find("元",pos1)
        if pos2>=0:
            bf_tax=text[pos1:pos2+1]
            remain=text[0:pos1]+text[pos2+1:length]
    pos2=-1
    text=remain
    if text and len(text)>0:
        pos1=text.find("含税")
        if pos1>=0:
            pos2=text.find("元",pos1)
            if pos2>=0:
                af_tax=text[pos1:pos2+1]
    return bf_tax,af_tax
def _parser_parameter(contents):
    param=Parameter()
    length=len(contents)
    for i in range(length):
        if "元" in contents[i]:
            bf_tax,af_tax=_get_budget_text(contents[i])
            if bf_tax and len(bf_tax)>0:
                res=Regx.search(bf_tax)
                if res:
                    param.bf_tax=res.group()
            if af_tax and len(af_tax)>0:
                res=Regx.search(af_tax)
                if res:
                    param.af_tax=res.group()
            continue
        if len(param.duration) ==0:
            text=contents[i]
            if "合同" in text:
                if "期限" in text:
                    pos=text.find("：")
                    if pos>=0:
                        param.duration=text[pos+1:]
                elif "时间" in text:
                    pos=text.find("：")
                    if pos>=0:
                        param.duration=text[pos+1:]
    return param
def _parser_profile(contents):
    pro=Profile()
    length=len(contents)
    i=0
    success=False
    while i<length:
        text=contents[i]
        if "代理" in text and "公司" in text:
            pos=text.find("：")
            pro.proxy_company=text[pos+1:]
            success=True
            break
        i=i+1
    if success:
        success=False
        while i<length:
            text=contents[i]
            if "联系人" in text or "经理" in text or "负责人" in text:
                pos=text.find("：")
                pro.people=text[pos+1:]
                success=True
                break
            i=i+1
    if success:
        while i<length:
            text=contents[i]
            res=RegPhone.search(text)
            if res:
                pro.telephone=res.group()
                break
            i=i+1
    return pro
def parser_notice_content(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    #title_div=soup.find("div", {"id":"titDiv"})
    #title_span=title_div.find("span")
    #print(title_span.contents)
    ggdiv1_set=soup.find_all("div", {"id":"ggdiv1"})
    ggdiv3_set=soup.find_all("div", {"id":"ggdiv3"})
    contents=_get_divset_list(ggdiv1_set)
    param=_parser_parameter(contents)
    contents=_get_divset_list(ggdiv3_set)
    pro=_parser_profile(contents)
    return param,pro
def fun_test():
    suffix=".txt"
    path="./resource/YN_1/"
    name="900707" #"900097"  "901715" "900933"
    path_name=path+name+suffix
    with open(file=path_name,mode="r") as f:
        html_content=f.read()
        param,pro=parser_notice_content(html_content)
        print(param)
        print(pro)
'''
if __name__=='__main__':
    fun_test()
'''