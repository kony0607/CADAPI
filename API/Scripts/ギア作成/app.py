import streamlit as st
import time

st.title("🍇 次世代型ブドウ棚管理システム")

# ダミーの天気データ取得
weather = st.sidebar.selectbox("現在の天気（シミュレーション）", ["晴れ", "雨"])

if weather == "雨":
    st.error("🚨 雨を検知しました！自動で棚を閉じます。")
    # ここで実際にモータを閉じる関数を呼ぶ予定
else:
    st.success("☀️ 現在は晴れです。")

# 操作パネル
st.subheader("マニュアル操作")
col1, col2 = st.columns(2)
with col1:
    if st.button("全開"):
        st.write("開いています...")
with col2:
    if st.button("全閉"):
        st.write("閉じています...")

# 動作ログ
st.divider()
st.subheader("動作ログ")
st.text(f"[{time.strftime('%H:%M:%S')}] システム稼働中")
if weather == "雨":
    st.text(f"[{time.strftime('%H:%M:%S')}] 【自動】雨天のため全閉を実行")