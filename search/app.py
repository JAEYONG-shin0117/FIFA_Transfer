import streamlit as st
import pandas as pd

# CSV 불러오기
df = pd.read_csv('data/players.csv')

st.title("⚽ Sofifa 선수 검색")

# 검색 필터
name = st.text_input("선수 이름 (부분 검색 가능)")
position = st.selectbox("포지션", ['ALL'] + sorted(df['player_positions'].unique()))
nation = st.selectbox("국적", ['ALL'] + sorted(df['nationality_name'].unique()))

# 필터 적용
filtered = df.copy()
if name:
    filtered = filtered[filtered['short_name'].str.contains(name, case=False)]
if position != 'ALL':
    filtered = filtered[filtered['player_positions'].str.contains(position)]
if nation != 'ALL':
    filtered = filtered[filtered['nationality_name'] == nation]

# 결과 출력
st.write(f"🔍 총 {len(filtered)}명 검색됨")
st.dataframe(filtered[['short_name', 'player_positions', 'overall', 'value_eur', 'club_name']])
