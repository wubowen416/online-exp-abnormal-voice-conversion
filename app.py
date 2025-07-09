import streamlit as st
import datetime

st.title("ようこそ")

if "agree" not in st.session_state:
    st.session_state["agree"] = False

if not st.session_state["agree"]:
    with st.container(border=True):
        st.header("実験概要")
        st.text(
            "本実験は、人工知能で合成した発話のクオリティを調査することを目的としています。\n\n"
            "被験者には、複数の合成音を聞いていただき、発話のクオリティに関する質問にご回答いただきます。所要時間は15～20分程度です。\n\n"
            "本実験は、音声を聞く必要がありますので、イヤホンかスピーカーを準備してください。"
        )

        st.header("同意書")
        st.text(
            "本実験では、年齢および性別の情報を収集いたします。収集した情報はデータ解析の目的のみに使用し、それ以外の目的には一切使用いたしません。"
        )
        st.text(
            "「同意する」ボタンをクリックされた時点で、上記の内容を十分に理解し、同意いただいたものとみなします。ご同意いただけない場合は、本研究への参加を中止し、画面を閉じてください。"
        )
        if st.button(label="同意する"):
            st.session_state["agree"] = True
            st.rerun()
else:
    with st.container(border=True):
        userid = st.text_input(
            label="ユーザーID", placeholder="ユーザーIDを半角で入力してください"
        )
        userid_reinput = st.text_input(
            label="ユーザーIDの確認",
            placeholder="もう一度ユーザーIDを半角で入力してください",
        )
        gender = st.radio(
            label="性別",
            options=["男性", "女性", "その他"],
            horizontal=True,
            index=None,
        )
        age = st.radio(
            label="年齢",
            options=["20代以下", "20代", "30代", "40代", "50代", "60代", "70代以上"],
            horizontal=True,
            index=None,
        )

        if st.button(
            label="提出", disabled=userid is None or gender is None or age is None
        ):
            if userid_reinput != userid:
                st.warning(
                    "2回入力されたユーザーIDが一致していません。ユーザーIDを再度ご確認ください。"
                )
            else:
                st.session_state["userid"] = userid
                st.session_state["gender"] = gender
                st.session_state["age"] = age
                st.session_state["start_time"] = datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S"
                )
                st.switch_page("pages/intro.py")
