
# -*- coding:utf-8 -*-

import requests
from time import sleep
from bs4 import BeautifulSoup
from django.http import HttpResponse
from report.models import Report,Report_detail
import tushare as ts

def hello(request,*args):
    if args:
        return HttpResponse("Hello " + args[0])
    return HttpResponse("Hello Lenovo")

def tongji(request):     # parse the title and store in a detail table
    things=Report.objects.all()
    for i in things:
        try:
            para = i.title.split("-")
            # print para
            facility, title, date = para[0],para[3],para[4]
            Report_detail.objects.create(code=i.code,urls=i.urls,facility=facility,title=title,date=date)
        except:
            print "=================="
            pass
    return HttpResponse("ok")

def test(request):
    html = ""
    result = Report_detail.objects.filter(code='600519')
    for i in result:
        html=html +'<br>'+i.code+i.urls+i.facility+i.title+i.date
    return HttpResponse(html)

def create(request):     #check the first X most reported stock
    codes = ts.get_stock_basics()

    code_to_number = {}
    for i in codes.index:
        code_to_number[i]=Report_detail.objects.filter(code=i).count()
    sorted_dict = sorted(code_to_number.iteritems(),key=lambda  asd:asd[1],reverse=True)
    print sorted_dict[:100]

    return HttpResponse("ok")

def pachong(request):


    codes = ts.get_stock_basics()

    # code_list = ['300078', '300070', '600104', '603108', '603588', '300068', '002322', '601668', '300119', '601689', '002078', '002074', '600487', '600138', '601336', '002672', '600009', '600309', '300124', '000333', '002304', '300136', '601311', '002456', '600816', '300144', '300145', '002206', '601933', '000910', '000596', '002739', '000776', '000002', '601021', '002508', '600779', '600519', '600054', '601012', '300367', '002223', '600693', '000034', '300398', '601009', '600535', '002094', '000568', '002701', '000967', '600887', '600048', '000035', '001979', '600522', '600418', '300408', '603885', '603338', '300197', '600068', '300212', '300033', '600728', '601633', '002281', '002024', '002022', '600276', '300203', '300422', '300338', '300334', '000063', '002563', '002033', '002032', '002638', '603808', '002405', '300015', '300017', '600872', '601628', '002007', '002648', '002640', '000858', '600340', '600867', '300003', '002343', '002127', '600594', '000651', '601888', '603008', '600856', '601677']
    # query_code(code_list)
    query_code(codes.index)

    return HttpResponse('ok')

def tackle_current_page(Cookies,page,code):
    url2 = "http://www.hibor.com.cn/newweb/web/search?index=0"+"&page="+str(page)
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Cookie": Cookies + "; ASPSESSIONIDAAARQTSS=GJDPOHGDDAMAANELCNLNEKGP; ASPSESSIONIDQADQRQTR=CKJHNOFDJBOPAPEMDMGFGJBN; ASPSESSIONIDAQCQRQQQ=KOFFPOGDBCKNNADGGLLFKHNK; ASPSESSIONIDQCBTSSTQ=DDEEGBHDIOFBMPBNBAAMIGPP; MBpwd=ODYxMTEwMTE%3D+; MBname=zhoumb86; MBemail=zhou16386%40163%2Ecom; CNZZDATA1752123=cnzz_eid%3D1539670584-1487850785-null%26ntime%3D1487856203; Hm_lvt_d554f0f6d738d9e505c72769d450253d=1487852926; Hm_lpvt_d554f0f6d738d9e505c72769d450253d=1487857759; c=; MBpermission=2",

               }
    request_data = {"sslm": "1", "ssfw": "ybbt", "sjfw": "6", "gjz": code, }
    res2 = requests.post(url2, data=request_data, headers=headers)
    sleep(1)
    # print res2.raw.data, res2.content,res2.encoding

    soup = BeautifulSoup(res2.content)
    table1 = soup.find("table", {"id": "table1"})
    try:
        divs = table1.find_all('div')
    except:
        return 1
    num_in_page = 0
    for i in divs:
        if 'title' in i.find('a').attrs:
            num_in_page+=1
            try:
                Report.objects.create(code=code, urls=i.find('a')['href'], title=i.find('a')['title'])
            except:
                print "----------------------======================$$$$$$$$$$$$$$$$$4"
                pass
    return num_in_page

def query_code(codes):
    url1 = 'http://www.hibor.com.cn/?action=login'
    # url2 = "http://www.hibor.com.cn/newweb/web/search?index=0"
    data = {"name": "zhoumb86", "password": "86111011"}
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               }
    res1 = requests.post(url1, data=data, headers=headers)

    sleep(1)
    Cookies = res1.headers['Set-Cookie'].split(";")[0]

    # print res1.raw.data

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Cookie": Cookies + "; ASPSESSIONIDAAARQTSS=GJDPOHGDDAMAANELCNLNEKGP; ASPSESSIONIDQADQRQTR=CKJHNOFDJBOPAPEMDMGFGJBN; ASPSESSIONIDAQCQRQQQ=KOFFPOGDBCKNNADGGLLFKHNK; ASPSESSIONIDQCBTSSTQ=DDEEGBHDIOFBMPBNBAAMIGPP; MBpwd=ODYxMTEwMTE%3D+; MBname=zhoumb86; MBemail=zhou16386%40163%2Ecom; CNZZDATA1752123=cnzz_eid%3D1539670584-1487850785-null%26ntime%3D1487856203; Hm_lvt_d554f0f6d738d9e505c72769d450253d=1487852926; Hm_lpvt_d554f0f6d738d9e505c72769d450253d=1487857759; c=; MBpermission=2",

               }

    for code in codes:
        request_data = {"sslm": "1", "ssfw": "ybbt", "sjfw": "6", "gjz": code, }
        print request_data
        page = 1
        while True:
            number_in_page = tackle_current_page(Cookies, page,code)
            if number_in_page == 30:
                page = page + 1
                tackle_current_page(Cookies, page,code)
            else:
                break

        # res2 = requests.post(url2, data=request_data, headers=headers)
        # sleep(1)
        # # print res2.raw.data, res2.content,res2.encoding
        #
        # # print(res2.content)
        # soup = BeautifulSoup(res2.content)
        # table1 = soup.find("table", {"id": "table1"})
        # divs = table1.find_all('div')
        # # print divs
        # for i in divs:
        #     if 'title' in i.find('a').attrs:
        #         try:
        #             Report.objects.create(code=code, urls=i.find('a')['href'], title=i.find('a')['title'])
        #         except:
        #             print "----------------------======================$$$$$$$$$$$$$$$$$4"
        #             pass
    return

