import streamlit as st
import sqlite3
import pandas as pd
import datetime

# データベース接続
conn = sqlite3.connect('health_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (date TEXT, weight REAL, bp_high INTEGER, bp_low INTEGER, 
              alcohol INTEGER, exercise INTEGER)''')
conn.commit()

st.title('健康管理アプリ 🏃‍♂️')

# 入力フォーム
with st.form("my_form"):
    d_date = st.date_input("日付", datetime.date.today())
    weight = st.number_input("体重 (kg)", step=0.1, format="%.1f")
    
    col1, col2 = st.columns(2)
    with col1:
        bp_high = st.number_input("血圧（上）", step=1)
    with col2:
        bp_low = st.number_input("血圧（下）", step=1)
        
    alcohol = st.number_input("お酒（本）", step=1)
    exercise = st.number_input("運動（分）", step=10)
    
    submitted = st.form_submit_button("記録する", type="primary")

    if submitted:
        c.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
                  (d_date, weight, bp_high, bp_low, alcohol, exercise))
        conn.commit()
        st.success("保存完了！")

# 履歴表示
st.divider()
st.subheader("📝 過去の記録")

# データを読み込んで新しい順に並べる
df = pd.read_sql_query("SELECT * FROM records ORDER BY date DESC", conn)

if not df.empty:
    st.dataframe(df)
    st.line_chart(df.set_index("date")["weight"])
else:
    st.info("まだ記録がありません")
