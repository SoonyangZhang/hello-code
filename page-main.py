import logging
import argparse
import html_crawler as spider
import fun_misc as fm
if __name__=='__main__':
    level = logging.WARNING # DEBUG、INFO、WARNING、ERROR、CRITICAL
    logging.basicConfig(level=level)
    info_dir="page-index/"
    resource_dir="resource/"
    index_files=fm.scan_file(info_dir)
    spider.download_notice_batch(index_files,resource_dir)
    #process_page_batch(index_files,resource_dir,"result.csv")
    
