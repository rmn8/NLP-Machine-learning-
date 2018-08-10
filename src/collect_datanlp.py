import bs4
import requests
from bs4 import BeautifulSoup as sp
import pandas as pd
import json




n=1


def web_crawl(url,dat):
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
	try:
		url_cont = requests.get(url,headers=headers,timeout=5)
		pg_soup=sp(url_cont.content,"html.parser")
	except requests.ConnectionError as e:
    		print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
    		print(str(e))
		return dat
	except requests.Timeout as e:
    		print("OOPS!! Timeout Error")
    		print(str(e))
		return dat
	except requests.RequestException as e:
    		print("OOPS!! General Error")
    		print(str(e))
		return dat
	except KeyboardInterrupt:
    		print("Someone closed the program")
		return dat
	try:
		pgno=pg_soup.find("span",{"pageInfo"}).text.split()
	except AttributeError :
		return dat
	a1=int(pgno[1])+1
	a2=int(pgno[3])
	
	p=pg_soup.findAll("div",{"class":"row review_table_row"})
	
	
	for x in p:
		review=x.find("div",{"class":"user_review"}).text
		emo=len(x.findAll("span",{"class":"glyphicon glyphicon-star"}))
		if emo==3:
			continue
		dat.append([review,emo])
	print(len(dat))
	ind=url.find('/?')
	url2=url[:ind]+"/?page="+str(a1)+"&type=user"
	print(url2)
	if(int(a1)<int(a2)):
		web_crawl(url2,dat)
	else:
		return dat


movie=['the_wizard_of_oz_1939','mad_max_fury_road','moonlight_2016','spotlight_2015','wonder_woman_2017','ghost_in_the_shell_2017','monster_trucks_2017','wonder_wheel','a_bad_moms_christmas','king_arthur_legend_of_the_sword']

dat=[]
for i in movie:
	url="https://www.rottentomatoes.com/m/"+str(i)+"/reviews/?type=user"	
	web_crawl(url,dat)
dat_frame=pd.DataFrame(dat,columns=['text','review'])
dat_frame.to_csv("../data/review_set.csv",index=False,encoding='utf-8')

