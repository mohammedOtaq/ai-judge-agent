import streamlit as st
from dotenv import load_dotenv
import os
import openai
import docx
import fitz  # PyMuPDF

# ✅ إعداد صفحة Streamlit
st.set_page_config(page_title="⚖️ القاضي الذكي", layout="centered")

# تحميل المتغيرات البيئية
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# دالة استدعاء GPT لإصدار الحكم
def ask_judge_agent(user_input):
    prompt = f"""
أنت قاضٍ مدني محترف تصدر الأحكام بأسلوب قانوني منضبط.
اقرأ القضية التالية التي قدمها المستخدم، ثم أصدِر حكمك الكامل متضمنًا:
- القرار القضائي
- الحيثيات القانونية والواقعية
- الاستناد إلى السوابق إن أمكن

نص الدعوى:
{user_input}

الحكم:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ خطأ أثناء الاتصال بـ OpenAI:\n{e}"

# 🧠 دوال استخراج النص من الملفات
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# 🖥️ واجهة المستخدم
st.title("⚖️ القاضي الذكي")

input_method = st.radio("📎 اختر طريقة إدخال القضية:", ["كتابة يدوية", "رفع ملف PDF / Word"])

user_input = ""

if input_method == "كتابة يدوية":
    user_input = st.text_area("✍️ اكتب هنا وقائع القضية أو النزاع:", height=300)
else:
    uploaded_file = st.file_uploader("📄 ارفع ملف PDF أو Word", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            user_input = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            user_input = extract_text_from_docx(uploaded_file)

        if user_input:
            st.success("✅ تم استخراج نص القضية بنجاح.")
            st.text_area("📄 نص الدعوى المستخرجة:", user_input, height=300)

# 🧠 إصدار الحكم
if st.button("🧠 إصدار الحكم"):
    if not user_input.strip():
        st.warning("يرجى كتابة أو رفع نص القضية.")
    else:
        with st.spinner("📚 يتم تحليل القضية..."):
            result = ask_judge_agent(user_input)
            st.success("✅ تم إصدار الحكم.")
            st.subheader("📜 الحكم الصادر:")
            st.text_area("📜 الناتج:", result, height=400)
