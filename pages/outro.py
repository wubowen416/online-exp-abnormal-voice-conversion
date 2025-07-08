import streamlit as st
import datetime
import gspread

st.title("終わり")

if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False

if not st.session_state["uploaded"]:
    st.warning("ただいまデータをアップロード中です。タブを閉じないでください。")
    # Write to worksheet
    worksheet: gspread.Worksheet = st.session_state["worksheet"]
    batch_cells = []
    row_idx = st.session_state["row_idx"]
    batch_cells.append({"range": f"A{row_idx}", "values": [[2]]})  # Update status
    batch_cells.append(
        {
            "range": f"F{row_idx}",
            "values": [[datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")]],
        }
    )  # Record finishing time
    batch_cells.append(
        {"range": f"G{row_idx}", "values": [[st.session_state["comment"]]]}
    )  # Record comment
    batch_cells.append(
        {
            "range": f"H{row_idx}",
            "values": [
                [",".join([str(v) for v in st.session_state["results"]["intonation"]])]
            ],
        }
    )  # Record intonation
    batch_cells.append(
        {
            "range": f"I{row_idx}",
            "values": [
                [
                    ",".join(
                        [str(v) for v in st.session_state["results"]["intelligibility"]]
                    )
                ]
            ],
        }
    )  # Record intelligibility
    worksheet.batch_update(batch_cells)
    st.session_state["uploaded"] = True
    st.rerun()
else:
    st.info("ご回答は正常に記録されました。")
    st.text("ご協力ありがとうございました。")
    st.text("本実験にご参加いただき、誠にありがとうございました。")
    st.text("これで終了です。タブを閉じていただいて構いません。")
