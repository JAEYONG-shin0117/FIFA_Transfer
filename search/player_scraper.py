from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()  # 또는 ChromeDriver 경로 직접 지정
driver.get("https://sofifa.com/players?offset=0")
time.sleep(3)  # 로딩 대기

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

players = []
for row in soup.select("table tbody tr"):
    try:
        name = row.select_one("td.col-name a").text.strip()
        pos = row.select_one("td.col-name span.pos").text.strip()
        overall = int(row.select_one("td.col-oa").text.strip())
        value_str = row.select_one("td.col-vl").text.strip()
        age = int(row.select_one("td.col-ae").text.strip())

        # € 단위 처리
        if 'M' in value_str:
            value = float(value_str.replace('€', '').replace('M', '')) * 1_000_000
        elif 'K' in value_str:
            value = float(value_str.replace('€', '').replace('K', '')) * 1_000
        else:
            value = 0.0

        players.append({
            "short_name": name,
            "player_positions": pos,
            "overall": overall,
            "value_eur": value,
            "age": age
        })
    except:
        continue

driver.quit()

df = pd.DataFrame(players)
df.to_csv("data/players.csv", index=False)
print(df.head())
