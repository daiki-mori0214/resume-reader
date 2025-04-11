import streamlit as st
from openai import OpenAI
import pdfplumber

st.set_page_config(page_title="ResuMe Reader AI", layout="centered")

st.title("📄 ResuMe Reader AI")
st.subheader("アップロードされたレジュメをもとに、候補者の適性・ポジション・特性を分析")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("レジュメファイルをアップロード (PDFのみ)", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    st.success("✅ レジュメの読み込み完了")

    prompt_template = f"""
あなたは、人材採用における職務経歴書（レジュメ）分析の専門家です。
以下のレジュメを読み取り、以下の観点で候補者の特徴を要約してください：

1. キャリアの変遷（時系列・規模・役割）
2. 転職の背景・推察される動機（人間関係／承認欲求／上司との相性なども含め）
3. 志向性・強み・行動特性（再現可能性のあるスキルや特性）
4. 適した企業タイプ／職種／ポジションの例（理由付き）
5. フィットしづらい環境やカルチャー（理由付き）

※ 表面的な職務だけでなく、職務内容の記述や職務間の移動・成果から候補者の価値観を想像してください。

【レジュメ全文】
{text}
"""

    with st.spinner("🧠 AIが分析中..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたはハイレベルなレジュメ読み解きのAIです。"},
                {"role": "user", "content": prompt_template}
            ]
        )
        result = response.choices[0].message.content

    st.markdown("---")
    st.subheader("🧠 分析結果")
    st.markdown(result)

    st.markdown("---")
    st.caption("※このツールはβ版です。分析結果の活用はご自身の判断にてお願いします。")
