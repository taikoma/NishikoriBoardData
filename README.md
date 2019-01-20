# NishikoriBoardData
This script gathers comment data of Kei Nishikori comment board and formats it as match data and outputs it as csv file.

錦織実況掲示板　Nishikori comment board
https://jbbs.shitaraba.net/sports/34934/

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

# Usage
Before executing the ScrapeNishikori.py, open the file and fix the following 2

Change to the url of the bulletin board you want to obtain data
```python
url = "https://jbbs.shitaraba.net/bbs/read.cgi/sports/34934/1547509776/"
```

Change the filename of the output file
```python
df.to_csv("201901Australian.csv")
```

Execute the script file
```terminal
ScrapeNishikori.py
```
