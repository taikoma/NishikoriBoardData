# coding: UTF-8
import urllib.request as urllib2
import re
import unicodedata
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import lxml.html
import time

if __name__ == "__main__":
    text = readTextFile('nick-3r.txt')
    text = preConvert(text)

    #df = pd.DataFrame({'Tournament':[],'OpponentPlayer':[],'Set':[],'TotalGame':[], 'Server':[], 'WinLose':[],'FirstSecond':[], 'Cource':[], 'Speed':[], 'AceDbF':[]})
    url = "https://jbbs.shitaraba.net/bbs/read.cgi/sports/34934/1547509776/"
    df = scrape(url)
    #df=textToDatabase("",df,text,'錦織圭vs.ニック・キリオス\n',0)

    df = scoreToDataFrame(df)
    df = df[~df.duplicated(
        subset=['OpponentPlayer', 'Set', 'TotalGame', 'ScoreServer', 'ScoreReturner'])]
    df = df.reset_index()
    df.to_csv("201901Australian.csv")
    print("end")


def createIndex(temp):  # 重複データを避けるためにインデックスを作成
    index = []
    index2 = []
    for i, r in enumerate(temp):
        temp2 = re.findall(r'G([0-9]+)([一-龥])(.*)\((.*)\)', r)
        if(temp2[0][0] not in index):
            index.append(temp2[0][0])
            index2.append(i)
        index2[index.index(temp2[0][0])] = i
    return index, index2


def devideText(text1):  # 大会の中で何試合あるかをカウントする
    opponentPlayers = list(set(re.findall('.*?vs.*?\n', text1)))
    text1 = text1.replace(" ", "")
    text1 = text1.replace("　", "")
    a = text1.split('\n\n')  # コメント毎に抽出
    b = [s for s in a if '赤黄色' in s]  # 赤黄色が含まれるコメントだけ抽出
    c = [s for s in b if 'set' in s]  # set
    d = [s for s in c if 'vs' in s]  # vs

    array = []  # 1⇒選手　2⇒set
    for k, kk in enumerate(opponentPlayers):
        array_temp = []
        for i in range(9):
            array_temp.append("")
        array.append(array_temp)
    for i, ii in enumerate(opponentPlayers):
        e = [s for s in d if ii in s]  # 相手プレイヤー毎に抽出
        match = [
            s for s in e if re.findall(
                r'set[0-9][0-9]-[0-9](\([0-9]\))?\n',
                s)]  # set2以降を抽出
        match = [s for s in e if re.findall('set([0-9])\n', s)]  # set1を抽出
        for j, jj in enumerate(match):
            f = re.findall('set([0-9])\n', jj)
            g = array[i][int(f[len(f) - 1]) - 1]  # len(f[0])
            g += jj
            array[i][int(f[len(f) - 1]) - 1] = g
    return opponentPlayers, array


def initArray():
    totalGame = []
    server = []
    winLose = []
    firstSecond = []
    cource = []
    speed = []
    ad = []
    row = []
    index = []
    index2 = []
    opponentPlayer = []
    setArray = []
    tournament = []
    return totalGame, server, winLose, firstSecond, cource, speed, ad, row, index, index2, opponentPlayer, setArray, tournament


def addRowData(
        i,
        serveText,
        op,
        s,
        dataServer,
        dataGame,
        dwl,
        dataSpeed,
        dataAD,
        tournament,
        opponentPlayer,
        setArray,
        totalGame,
        server,
        winLose,
        firstSecond,
        cource,
        speed,
        ad,
        title):
    tournament.append(title)
    temp10 = re.search('vs.(.*?)\n', op)
    opponentPlayer.append(temp10.group(1))
    setArray.append(s + 1)
    totalGame.append(dataGame)
    server.append(dataServer)

    winLose.append(dwl)

    if(len(serveText) > 0):
        if(serveText[0] == 'A'):
            firstSecond.append("1")
        elif(serveText[0] == 'D'):
            firstSecond.append("2")
        else:
            firstSecond.append(serveText[0])
    else:
        firstSecond.append("")
    if(len(serveText) > 1):
        cource.append(serveText[1])
    else:
        cource.append("")
    if(dataSpeed is not None):
        speed.append(dataSpeed.group(0))
    else:
        speed.append("")
    if(dataAD is not None):
        ad.append(dataAD.group(0))
    else:
        ad.append("")
    return tournament, opponentPlayer, setArray, totalGame, server, winLose, firstSecond, cource, speed, ad


