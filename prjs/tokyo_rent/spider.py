# -*- coding: utf-8 -*-

#必要なライブラリをインポート
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import numpy as np

def summo_spider(url_list, location_list):
    for data_i, url in enumerate(url_list):
        print("[info] location: {}".format(location_list[data_i]))
        #データ取得
        result = requests.get(url)
        c = result.content
    
        #HTMLを元に、オブジェクトを作る
        soup = BeautifulSoup(c)
    
        #物件リストの部分を切り出し
        summary = soup.find("div",{'id':'js-bukkenList'})
    
        #ページ数を取得
        body = soup.find("body")
        pages = body.find_all("div",{'class':'pagination pagination_set-nav'})
        pages_text = str(pages)
        pages_split = pages_text.split('</a></li>\n</ol>')
        pages_split0 = pages_split[0]
        pages_split1 = pages_split0[-3:]
        pages_split2 = pages_split1.replace('>','')
        pages_split3 = int(pages_split2)
    
        #URLを入れるリスト
        urls = []
    
        #1ページ目を格納
        urls.append(url)
    
        #2ページ目から最後のページまでを格納
        for i in range(pages_split3-1):
            pg = str(i+2)
            url_page = url + '&pn=' + pg
            urls.append(url_page)
    
        name = [] #マンション名
        address = [] #住所
        locations0 = [] #立地1つ目（最寄駅/徒歩~分）
        locations1 = [] #立地2つ目（最寄駅/徒歩~分）
        locations2 = [] #立地3つ目（最寄駅/徒歩~分）
        age = [] #築年数
        height = [] #建物高さ
        floor = [] #階
        rent = [] #賃料
        admin = [] #管理費
        others = [] #敷/礼/保証/敷引,償却
        floor_plan = [] #間取り
        area = [] #専有面積
    
        #各ページで以下の動作をループ
        for url in urls:
            print(url)
            #物件リストを切り出し
            result = requests.get(url)
            c = result.content
            soup = BeautifulSoup(c, "lxml")
            summary = soup.find("div",{'id':'js-bukkenList'})
    
            #マンション名、住所、立地（最寄駅/徒歩~分）、築年数、建物高さが入っているcassetteitemを全て抜き出し
            cassetteitems = summary.find_all("div",{'class':'cassetteitem'})
    
            #各cassetteitemsに対し、以下の動作をループ
            for i in range(len(cassetteitems)):
                #各建物から売りに出ている部屋数を取得
                tbodies = cassetteitems[i].find_all('tbody')
    
                #マンション名取得
                subtitle = cassetteitems[i].find_all("div",{
                    'class':'cassetteitem_content-title'})
                subtitle = str(subtitle)
                subtitle_rep = subtitle.replace(
                    '[<div class="cassetteitem_content-title">', '')
                subtitle_rep2 = subtitle_rep.replace(
                    '</div>]', '')
    
                #住所取得
                subaddress = cassetteitems[i].find_all("li",{
                    'class':'cassetteitem_detail-col1'})
                subaddress = str(subaddress)
                subaddress_rep = subaddress.replace(
                    '[<li class="cassetteitem_detail-col1">', '')
                subaddress_rep2 = subaddress_rep.replace(
                    '</li>]', '')
    
                #部屋数だけ、マンション名と住所を繰り返しリストに格納（部屋情報と数を合致させるため）
                for y in range(len(tbodies)):
                    name.append(subtitle_rep2)
                    address.append(subaddress_rep2)
    
                #立地を取得
                sublocations = cassetteitems[i].find_all("li",{
                    'class':'cassetteitem_detail-col2'})
    
                #立地は、1つ目から3つ目までを取得（4つ目以降は無視）
                for x in sublocations:
                    cols = x.find_all('div')
                    for i in range(len(cols)):
                        text = cols[i].find(text=True)
                        for y in range(len(tbodies)):
                            if i == 0:
                                locations0.append(text)
                            elif i == 1:
                                locations1.append(text)
                            elif i == 2:
                                locations2.append(text)
    
                #築年数と建物高さを取得
                tbodies = cassetteitems[i].find_all('tbody')
                col3 = cassetteitems[i].find_all("li",{
                    'class':'cassetteitem_detail-col3'})
                for x in col3:
                    cols = x.find_all('div')
                    for i in range(len(cols)):
                        text = cols[i].find(text=True)
                        for y in range(len(tbodies)):
                            if i == 0:
                                age.append(text)
                            else:
                                height.append(text)
    
            #階、賃料、管理費、敷/礼/保証/敷引,償却、間取り、専有面積が入っているtableを全て抜き出し
            tables = summary.find_all('table')
    
            #各建物（table）に対して、売りに出ている部屋（row）を取得
            rows = []
            for i in range(len(tables)):
                rows.append(tables[i].find_all('tr'))
    
            #各部屋に対して、tableに入っているtext情報を取得し、dataリストに格納
            data = []
            for row in rows:
                for tr in row:
                    cols = tr.find_all('td')
                    for td in cols:
                        text = td.find(text=True)
                        data.append(text)
    
            #dataリストから、階、賃料、管理費、敷/礼/保証/敷引,償却、間取り、専有面積を順番に取り出す
            index = 0
            for item in data:
                if '階' in item:
                    floor.append(data[index])
                    rent.append(data[index+1])
                    admin.append(data[index+2])
                    others.append(data[index+3])
                    floor_plan.append(data[index+4])
                    area.append(data[index+5])
                index +=1
    
            #プログラムを10秒間停止する（スクレイピングマナー）
            time.sleep(10)
    
            #各リストをシリーズ化
        name = Series(name)
        address = Series(address)
        locations0 = Series(locations0)
        locations1 = Series(locations1)
        locations2 = Series(locations2)
        age = Series(age)
        height = Series(height)
        floor = Series(floor)
        rent = Series(rent)
        admin = Series(admin)
        others = Series(others)
        floor_plan = Series(floor_plan)
        area = Series(area)
    
        #各シリーズをデータフレーム化
        suumo_df = pd.concat([name, address, locations0, locations1, locations2, age, height, floor, rent, admin, others, floor_plan, area], axis=1)
    
        #カラム名
        suumo_df.columns=['マンション名','住所','立地1','立地2','立地3','築年数','建物高さ','階','賃料','管理費', '敷/礼/保証/敷引,償却','間取り','専有面積']
    
        #csvファイルとして保存
        file_name = location_list[data_i] + ".csv"
        suumo_df.to_csv(file_name, sep = '\t',encoding='utf-16')

