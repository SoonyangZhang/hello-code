from bs4 import BeautifulSoup
'''
https://blog.csdn.net/qq_16912257/article/details/53332474
https://blog.csdn.net/weixin_42970378/article/details/83108206
https://www.jb51.net/article/179145.htm
'''
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
def fun_test(html_name):
    with open(file=html_name,mode="r") as f:
        html_content=f.read()
        info=get_onclick_info(html_content)
        print(len(info))
        temp=list(info.values())
        print(temp[0])
'''
if __name__=='__main__':
    fun_test("yun-page.txt")
'''