def matchToArrayTibreak(
        pattern,
        tiebreak,
        op,
        s,
        lastGame,
        lastServer,
        anotherServer,
        title):
    serverList = [anotherServer, lastServer]
    totalGame, server, winLose, firstSecond, cource, speed, ad, row, index, index2, opponentPlayer, setArray, tournament = initArray()  # 配列を初期化
    #print(tiebreak)

    #for i,dl in enumerate(tiebreak):
    # print(tiebreak[0])#TB×○○××○○○○○(2b1102w842b901w1312w1w1181c118Dn1w1112c102)
    devided = re.findall(pattern, tiebreak[0])

    #print(devided)
    if(devided):
        serveList = re.sub(r'([0-9A-D][a-z])', r',\1', devided[0]
                           [len(devided[0]) - 1].replace(" ", ""))  # ()の中を分解する
        serveList = re.sub('^,', "", serveList)  # 先頭の,を削除
        serveList = serveList.split(",")
        dataWonLostList = devided[0][0]
        j = 1
        k = 0
        for i, dwl in enumerate(dataWonLostList):  # サーブデータを分割して1つずつ処理
            dataGame = int(lastGame) + 1
            dataServer = serverList[k]
            if(i < len(serveList)):
                t = serveList[i]
                temp7 = re.search('[0-9A-D][a-z]', t)
                dataSpeed = re.search('[0-9]{3}', t)
                dataAD = re.search('[A-Z][a-z]', t)
            else:
                t = ''
            tournament, opponentPlayer, setArray, totalGame, server, winLose, firstSecond, cource, speed, ad = addRowData(
                i, t, op, s, dataServer, dataGame, dwl, dataSpeed, dataAD, tournament, opponentPlayer, setArray, totalGame, server, winLose, firstSecond, cource, speed, ad, title)
            j += 1
            if(j == 2):
                j = 0
                k = (k + 1) % 2
    df = pd.DataFrame({'Tournament': tournament,
                       'OpponentPlayer': opponentPlayer,
                       'Set': setArray,
                       'TotalGame': totalGame,
                       'Server': server,
                       'WinLose': winLose,
                       'FirstSecond': firstSecond,
                       'Cource': cource,
                       'Speed': speed,
                       'AceDbF': ad})
    return df


def matchToArray(pattern, dataList, op, s, title):
    totalGame, server, winLose, firstSecond, cource, speed, ad, row, index, index2, opponentPlayer, setArray, tournament = initArray()  # 配列を初期化
    dataGame = ''
    dataServer = ''
    for i, dl in enumerate(dataList):
        # [('1', '霧', '××○○○○', '1w120Ac1251c1312w1042b1072w108')]
        devided = re.findall(pattern, dl)
        if(devided):
            serveList = re.sub(r'([0-9A-D][a-z])',
                               r',\1',
                               devided[0][len(devided[0]) - 1].replace(" ",
                                                                       ""))  # ()の中を分解する
            serveList = re.sub('^,', "", serveList)  # 先頭の,を削除
            serveList = serveList.split(",")
            dataGame = devided[0][0]
            dataServer = devided[0][1]
            dataWonLostList = devided[0][2]

            j = 1
            k = 0
            for i, dwl in enumerate(dataWonLostList):  # サーブデータを分割して1つずつ処理
                if(i < len(serveList)):
                    t = serveList[i]
                    temp7 = re.search('[0-9A-D][a-z]', t)
                    dataSpeed = re.search('[0-9]{3}', t)
                    dataAD = re.search('[A-Z][a-z]', t)
                else:
                    t = ''
                tournament, opponentPlayer, setArray, totalGame, server, winLose, firstSecond, cource, speed, ad = addRowData(
                    i, t, op, s, dataServer, dataGame, dwl, dataSpeed, dataAD, tournament, opponentPlayer, setArray, totalGame, server, winLose, firstSecond, cource, speed, ad, title)

    df = pd.DataFrame({'Tournament': tournament,
                       'OpponentPlayer': opponentPlayer,
                       'Set': setArray,
                       'TotalGame': totalGame,
                       'Server': server,
                       'WinLose': winLose,
                       'FirstSecond': firstSecond,
                       'Cource': cource,
                       'Speed': speed,
                       'AceDbF': ad})
    lastGame = dataGame
    lastServer = dataServer
    serverList = list(set(server))
    return df, lastGame, lastServer, serverList


