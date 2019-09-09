# NishikoriBoardData
This script gathers comment data of Kei Nishikori comment board and formats it as match data and outputs it as csv file.

錦織実況掲示板　Nishikori comment board
https://jbbs.shitaraba.net/sports/34934/

# Collected data
Collected Data is saved in csv format.

Year2016-2019
https://github.com/taikoma/NishikoriBoardData/tree/master/data


# Match Data
The csv file contains the following data.

Point by point data.
- Serve direction.
- Ace or DoubleFault
- 1stServe or 2ndServe
- Server
- ServeSpeed
- Won or Lost
- Score
- Side

The Picture below is a screenshot of the csv file.
![default](https://user-images.githubusercontent.com/7829080/51440449-8634da80-1d0a-11e9-9282-b557f68e97af.jpg)

# Requirement
- python3
- urllib2
- re
- unicodedata
- pandas 
- BeautifulSoup
- selenium
- lxml.html
- time
- json

# Usage
1. Clone this repository or download ScrapeNishikori.py to your working directory.

2. Before executing the ScrapeNishikori.py, open the init.json file and edit url,outputfile, and unit km or mile.
 if you input "km" in unit, The data of serve speed is multiplied by 1.6.

```
{
	"url":"https://jbbs.shitaraba.net/bbs/read.cgi/sports/34934/1521822616/",
	"outputfile":"20180324_Miami.csv",
	"unit":"km"
	}
```



3. Execute the script file
```terminal
python ScrapeNishikori.py
```
