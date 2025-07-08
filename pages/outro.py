import streamlit as st
import datetime
import gspread

st.title("Outro")

if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False

if not st.session_state["uploaded"]:
    st.warning("Do not close the tab! Data is uploading!")
    # Write to worksheet
    worksheet: gspread.Worksheet = st.session_state["worksheet"]
    batch_cells = []
    row_idx = st.session_state["row_idx"]
    batch_cells.append({"range": f"A{row_idx}", "values": [[2]]})  # Update status
    batch_cells.append(
        {
            "range": f"F{row_idx}",
            "values": [[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
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
    st.info("Your response has been recorded.")
    st.text("Thank you for taking part in our experiment!")
    st.text("You can now close the tab.")
