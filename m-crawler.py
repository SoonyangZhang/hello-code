import requests
import random
import io
'''
https://blog.csdn.net/guanmaoning/article/details/80158554
'''
#https://blog.csdn.net/flyailin/article/details/124782824
def remove_annotation(code):
    ret=''
    length=len(code)
    i=0
    flag=0
    while i<length:
        next=''
        if i<length-1:
            next=code[i+1]
        if flag==0 and code [i]=='/' and next=='/':
            break
        elif flag==0 and code[i]=='/' and next=='*':
            flag=1
            i=i+1
        elif flag==1 and code[i]=='*' and next=='/':
            flag=0;
            i=i+1
        elif flag==1:
            i=i+1
            continue
        else:
            ret=ret+code[i]
        i=i+1
    return ret
def string_contains(text,token):
    ret=False
    for i in range(len(text)):
        if token==text[i]:
            ret=True
            break
    return ret
def strip_token(code,token_list):
    ret=''
    for i in range(len(code)):
        if string_contains(token_list,code[i]) is False:
            ret=ret+code[i]
    return ret
def parser_qt(text):
    f= io.StringIO(text)
    content=[]
    locate_caigou8=False
    while True:
        line=f.readline()
        if not line:
            break
        else:
            if locate_caigou8 is False and "0!caigou8" in line:
                locate_caigou8=True
            if locate_caigou8:
                if "success" in line:
                    break
                t=line.strip()
                t=remove_annotation(t)
                if len(t)>0:
                    content.append(t)
    i=2
    length=len(content)
    qt=strip_token(content[2],"'+")+strip_token(content[3],"'+")
    return qt


if __name__=='__main__':
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    ua_list = [
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
        ]
    user_Agent=random.choice(ua_list)
    headers = {
        "Referer":None,
        "User-Agent":user_Agent,
        'Connection': 'keep-alive',
    }
    login_url="https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
    session=requests.session()
    ret = session.get(url=login_url,headers=headers)
    cookies = ret.cookies.items()
    Cookie=''
    for name,value in cookies:
        Cookie += '{0}={1};'.format(name, value)
    referer=login_url
    url="https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2"
    host="b2b.10086.cn"
    origin='https://b2b.10086.cn'
    headers = {
    'User-agent':user_Agent,
    "cookie": Cookie,
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host':host,
    'Referer':referer,
    'Origin':origin
    }
    qt=parser_qt(ret.text)
    print(qt)
    pageIndex=1
    province='YN'
    #https://zhuanlan.zhihu.com/p/31856224
    provinceCN='云南'.encode('utf-8')
    formData={
        'page.currentPage':pageIndex,
        'page.perPageSize':20,
        'noticeBean.sourceCH':provinceCN,
        'noticeBean.source':province,
        'noticeBean.title':'',
        'noticeBean.startDate':'',
        'noticeBean.endDate':'',
        '_qt':qt
    }
    resp= session.post(url=url,headers=headers,data=formData)
    session.close()
    with open(file="main-page.txt",mode="w") as f:
        f.write(ret.text)
    print(ret.status_code,"done")
    with open(file="yun-page.txt",mode="w") as f:
        f.write(resp.text)
    print(resp.status_code,"done")
