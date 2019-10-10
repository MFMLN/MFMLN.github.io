#导入request库-请求网站获取网络数据
import requests
#导入bs4库里面的BeautifulSoup类-解析数据
from bs4 import BeautifulSoup
import time
#导入echarts库制图-数据可视化
from echarts import Echart,Bar,Axis
#初始化
TEMPERATURE_LIST=[]
CITY_LIST=[]
MAX_LIST=[]



#get气温函数：从http://www.weather.com.cn/textFC/hb.shtml上爬取数据(省,市,最高温)
def get_temperature(url):
	#增加对应请求头(headers相关在网页控制台network中),模拟浏览器并发起request请求
    headers={
    	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    	'Upgrade-Insecure-Requests':'1',
   	 	'Host':'www.weather.com.cn',}
    res=requests.get(url,headers=headers)
    res.encoding=('utf-8')
    text=res.text
    soup=BeautifulSoup(text,'lxml')#请求得到的用lxml解析器解析
	#以下是对所获得的html进行清洗，结合网页控制台Elements看
    conMidtab=soup.find('div',class_='conMidtab')  #获取class=conMidtab的第一页所有div1(各区)
    conMidtab2_list=conMidtab.find_all('div',class_='conMidtab2')#find出div1里所有下一级div2(各区下各省)
    #find出每个下一级div2里从第三个开始的所有tr(各省下的各市列表)
    for x in conMidtab2_list:
        tr_list=x.find_all('tr')[2:]
        province=''
        max=''
        #for循环区别从第一个区第一个div2(即北京省)中第三个tr中各td下标和其他div2获取省,市,最高温的差异并遍历获得该区北京+其他 所有省市信息并赋值
        for index,tr in enumerate(tr_list):
            if index==0:
                td_list=tr.find_all('td')#获北京省下各市列表
                province=td_list[0].text.replace('\n','')#获取列表0为省
                city=td_list[1].text.replace('\n','')#获取列表1为市
                max=td_list[4].text.replace('\n','')#获取列表4为最高温
            else:
                td_list=tr.find_all('td')#获取其他省市各列表
                city=td_list[0].text.replace('\n','')
                max=td_list[3].text.replace('\n','')
            #(print('%s|%s'%(province+city,max)))
            TEMPERATURE_LIST.append({
                'city':province+city,
                'max':max
                })
            CITY_LIST.append(province+city)
            MAX_LIST.append(max)

#display气温函数
def display_temperature():
	#url各区为华北,东北,华东,华中,华南,西北,西南
    urls=['http://www.weather.com.cn/textFC/hb.shtml',
          'http://www.weather.com.cn/textFC/db.shtml',
          'http://www.weather.com.cn/textFC/hd.shtml',
          'http://www.weather.com.cn/textFC/hz.shtml',
          'http://www.weather.com.cn/textFC/hn.shtml',
          'http://www.weather.com.cn/textFC/xb.shtml',
          'http://www.weather.com.cn/textFC/xn.shtml']
    #循环传各区url参数并执行get气温函数
    for url in urls:
        get_temperature(url)
        time.sleep(2)#每爬一个页面停顿防止过度干扰服务器不友好
    #对执行完获得全国最高温进行排序   
    SORTED_TEMPERATURE_LIST=sorted(TEMPERATURE_LIST, key=(lambda x:(int(x['max']))),reverse=True)
    #，页面显示不了这么多，故筛选排前20的并定义新变量赋值
    TOP20_TEMPERATURE_LIST= SORTED_TEMPERATURE_LIST[0:20]
    TOP20_CITY_LIST=[]
    OP20_MAX_LIST=[]
    for city_max in TOP20_TEMPERATURE_LIST:
         TOP20_CITY_LIST.append(city_max['city'])
         TOP20_MAX_LIST.append(city_max['max'])
    #用echarts库进行可视化制图        
    echart=Echart(u'全国最高气温排名TOP1~20')
    bar=Bar(u'最高温度',TOP20_MAX_LIST)
    axis=Axis('category','left',data=TOP20_CITY_LIST)
    echart.use(bar)
    echart.use(axis)
    echart.plot()
	  # {{a=1
	  #   b=20
	  #   for i in [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7...]:
	  #       TOP20_TEMPERATURE_LIST= SORTED_TEMPERATURE_LIST[a:b]
	  #       TOP20_CITY_LIST=[]
	  #       TOP20_MAX_LIST=[]
	  #       for city_max in TOP20_TEMPERATURE_LIST:
	  #           TOP20_CITY_LIST.append(city_max['city'])
	  #           TOP20_MAX_LIST.append(city_max['max'])
	            
	  #       echart=Echart(u'全国最高气温排名TOP'+str(a)+'~'+str(b))
	  #       bar=Bar(u'最高温度',TOP20_MAX_LIST)
	  #       axis=Axis('category','left',data=TOP20_CITY_LIST)
	  #       echart.use(bar)
	  #       echart.use(axis)
	  #       echart.plot()
	  #       a+=20
	  #       b+=20    }}
   



#最终调用        
display_temperature()
