def exec_spider():
    locations = [
        'shinjuku',
        'shibuya'
    ]
    urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13104&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1',
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13113&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
    ]
    summo_spider(urls, locations)

def concat_csv():
    df_adachi = pd.read_csv('suumo_adachi.csv', sep='\t', encoding='utf-16')
    df_shibuya = pd.read_csv('suumo_shibuya.csv', sep='\t', encoding='utf-16')
    df_shinjuku = pd.read_csv('suumo_shinjuku.csv', sep='\t', encoding='utf-16')
    df = pd.concat([df_adachi, df_shibuya, df_shinjuku], axis=0, ignore_index=True)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #立地を「路線+駅」と「徒歩〜分」に分割
    splitted1 = df['立地1'].str.split(' 歩', expand=True)
    splitted1.columns = ['立地11', '立地12']
    splitted2 = df['立地2'].str.split(' 歩', expand=True)
    splitted2.columns = ['立地21', '立地22']
    splitted3 = df['立地3'].str.split(' 歩', expand=True)
    splitted3.columns = ['立地31', '立地32']
    
    #その他費用を、「敷金」「礼金」「保証金」「敷引,償却」に分割
    splitted4 = df['敷/礼/保証/敷引,償却'].str.split('/', expand=True)
    splitted4.columns = ['敷金', '礼金', '保証金', '敷引,償却']
    
    #「敷引,償却」をさらに「敷引」「償却」に分割
    #TODO no ['敷引,償却']
    splitted5 = df['敷引,償却'].str.split('・', expand=True)
    splitted5.columns = ['敷引', '償却']
    
    #分割したカラムを結合
    df = pd.concat([df, splitted1, splitted2, splitted3, splitted4, splitted5], axis=1)
    
    #分割前のカラムは分析に使用しないので削除しておく
    df.drop(['立地1','立地2','立地3','敷/礼/保証/敷引,償却','敷引,償却'], axis=1, inplace=True)
    
    #「賃料」がNAの行を削除
    df = df.dropna(subset=['賃料'])
    
    #エンコードをcp932に変更しておく（これをしないと、replaceできない）
    df['賃料'].str.encode('cp932')
    df['敷金'].str.encode('cp932')
    df['礼金'].str.encode('cp932')
    df['保証金'].str.encode('cp932')
    df['敷引'].str.encode('cp932')
    df['償却'].str.encode('cp932')
    df['管理費'].str.encode('cp932')
    df['築年数'].str.encode('cp932')
    df['専有面積'].str.encode('cp932')
    df['立地12'].str.encode('cp932')
    df['立地22'].str.encode('cp932')
    df['立地32'].str.encode('cp932')
    
    #数値として扱いたいので、不要な文字列を削除
    df['賃料'] = df['賃料'].str.replace(u'万円', u'')
    df['敷金'] = df['敷金'].str.replace(u'万円', u'')
    df['礼金'] = df['礼金'].str.replace(u'万円', u'')
    df['保証金'] = df['保証金'].str.replace(u'万円', u'')
    df['敷引'] = df['敷引'].str.replace(u'万円', u'')
    df['償却'] = df['償却'].str.replace(u'万円', u'')
    df['管理費'] = df['管理費'].str.replace(u'円', u'')
    df['築年数'] = df['築年数'].str.replace(u'新築', u'0') #新築は築年数0年とする
    df['築年数'] = df['築年数'].str.replace(u'築', u'')
    df['築年数'] = df['築年数'].str.replace(u'年', u'')
    df['専有面積'] = df['専有面積'].str.replace(u'm', u'')
    df['立地12'] = df['立地12'].str.replace(u'分', u'')
    df['立地22'] = df['立地22'].str.replace(u'分', u'')
    df['立地32'] = df['立地32'].str.replace(u'分', u'')
    
    #「-」を0に変換
    df['管理費'] = df['管理費'].replace('-',0)
    df['敷金'] = df['敷金'].replace('-',0)
    df['礼金'] = df['礼金'].replace('-',0)
    df['保証金'] = df['保証金'].replace('-',0)
    df['敷引'] = df['敷引'].replace('-',0)
    df['敷引'] = df['敷引'].replace('実費',0) #「実費」と文字列が入っている場合がある
    df['償却'] = df['償却'].replace('-',0)
    
    #Noneを0に変換
    df['償却'] = [0 if x is None else x for x in df['償却']]
    
    #文字列から数値に変換
    df['賃料'] = pd.to_numeric(df['賃料'])
    df['管理費'] = pd.to_numeric(df['管理費'])
    df['敷金'] = pd.to_numeric(df['敷金'])
    df['礼金'] = pd.to_numeric(df['礼金'])
    df['保証金'] = pd.to_numeric(df['保証金'])
    df['敷引'] = pd.to_numeric(df['敷引'])
    df['償却'] = pd.to_numeric(df['償却'])
    df['築年数'] = pd.to_numeric(df['築年数'])
    df['専有面積'] = pd.to_numeric(df['専有面積'])
    df['立地12'] = pd.to_numeric(df['立地12'])
    df['立地22'] = pd.to_numeric(df['立地22'])
    df['立地32'] = pd.to_numeric(df['立地32'])
    
    #単位を合わせるために、管理費以外を10000倍。
    df['賃料'] = df['賃料'] * 10000
    df['敷金'] = df['敷金'] * 10000
    df['礼金'] = df['礼金'] * 10000
    df['保証金'] = df['保証金'] * 10000
    df['敷引'] = df['敷引'] * 10000
    df['償却'] = df['償却'] * 10000
    
    #管理費は実質的には賃料と同じく毎月支払うことになるため、「賃料+管理費」を家賃を見る指標とする
    df['賃料+管理費'] = df['賃料'] + df['管理費']
    
    #敷金/礼金と保証金は同じく初期費用であり、どちらかが適用されるため、合計を初期費用を見る指標とする
    df['敷/礼/保証金'] = df['敷金'] + df['礼金'] + df['保証金']
    
    #住所を「東京都」「〜区」「市町村番地」に分割
    splitted6 = df['住所'].str.split('区', expand=True)
    splitted6.columns = ['区', '市町村']
    splitted6['区'] = splitted6['区'] + '区'
    splitted6['区'] = splitted6['区'].str.replace('東京都','')

    #路線と駅が３つ以上に分かれてしまう行を削除
    drop_idx = [98764] #手動でindexを確認
    df = df.drop(drop_idx, axis=0)
    
    #立地を「路線」「駅」「徒歩〜分」に分割
    splitted7 = df['立地11'].str.split('/', expand=True)
    splitted7.columns = ['路線1', '駅1']
    splitted7['徒歩1'] = df['立地12']
    splitted8 = df['立地21'].str.split('/', expand=True)
    splitted8.columns = ['路線2', '駅2']
    splitted8['徒歩2'] = df['立地22']
    splitted9 = df['立地31'].str.split('/', expand=True)
    splitted9.columns = ['路線3', '駅3']
    splitted9['徒歩3'] = df['立地32']
    
    #結合
    df = pd.concat([df, splitted6, splitted7, splitted8, splitted9], axis=1)
    
    #不要なカラムを削除
    df.drop(['立地11','立地12','立地21','立地22','立地31','立地32'], axis=1, inplace=True)
    
    #「賃料」がNAの行を削除
    df = df.dropna(subset=['賃料'])
    
    #エンコードをcp932に変更しておく（これをしないと、replaceできない）
    df['賃料'].str.encode('cp932')
    df['敷金'].str.encode('cp932')
    df['礼金'].str.encode('cp932')
    df['保証金'].str.encode('cp932')
    df['敷引'].str.encode('cp932')
    df['償却'].str.encode('cp932')
    df['管理費'].str.encode('cp932')
    df['築年数'].str.encode('cp932')
    df['専有面積'].str.encode('cp932')
    df['立地12'].str.encode('cp932')
    df['立地22'].str.encode('cp932')
    df['立地32'].str.encode('cp932')
    
    #数値として扱いたいので、不要な文字列を削除
    df['賃料'] = df['賃料'].str.replace(u'万円', u'')
    df['敷金'] = df['敷金'].str.replace(u'万円', u'')
    df['礼金'] = df['礼金'].str.replace(u'万円', u'')
    df['保証金'] = df['保証金'].str.replace(u'万円', u'')
    df['敷引'] = df['敷引'].str.replace(u'万円', u'')
    df['償却'] = df['償却'].str.replace(u'万円', u'')
    df['管理費'] = df['管理費'].str.replace(u'円', u'')
    df['築年数'] = df['築年数'].str.replace(u'新築', u'0') #新築は築年数0年とする
    df['築年数'] = df['築年数'].str.replace(u'築', u'')
    df['築年数'] = df['築年数'].str.replace(u'年', u'')
    df['専有面積'] = df['専有面積'].str.replace(u'm', u'')
    df['立地12'] = df['立地12'].str.replace(u'分', u'')
    df['立地22'] = df['立地22'].str.replace(u'分', u'')
    df['立地32'] = df['立地32'].str.replace(u'分', u'')
    
    #「-」を0に変換
    df['管理費'] = df['管理費'].replace('-',0)
    df['敷金'] = df['敷金'].replace('-',0)
    df['礼金'] = df['礼金'].replace('-',0)
    df['保証金'] = df['保証金'].replace('-',0)
    df['敷引'] = df['敷引'].replace('-',0)
    df['敷引'] = df['敷引'].replace('実費',0) #「実費」と文字列が入っている場合がある
    df['償却'] = df['償却'].replace('-',0)
    
    #Noneを0に変換
    df['償却'] = [0 if x is None else x for x in df['償却']]
    
    #文字列から数値に変換
    df['賃料'] = pd.to_numeric(df['賃料'])
    df['管理費'] = pd.to_numeric(df['管理費'])
    df['敷金'] = pd.to_numeric(df['敷金'])
    df['礼金'] = pd.to_numeric(df['礼金'])
    df['保証金'] = pd.to_numeric(df['保証金'])
    df['敷引'] = pd.to_numeric(df['敷引'])
    df['償却'] = pd.to_numeric(df['償却'])
    df['築年数'] = pd.to_numeric(df['築年数'])
    df['専有面積'] = pd.to_numeric(df['専有面積'])
    df['立地12'] = pd.to_numeric(df['立地12'])
    df['立地22'] = pd.to_numeric(df['立地22'])
    df['立地32'] = pd.to_numeric(df['立地32'])
    
    #単位を合わせるために、管理費以外を10000倍。
    df['賃料'] = df['賃料'] * 10000
    df['敷金'] = df['敷金'] * 10000
    df['礼金'] = df['礼金'] * 10000
    df['保証金'] = df['保証金'] * 10000
    df['敷引'] = df['敷引'] * 10000
    df['償却'] = df['償却'] * 10000
    
    #管理費は実質的には賃料と同じく毎月支払うことになるため、「賃料+管理費」を家賃を見る指標とする
    df['賃料+管理費'] = df['賃料'] + df['管理費']
    
    #敷金/礼金と保証金は同じく初期費用であり、どちらかが適用されるため、合計を初期費用を見る指標とする
    df['敷/礼/保証金'] = df['敷金'] + df['礼金'] + df['保証金']
    
    #住所を「東京都」「〜区」「市町村番地」に分割
    splitted6 = df['住所'].str.split('区', expand=True)
    splitted6.columns = ['区', '市町村']
    splitted6['区'] = splitted6['区'] + '区'
    splitted6['区'] = splitted6['区'].str.replace('東京都','')
    
    #階を数値化。地下はマイナスとして扱う
    splitted10 = df['階'].str.split('-', expand=True)
    splitted10.columns = ['階1', '階2']
    splitted10['階1'].str.encode('cp932')
    splitted10['階1'] = splitted10['階1'].str.replace(u'階', u'')
    splitted10['階1'] = splitted10['階1'].str.replace(u'B', u'-')
    splitted10['階1'] = pd.to_numeric(splitted10['階1'])
    df = pd.concat([df, splitted10], axis=1)
    
    #建物高さを数値化。地下は無視。
    df['建物高さ'].str.encode('cp932')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下1地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下2地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下3地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下4地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下5地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下6地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下7地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下8地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'地下9地上', u'')
    df['建物高さ'] = df['建物高さ'].str.replace(u'平屋', u'1')
    df['建物高さ'] = df['建物高さ'].str.replace(u'階建', u'')
    df['建物高さ'] = pd.to_numeric(df['建物高さ'])
    
    #indexを振り直す（これをしないと、以下の処理でエラーが出る）
    df = df.reset_index(drop=True)
    
    #間取りを「部屋数」「DK有無」「K有無」「L有無」「S有無」に分割
    df['間取りDK'] = 0
    df['間取りK'] = 0
    df['間取りL'] = 0
    df['間取りS'] = 0
    df['間取り'].str.encode('cp932')
    df['間取り'] = df['間取り'].str.replace(u'ワンルーム', u'1') #ワンルームを1に変換
    
    for x in range(len(df)):
        if 'DK' in df['間取り'][x]:
            df.loc[x,'間取りDK'] = 1
    df['間取り'] = df['間取り'].str.replace(u'DK',u'')
    
    for x in range(len(df)):
        if 'K' in df['間取り'][x]:
            df.loc[x,'間取りK'] = 1        
    df['間取り'] = df['間取り'].str.replace(u'K',u'')
    
    for x in range(len(df)):
        if 'L' in df['間取り'][x]:
            df.loc[x,'間取りL'] = 1        
    df['間取り'] = df['間取り'].str.replace(u'L',u'')
    
    for x in range(len(df)):
        if 'S' in df['間取り'][x]:
            df.loc[x,'間取りS'] = 1        
    df['間取り'] = df['間取り'].str.replace(u'S',u'')
    
    df['間取り'] = pd.to_numeric(df['間取り'])
    
    #カラムを入れ替えて、csvファイルとして出力
    df = df[['マンション','住所','区','市町村','間取り','間取りDK','間取りK','間取りL','間取りS','築年数','建物高さ','階1','専有面積','賃料+管理費','敷/礼/保証金',
                    '路線1','駅1','徒歩1','路線2','駅2','徒歩2','路線3','駅3','徒歩3','賃料','管理費',
                    '敷金','礼金','保証金','敷引','償却']]
    
    df.to_csv('suumo_tokyo.csv', sep = '\t',encoding='utf-16')

if __name__ == "__main__":
    concat_csv()