import streamlit as st
import numpy as np

np.random.seed(1234)


def get_url(idx: str, name: str = ""):
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/202507-abnormal-voice-conversion/{name}/{idx}.wav"
    return url


if "pairs" not in st.session_state:
    indices = [
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
    np.random.shuffle(indices)
    indices += ["101", "102", "103", "104"]
    pairs = []
    for idx in indices:
        pairs.append(
            {
                "A_url": get_url(idx, "qvc"),
                "B_url": get_url(idx, "qvc_enc_p_flow"),
                "swap": np.random.rand() >= 0.5,
            }
        )

    st.session_state["pair_indices"] = indices
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
progress_bar_text = "進捗"
progress_bar = st.progress(0, text=f"{progress_bar_text}: {0}/{num_pairs}")


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

    progress_bar.progress(
        st.session_state["pair_idx"] / num_pairs,
        f'{progress_bar_text}: {st.session_state["pair_idx"]}/{num_pairs}',
    )


exp_fragment()
