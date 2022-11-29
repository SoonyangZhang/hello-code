import html_parser as hp
import fun_misc as fm
import os
def _write_info_csv(f,count,page_id,title,param,pro,delimiter=','):
    literal=count+delimiter+page_id+delimiter+title+delimiter
    contents=[param.no_tax,param.with_tax,param.duration,pro.proxy_company,
        pro.people,pro.telephone]
    length=len(contents)
    for i in range(length):
        text=fm.text_purge(contents[i])
        if len(text)>0:
            literal=literal+text+delimiter
        else:
            literal=literal+'no value'+delimiter
    f.write(literal+'\n')
def process_page_batch(index_list,resource_dir,csv_name,suffix=".txt"):
    csv_f=open(csv_name,"w")
    delimiter='|'
    csv_f.write("index|page_id|title|no_tax|with_tax|duration|company|people|tel|\n")
    count=1
    for i in range(len(index_list)):
        path_name=index_list[i]
        id2title=fm.extrac_id2title(path_name)
        pos2=path_name.rfind('.')
        pos1=path_name.rfind('/')
        name=path_name[pos1+1:pos2]
        chilld_folder=resource_dir+name+'/'
        for item in id2title.items():
            id=item[0]
            title=item[1]
            page_name=chilld_folder+id+suffix
            param=hp.Parameter()
            pro=hp.Profile()
            if os.path.exists(page_name):
                with open(file=page_name,mode="r") as f:
                    html_content=f.read()
                    param,pro=hp.parser_notice_content(html_content)
            _write_info_csv(csv_f,str(count),id,title,param,pro,delimiter)
            count=count+1
    csv_f.close()
if __name__=='__main__':
    info_dir="page-index/"
    resource_dir="resource/"
    index_files=fm.scan_file(info_dir)
    result_file="result.csv"
    process_page_batch(index_files,resource_dir,result_file)
    fm.UTF8_2_GBK(result_file,result_file)
