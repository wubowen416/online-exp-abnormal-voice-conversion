import streamlit as st

st.title("実験紹介")

with st.container(border=True):
    st.header("内容")
    st.text(
        "本実験では、5〜10秒程度の発話音声のペアを聞いていただき、その音声に関する質問にご回答ください。\n\n"
        "各音声ペアに、以下に関する質問が用意されています。\n"
        "(1) イントネーションの自然さ：イントネーションが、どちらの音声の方が自然に聞こえるかを評価してください。\n"
        "(2) 明瞭性：発話内容がどちらの音声の方が聞き取りやすいかを評価してください。\n\n"
        "各質問にはラジオボタン式の選択肢があります。\n"
        "音声ペアをAとBとした場合、ラジオボタンは以下の5個で構成されています。もっとも当てはまるものを選択してください。\n"
        "(1) Aの方が良い\n"
        "(2) Aの方がやや良い\n"
        "(3) どちらとも言えない\n"
        "(4) Bの方がやや良い\n"
        "(5) Bの方が良い\n\n"
        "どちらも同じくらい良い、もしくはどちらも同じくらい良くない場合は、「(3) どちらとも言えない」を選んでください。\n\n"
        "音声は必要に応じて繰り返し聞くことが可能です。\n\n"
        "全部で26の音声ペアを聞いて評価していただきます。所要時間は15～20分程度です。"
    )

    st.header("インタフェース")
    st.text(
        "以下に、実際に使用していただくインターフェースの例を示します。\n\n"
        "- 音声を再生して、スピーカーの動作を事前に確認できます。\n\n"
        "- 画面が大きすぎる・小さすぎる場合は、ブラウザのズーム機能（Ctrl/CMD＋「+」「-」キー）で拡大・縮小してください。"
    )

    with st.container(border=True):
        st.subheader("音声を聞いていただき、質問にご回答ください。")
        columns = st.columns(2, border=True)
        columns[0].text("Audio A")
        columns[0].audio(
            "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/202507-abnormal-voice-conversion/qvc/100.wav"
        )
        columns[1].text("Audio B")
        columns[1].audio(
            "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/202507-abnormal-voice-conversion/qvc_enc_p_flow/100.wav"
        )
        st.radio(
            "Q1: イントネーションの自然さについて、どちらの方が自然に聞こえますか？",
            options=[
                "Aの方が良い",
                "Aの方がやや良い",
                "どちらとも言えない",
                "Bの方がやや良い",
                "Bの方が良い",
            ],
            index=None,
        )
        st.radio(
            "Q2: 明瞭性について、どちらの方が聞き取りやすいと感じますか？",
            options=[
                "Aの方が良い",
                "Aの方がやや良い",
                "どちらとも言えない",
                "Bの方がやや良い",
                "Bの方が良い",
            ],
            index=None,
        )
        st.button("提出", help="下の「実験へ」で次へ行けます")

next_button = st.button(label="実験へ")
if next_button:
    st.switch_page("pages/exp.py")
