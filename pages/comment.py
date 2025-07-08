import streamlit as st

st.title("コメント")
st.warning(
    "ページを更新したりタブを閉じたりしないでください。入力済みのデータが失われます。"
)

comment = st.text_area(
    label="コメント欄", placeholder="コメントがあれば入力してください"
)

if st.button(label="提出"):
    st.session_state["comment"] = comment
    st.switch_page("pages/outro.py")
