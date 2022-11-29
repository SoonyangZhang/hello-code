# -*- coding: utf-8 -*- 
import requests
import random
import io,os,time
import logging
import html_parser as hp
import fun_misc as fm
'''
https://blog.csdn.net/guanmaoning/article/details/80158554
'''
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
#https://blog.csdn.net/flyailin/article/details/124782824
def _remove_annotation(code):
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
            flag=0
            i=i+1
        elif flag==1:
            i=i+1
            continue
        else:
            ret=ret+code[i]
        i=i+1
    return ret
def _string_contains(text,token):
    ret=False
    for i in range(len(text)):
        if token==text[i]:
            ret=True
            break
    return ret
def _strip_token(code,token_list):
    ret=''
    for i in range(len(code)):
        if _string_contains(token_list,code[i]) is False:
            ret=ret+code[i]
    return ret
def _parser_qt(text):
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
                t=_remove_annotation(t)
                if len(t)>0:
                    content.append(t)
    length=len(content)
    qt=_strip_token(content[2],"'+")+_strip_token(content[3],"'+")
    return qt
def login(session,login_url,login_headers):
    cookie=''
    qt=''
    ret = session.get(url=login_url,headers=login_headers)
    status_code=ret.status_code
    if status_code==200:
        items = ret.cookies.items()
        info=''
        for name,value in items:
            info+= '{0}={1};'.format(name, value)
        cookie=info
        qt=_parser_qt(ret.text)
    return cookie,qt
def post_emit(session,post_url,post_headers,form_data,retry=1):
    html_content=None
    i=0
    while True:
        resp= session.post(url=post_url,headers=post_headers,data=form_data)
        '''
        if 'Content-Length' in resp.request.headers:
            logging.info(resp.request.headers['Content-Length'])
        '''
        if resp.status_code==200:
            html_content=resp.text
            break
        i=i+1
        if i>=retry:
            break
        else:
            time.sleep(1)# try again
    return html_content
def save_notice_page(pathname,html_content):
    title2id=hp.get_onclick_info(html_content)
    fm.save_title2id(title2id,pathname)
login_url="https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
referer=login_url
post_url="https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2"
host="b2b.10086.cn"
origin='https://b2b.10086.cn'
url_base="https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="
login_headers = {
    "Referer":'',
    "User-Agent":'',
    'Connection': 'keep-alive',
}
post_headers ={
'User-agent':'',
'cookie': '',
'Connection': 'keep-alive',
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':host,
'Referer':referer,
'Origin':origin,
'X-Requested-With':'XMLHttpRequest'
}

def request_page_index(session,cookie,qt,post_headers,page_index,retry=1,info_dir=None):
    success=False
    per_page_size=20
    province='YN'
    #https://zhuanlan.zhihu.com/p/31856224
    province_ch='云南'
    form_data={
        'page.currentPage':str(page_index),
        'page.perPageSize':str(per_page_size),
        'noticeBean.sourceCH':province_ch,
        'noticeBean.source':province,
        'noticeBean.title':'',
        'noticeBean.startDate':'',
        'noticeBean.endDate':'',
        '_qt':qt
    }
    post_headers['cookie']=cookie
    #https://blog.csdn.net/weixin_51111267/article/details/124616848
    post_content=post_emit(session,post_url,post_headers,form_data,retry)
    if post_content is None:
        logging.warn("fail to download notice page {}".format(page_index))
        return success
    success=True
    if info_dir:
        pathname=info_dir+province+"_"+str(page_index)+".txt"
        save_notice_page(pathname,post_content)
    return success
def open_page(session,page_url,headers,file_name):
    success=False
    resp = session.get(url=page_url,headers=headers)
    with open(file=file_name,mode="w") as f:
        f.write(resp.text)
    if resp.status_code==200:
        success=True
    return success

def download_notice_batch(index_list,resource_dir,suffix=".txt"):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    for i in range(len(index_list)):
        user_agent=random.choice(ua_list)
        login_headers['User-Agent']=user_agent
        session=requests.session()
        path_name=index_list[i]
        id2title=fm.extrac_id2title(path_name)
        pos2=path_name.rfind('.')
        pos1=path_name.rfind('/')
        name=path_name[pos1+1:pos2]
        new_path=resource_dir+name+'/'
        fm.mkdir(new_path)
        for item in id2title.items():
            id=item[0]
            page_url=url_base+id+""
            dest_name=new_path+id+suffix
            if open_page(session,page_url,login_headers,dest_name) is False:
                logging.warn("download failure {} {}".format(name,dest_name))
        session.close()
def download_page_index_batch(page_index_list,store_dir,retry=1):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    fail_list=[]
    user_agent=random.choice(ua_list)
    login_headers['User-Agent']=user_agent
    post_headers['User-agent']=user_agent
    session=requests.session()
    cookie,qt=login(session,login_url,login_headers)
    if len(cookie)==0:
        logging.warn("oop,login failure,try agian")
        fail_list=page_index_list
        return fail_list
    for i in range(len(page_index_list)):
        page_index=page_index_list[i]
        status=request_page_index(session,cookie,qt,post_headers,page_index,retry,store_dir)
        if status is False:
            fail_list.append(page_index)
    session.close()
    return fail_list