def textToDatabase(title, df, text, op, s=1):  # テキストデータ全体を処理してデータベースに格納する
    text = preConvert(text)
    print(text)

    totalGame, server, winLose, firstSecond, cource, speed, ad, row, index, index2, opponentPlayer, setArray, tournament = initArray()  # 配列を初期化

    #タイブレーク以外のゲームデータ
    dataList = re.findall(
        r'G[0-9]+[一-龥].*\(?.*?\)?',
        text)  # サーブ記載行をすべて抽出してリスト化
    print(dataList)
    pattern = r'G([0-9]+)([一-龥]).*?([○|×]+)\(?(.*)?\)?'
    df_add, lastGame, lastServer, serverList = matchToArray(
        pattern, dataList, op, s, title)
    df = df.append(df_add)

    anotherServerList = [s for s in serverList if lastServer not in s]
    #print(lastGame,lastServer,serverList,anotherServerList[0])
    print(lastGame, lastServer, serverList)

    anotherServer = anotherServerList[0]

    #タイブレークのゲームデータ
    pattern = r'TB.*\(.*\)'
    tiebreak = re.findall(r'TB.*\(.*\)', text)
    if(len(tiebreak) > 0):
        pattern = r'TB.*?([○|×]+)\((.*)\)'
        df_add = matchToArrayTibreak(
            pattern,
            tiebreak,
            op,
            s,
            lastGame,
            lastServer,
            anotherServer,
            title)
        df = df.append(df_add)

    return df


def scrape(url):
    links = [url]
    df = pd.DataFrame({'Tournament': [],
                       'OpponentPlayer': [],
                       'Set': [],
                       'TotalGame': [],
                       'Server': [],
                       'WinLose': [],
                       'FirstSecond': [],
                       'Cource': [],
                       'Speed': [],
                       'AceDbF': []})
    options = Options()
    options.set_headless(True)  # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
    driver = webdriver.Chrome(chrome_options=options)  # ブラウザを起動する

    for i, l in enumerate(links):
        url = l.replace("/l50", "/")
        #print(i,url)
        driver.get(url)  # ブラウザでアクセスする
        time.sleep(1)
        title = driver.find_element_by_class_name(
            'thread-title').text  # 全体をテクスト情報として入手
        text = driver.find_element_by_id('thread-body').text  # 全体をテクスト情報として入手
        text2 = preConvert(text)
        opponentPlayers, array = devideText(text2)

        for p in range(len(array)):
            for s in range(len(array[p])):
                text = array[p][s]
                if(text):
                    df = textToDatabase(title, df, text, opponentPlayers[p], s)
    driver.close()
    driver.quit()
    return df


def preConvert(text):  # テキストの前処理
    text1 = unicodedata.normalize('NFKC', text)  # 全角を半角に変換
    text2 = re.sub(r"([0-9])(\.)", r"\1", text1)
    text2 = re.sub(r"(Ac)(\.)", r"\1", text2)
    text2 = re.sub(r"(Aw)(\.)", r"\1", text2)
    text2 = re.sub(r"(Do)(\.)", r"\1", text2)
    text2 = re.sub(r"(Dn)(\.)", r"\1", text2)
    text2 = text2.replace(" ", "")
    text2 = text2.replace("　", "")
    text2 = text2.replace("/", "")
    text2 = re.sub(r'[0-9]-[0-9]', "", text2)
    return text2


def readTextFile(fileName):  # txtファイルの読み込み
    with open(fileName, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    text2 = ''
    for t in lines:
        text2 += t
    return text2


def calcScore(p_s, p_r):
    score = ["0", "15", "30", "40", "Ad"]
    s_s = ""
    s_r = ""
    if((p_s < 4) & (p_r < 4)):
        s_s = score[p_s]
        s_r = score[p_r]
    elif((p_s - p_r) == 1):
        s_s = score[4]
        s_r = score[3]
    elif((p_s - p_r) == -1):
        s_s = score[3]
        s_r = score[4]
    elif((p_s - p_r) == 0):
        s_s = score[3]
        s_r = score[3]
    return s_s, s_r


def scoreToDataFrame(df):
    side = ["Deuce", "Ad"]
    score_serve_array = []
    score_return_array = []
    side_array = []
    wonA_array = []
    wonB_array = []

    preGame = df.iloc[0]["TotalGame"]
    p_s = 0
    p_r = 0
    for i in range(len(df)):
        game = df.iloc[i]["TotalGame"]
        if(preGame != game):
            p_s = 0
            p_r = 0
        if(game == 13):
            score_s, score_r = p_s, p_r
        else:
            score_s, score_r = calcScore(p_s, p_r)
        sd = side[(p_s + p_r) % 2]
        score_serve_array.append(score_s)
        score_return_array.append(score_r)
        side_array.append(sd)

        if(df.iloc[i]["WinLose"] == '○'):
            p_s += 1
            wonA_array.append(1)
            wonB_array.append(0)
        elif(df.iloc[i]["WinLose"] == '×'):
            p_r += 1
            wonA_array.append(0)
            wonB_array.append(1)
        else:
            wonA_array.append("")
            wonB_array.append("")
        preGame = df.iloc[i]["TotalGame"]

    df['ScoreServer'] = score_serve_array
    df['ScoreReturner'] = score_return_array
    df['Side'] = side_array
    df['WonA'] = wonA_array
    df['WonB'] = wonB_array
    return df
