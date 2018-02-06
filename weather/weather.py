"""天气查看

Usage:
	weather <days> <city>

Example:
	weather 1 北京

"""
from docopt import docopt
from city import city
import json
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from pandas import DataFrame
import csv


def  cli():
	"""command-line interface"""
	arguments = docopt(__doc__)
	citys = city.get(arguments['<city>'])
	days = arguments['<days>']

	#produce url
	url = produce_url(days, citys)

	#parse url
	parse_url(url)
	

def produce_url(days,citys):
	"""produce url"""
	if days == 7:
		url = 'http://www.weather.com.cn/weather/{}.shtml'.format(citys)
	else:
		url = 'http://www.weather.com.cn/weather{}d/{}.shtml'.format(days,citys)	
	return url


def parse_url(url):
	"""parse url"""
	response = requests.get(url)
	soup = BeautifulSoup(response.content,'lxml')
	dwea = soup.select('.wea')[0]
	nwea = soup.select('.wea')[1]
	dtem = soup.select('.tem')[0]
	ntem = soup.select('.tem')[1]
	dwin = soup.select('.win > span')[0]
	nwin = soup.select('.win > span')[1]
	UVI = soup.select('.li1.hot > p')[0]
	dressing = soup.select('.li3.hot > a > p')[0]
	pollution = soup.select('.li6.hot > span')[0]

	day_wea = dwea.get_text()
	#print(day_wea)

	day_tem = dtem.get_text()
	#print(day_tem)

	day_win = dwin.get_text()
	#print(day_win)

	night_wea = nwea.get_text()
	#print(night_wea)

	night_tem = ntem.get_text()
	#print(night_tem)

	night_win = nwin.get_text()
	#print(night_win)

	day_UVI = UVI.get_text()
	#print(day_UVI)
	#print(UVI)

	day_dressing = dressing.get_text()
	#print(day_dressing)

	day_pollution = pollution.get_text()

	#to_csv(filePath,sep=",",index=True,header = True)
	
	weather = DataFrame({
		
		'项目':["日间天气","日间气温","日间风向","夜间天气","夜间气温","夜间风向","紫外线情况","穿衣情况","污染情况"],
		'数值':[day_wea,day_tem,day_win,night_wea,night_tem,night_win,day_UVI,day_dressing,day_pollution]
		})
	columns = ['项目','数值']
	weather.to_csv("E:\homework\CS\scrawl\weather\weather.csv",sep=",",index=True,header=True,columns = columns)

	#return day_wea,day_tem,day_win,night_wea,night_tem,night_win,day_UVI,day_dressing,day_pollution




if __name__ == '__main__':
	cli()
	
'''display data with table'''
pt = None  # to avoid it vanished at end of block...
with open('E:\homework\CS\scrawl\weather\weather.csv') as fd:
    rd = csv.reader(fd, delimiter = ',')
    pt = PrettyTable(next(rd))
    for row in rd:
        pt.add_row(row)
print(pt)
