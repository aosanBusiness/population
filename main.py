import pandas as pd
import altair as alt
import streamlit as st

df = pd.read_csv("pop.csv")

st.sidebar.write("""
# 都道府県別人口推移
以下のオプションから表示年数を指定してください。
""")

st.sidebar.write("""
## 表示年数の選択
""")

years = st.sidebar.slider("年", 1, 16, 5)

st.write(f"""
### **{years}年間** の都道府県別人口
""")

try:
    df = df[:years]
    prefectures = st.multiselect(
        "都道府県を選択してください",
        list(df.columns)[1:],
        ["北海道", "東京都", "沖縄県"]
    )
    if not prefectures:
        st.error("少なくとも一県は選んでください。")
    else:
        prefectures.insert(0, "年")
        data = df[prefectures]
        st.write("### 人口の変遷")
        st.dataframe(data, width=600, height=200)
        # dataをピポットテーブルの逆処理で変形
        data = pd.melt(data, id_vars=["年"]).rename(
            columns={"variable":"都道府県", "value":"人口 (千人)"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                #x="年:T",
                x="年",
                y=alt.Y("人口 (千人):Q", stack=None, scale=alt.Scale(domain=[0,15000])),
                color="都道府県:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )

