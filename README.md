# crawler
a simple crawler and its target is [here](https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2)  
## Get python3 to run this preject.    
## Dependcy
install depended python modules:  
```  
sudo su  
pip3 install beautifulsoup4  
pip3 install lxml  
```  
## Run tips 
- download notice info  
download page 1 to page 29:  
```  
python index_main.py --range=1:10  
python index_main.py --range=10:30  
```  
If any failure encouted, run it again.  
- download content page  
```  
python page-main.py  
```  
- get results  
```  
python get_csv.py  
```   
The result can be found in result.csv and the separator in csv is |   
To open result.csv in excel, set List separator as |  
To set List separator, [here](http://www.ujiaoshou.com/xtjc/17519675.html) is the guidance.  
With the help of excel, you could save result.csv in xlsx format.  

