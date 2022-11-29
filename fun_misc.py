# -*- coding: utf-8 -*- 
import os
import codecs
def remove_dir(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.exists(top):
        os.rmdir(top)
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:    
        os.makedirs(path)
#https://blog.csdn.net/a1579990149wqh/article/details/124953746
def delete_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            # if file_name != 'wibot.log':
            tf = os.path.join(dir_path, file_name)
            del_files(tf)
def scan_file(url):
    names=[]
    for root, dirs, files in os.walk(url):
        for name in files:
            names.append(os.path.join(root, name))
    return names
def scan_folder(url):
    names=[]
    for root, dirs, files in os.walk(url):
        for name in dirs:
            names.append(os.path.join(root, name))
    return names
def save_title2id(title2id,pathname):
    with open(file=pathname,mode="w") as f:
        for item in title2id.items():
            f.write(item[1]+","+item[0]+"\n")
def extrac_id2title(path_name):
    dic={}
    for index, line in enumerate(open(path_name,'r')):
        line_arr= line.strip().split(',')
        dic.update({line_arr[0]:line_arr[1]})
    return dic
#https://blog.csdn.net/weixin_39963132/article/details/85197894
#https://blog.csdn.net/Owen_goodman/article/details/107783304
ch_punc=["、", "，", "。"]
en_punc=[",", ",", "."]
def in_ch_punc_table(token):
    pos=-1
    for i in range(len(ch_punc)):
        if token==ch_punc[i]:
            pos=i
            break
    return pos
def text_purge(text):
    t2=''
    for i in range(len(text)):
        pos=in_ch_punc_table(text[i])
        if pos>=0:
            t2=t2+en_punc[pos]
        else:
            t2=t2+text[i]
    if len(t2)>0:
        t2 = ' '.join(t2.split())
    return t2
#https://blog.csdn.net/LLC25802580/article/details/123103423
def read_file(pathname,encoding="utf-8"):
    with codecs.open(pathname,"r",encoding) as f:
        return f.read()
def write_file(pathname,u,encoding="gbk"):
    with codecs.open(pathname,"w",encoding) as f:
        f.write(u)
def UTF8_2_GBK(src,dst,del_src=True):
    if os.path.exists(src):
        content = read_file(src,encoding="utf-8")
        if del_src:
            delete_files(src)
        write_file(dst,content,encoding="gbk")
    
