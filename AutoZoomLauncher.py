import time
import webbrowser as web
import pandas as pd
import datetime as dt
import pyautogui as pgui
import schedule as sc


def join_room(ID, password):
    # ブラウザ経由でzoomに参加
    url = 'https://zoom.us/j/' + ID + '?pwd=' + password  # ブラウザに入力するurl
    web.open(url)
    time.sleep(30)
    pgui.write(password)
    pgui.hotkey('enter')
    time.sleep(60)
    pgui.click
    pgui.hotkey('win', 'alt', 'r')


def check_time():
    # 今日の授業のリストを作成
    today = dt.datetime.now().strftime('%a')  # 今日の曜日を取得
    lecture = pd.read_csv('schedule.csv', header=0, dtype=object).values.tolist()  # schedule.csvからリストを作成
    list_lecture = [i for i in lecture if i[0] == today]  # 作成したリストから今日の曜日に一致するものを抽出
    
    # リスト内の時間の型を文字列から日付の型に変換
    for i in list_lecture:
        i[1] = dt.datetime.strptime(i[1], '%H:%M')
        i[2] = dt.datetime.strptime(i[2], '%H:%M')
        
    in_class = False  # ミーティング参加状況のフラグ
    time_class = -1
    
    # 時間を監視してミーティングに参加
    while True:
        time.sleep(1)
        now = dt.datetime.now().time().strftime('%H:%M')
        if now == '23:59':  # 23時59分なら時間監視のループを停止
            break
        else:
            now = dt.datetime.strptime(now, '%H:%M')
            if in_class == False:
                for i in list_lecture:
                    if i[1] <= now <= i[2]:
                        join_room(str(i[3]), str(i[4]))
                        time_class +=1
                        in_class = True
            elif in_class == True:
                if now > list_lecture[time_class][2]:
                    pgui.hotkey('alt', 'q')
                    in_class = False


def reflesh():
    sc.every().day.at("00:01").do(check_time)  # 毎日0時1分にcheck_time()を起動
    
    # 時間監視用のループ
    while True:
        sc.run_pending()
        time.sleep(1)


check_time()
reflesh()