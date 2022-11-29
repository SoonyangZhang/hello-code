import logging
import argparse
import html_crawler as spider
import fun_misc as fm
## python index_main --range=20:30
if __name__=='__main__':
    level = logging.WARNING # DEBUG、INFO、WARNING、ERROR、CRITICAL
    logging.basicConfig(level=level)
    parser = argparse.ArgumentParser(description='input page range:')
    parser.add_argument('--range', type=str,default='1:10')
    args = parser.parse_args()
    pos=args.range.find(':')
    num=int(args.range[0:pos])
    start_page=num
    num=int(args.range[pos+1:])
    end_page=num
    info_dir="page-index"
    resource_dir="resource/"
    page_index_list=[]
    fm.mkdir(info_dir)
    fm.mkdir(resource_dir)
    if start_page<end_page:
        for i in range(start_page,end_page):
            if i>0:
                page_index_list.append(i)
        if len(page_index_list):
            fail_list=spider.download_page_index_batch(page_index_list,info_dir)
