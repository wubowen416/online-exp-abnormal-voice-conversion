import streamlit as st
import datetime
import pytz
from google.cloud import firestore

st.title("終わり")

if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False

if not st.session_state["uploaded"]:
    st.warning("ただいまデータをアップロード中です。タブを閉じないでください。")
    # Connect to database
    db = firestore.Client.from_service_account_info(st.secrets["firestore"])

    # Create document data for Firestore
    doc_data = {
        "userid": st.session_state.get("userid", ""),
        "gender": st.session_state.get("gender", ""),
        "age": st.session_state.get("age", ""),
        "comment": st.session_state["comment"],  # Record comment
        "start_time": st.session_state.get("start_time"),
        "finishing_time": datetime.datetime.now(pytz.timezone("Asia/Tokyo")).strftime(
            "%Y-%m-%d_%H-%M-%S"
        ),  # Record finishing time
        "intonation": ",".join(
            [str(v) for v in st.session_state["results"]["intonation"]]
        ),  # Record intonation
        "intelligibility": ",".join(
            [str(v) for v in st.session_state["results"]["intelligibility"]]
        ),  # Record intelligibility
        "pair_indices": ",".join(
            [str(i) for i in st.session_state["pair_indices"]]
        ),  # Record the shuffled indices
    }

    # Write to Firestore collection
    db.collection("responses").add(doc_data)
    st.session_state["uploaded"] = True
    st.rerun()
else:
    st.info("ご回答は正常に記録されました。")
    st.text("ご協力ありがとうございました。")
    st.text("本実験にご参加いただき、誠にありがとうございました。")
    st.text("これで終了です。タブを閉じていただいて構いません。")

    st.subheader("Crowd Works ユーザーへ")
    st.text("Crowd Works以外のユーザーは無視してください")
    st.text(
        "Crowd Worksの画面上の、合言葉を入れる欄に次のひらがな4文字を入力してください。\n\n"
        "「じんこう」"
    )
