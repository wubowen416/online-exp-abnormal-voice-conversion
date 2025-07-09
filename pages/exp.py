import streamlit as st
import time
import datetime
import gspread
import numpy as np

# np.random.seed(1234)


def claim_row_atomically(worksheet: gspread.Worksheet, row_idx_to_claim: int):
    """
    Attempts to claim a row by atomically changing column B from '0' to claim_value.
    Returns True if successful, False otherwise.
    """
    try:
        find_replace_request = {
            "findReplace": {
                "find": "0",  # Value indicating 'available'
                "replacement": "1",  # Value indicating 'claimed by this user'
                "matchCase": True,
                "matchEntireCell": True,
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": row_idx_to_claim,
                    "endRowIndex": row_idx_to_claim + 1,
                    "startColumnIndex": 0,  # Assuming status is in Column A (0-indexed B is 1)
                    "endColumnIndex": 1,
                },
            }
        }
        body = {"requests": [find_replace_request]}
        response = worksheet.spreadsheet.batch_update(body)

        # Check if the replacement was made
        # The exact structure of response['replies'] might need verification
        if response["replies"] and response["replies"][0].get("findReplace"):
            occurrences_changed = response["replies"][0]["findReplace"].get(
                "occurrencesChanged", 0
            )
            return occurrences_changed > 0
        return False
    except Exception as e:
        st.error(f"Error during atomic claim for row {row_idx_to_claim}: {e}")
        return False


def get_url(idx: str, name: str = ""):
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/202507-abnormal-voice-conversion/{name}/{idx}.wav"
    return url


# Retrieve data
if "row_idx" not in st.session_state:
    st.warning("Retrieving data. Please wait...")
    try:
        credentials = st.secrets["connections"]["gsheets"]
        gc = gspread.service_account_from_dict(info=credentials)
        sh = gc.open_by_url(credentials["spreadsheet"])
        worksheet = sh.get_worksheet(0)
        st.session_state["worksheet"] = worksheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        st.error("Attempting rerunning in 3 seconds...")
        time.sleep(3.0)
        st.rerun()

    # Get header
    columns = worksheet.row_values(1)

    # Get a available row to store data
    row_idx = 1  # Exclude header
    success = False
    while not success:
        success = claim_row_atomically(worksheet, row_idx)
        row_idx += 1
        time.sleep(1.0)
    batch_cells = []
    batch_cells.append(
        {"range": f"B{row_idx}", "values": [[st.session_state["userid"]]]}
    )
    batch_cells.append(
        {"range": f"C{row_idx}", "values": [[st.session_state["gender"]]]}
    )
    batch_cells.append({"range": f"D{row_idx}", "values": [[st.session_state["age"]]]})
    batch_cells.append(
        {
            "range": f"E{row_idx}",
            "values": [[st.session_state["start_time"]]],
        }
    )
    worksheet.batch_update(batch_cells)
    st.session_state["row_idx"] = row_idx
    st.rerun()


if "pairs" not in st.session_state:
    idcs = [
        "001",
        # "002",
        # "004",
        "011",
        "017",
        "021",
        # "024",
        "025",
        "035",
        "036",
        # "038",
        # "039",
        "058",
        "065",
        # "066",
        "071",
        "075",
        "077",
        "086",
        "088",
        "092",
        "093",
    ]
    np.random.shuffle(idcs)
    idcs += ["101", "102", "103", "104"]
    pairs = []
    for idx in idcs:
        pairs.append(
            {
                "A_url": get_url(idx, "qvc"),
                "B_url": get_url(idx, "qvc_enc_p_flow"),
                "swap": np.random.rand() >= 0.5,
            }
        )

    st.session_state["indices"] = idcs
    st.session_state["pairs"] = pairs
if "pair_idx" not in st.session_state:
    st.session_state["pair_idx"] = 0
if "results" not in st.session_state:
    st.session_state["results"] = {"intonation": [], "intelligibility": []}


def choice_to_value(choice: str) -> int:
    value = 0
    match choice:
        case "A":
            value = -2
        case "ややA":
            value = -1
        case "ややB":
            value = 1
        case "B":
            value = 2
    return value


def on_form_submitted():
    # Record choice
    pair = st.session_state["pairs"][st.session_state["pair_idx"]]
    intonation_value = choice_to_value(
        st.session_state[f'intonation_choice_{st.session_state["pair_idx"]}']
    )
    intelligibility_value = choice_to_value(
        st.session_state[f'intelligibility_choice_{st.session_state["pair_idx"]}']
    )

    if pair["swap"]:
        intonation_value = -intonation_value
        intelligibility_value = -intelligibility_value

    st.session_state["results"]["intonation"].append(intonation_value)
    st.session_state["results"]["intelligibility"].append(intelligibility_value)

    # Move to next pair
    st.session_state["pair_idx"] += 1


num_pairs = len(st.session_state["pairs"])
pair_idx = 0

# Interface
st.title("実験")
st.warning(
    "ページを更新したりタブを閉じたりしないでください。入力済みのデータが失われます。"
)
pbar_text = "進捗"
pbar = st.progress(0, text=f"{pbar_text}: {0}/{num_pairs}")


@st.fragment
def exp_fragment():
    # Check if all completed
    if st.session_state["pair_idx"] == num_pairs:
        st.switch_page("pages/comment.py")

    # Get pair info
    pair = st.session_state["pairs"][st.session_state["pair_idx"]]
    # st.write(f'group_id: {pair["group_id"]}')
    A_url = pair["A_url"]
    B_url = pair["B_url"]
    if pair["swap"]:
        A_url, B_url = B_url, A_url

    # Place interface
    with st.container(border=True):
        st.subheader(f"音声を聞いていただき、質問にご回答ください。")
        columns = st.columns(2, border=True)
        columns[0].text("Audio A")
        columns[0].audio(A_url)
        columns[1].text("Audio B")
        columns[1].audio(B_url)
        intonation_choice = st.radio(
            "Q1: イントネーションの自然さについて、どちらの方が自然に聞こえますか？",
            options=[
                "A",
                "ややA",
                "分からない",
                "ややB",
                "B",
            ],
            index=None,
            key=f'intonation_choice_{st.session_state["pair_idx"]}',
            horizontal=True,
        )
        intelligibility_choice = st.radio(
            "Q2: 明瞭性について，どちらの方が聞き取りやすいと感じますか?",
            options=[
                "A",
                "ややA",
                "分からない",
                "ややB",
                "B",
            ],
            index=None,
            key=f'intelligibility_choice_{st.session_state["pair_idx"]}',
            horizontal=True,
        )
        choice_has_not_been_made = (
            intonation_choice == None or intelligibility_choice == None
        )
        st.button(
            "次へ",
            on_click=on_form_submitted,
            disabled=choice_has_not_been_made,
            help="質問にご回答ください" if choice_has_not_been_made else "",
        )

    pbar.progress(
        st.session_state["pair_idx"] / num_pairs,
        f'{pbar_text}: {st.session_state["pair_idx"]}/{num_pairs}',
    )


exp_fragment()
