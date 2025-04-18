import streamlit as st
from dotenv import load_dotenv
import os
import openai
from docx import Document
import fitz  # PyMuPDF
from datetime import datetime, timedelta

# ✅ إعداد صفحة Streamlit
st.set_page_config(page_title="⚖️ القاضي الذكي", layout="centered")

# تحميل المتغيرات البيئية
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ ⏰ التايمر يبدأ عند أول دخول للجلسة
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# تحديد نهاية الوقت (غيّر seconds=10 إلى hours=1 لاحقًا)
end_time = st.session_state.start_time + timedelta(seconds=10)  # للتجربة: 10 ثواني فقط

# حساب الوقت المتبقي
remaining_time = end_time - datetime.now()

if remaining_time.total_seconds() > 0:
    mins, secs = divmod(int(remaining_time.total_seconds()), 60)
    st.info(f"🕒 تبقى من وقتك المجاني: {mins} دقيقة و {secs} ثانية")
else:
    st.error("⛔ انتهى وقت الاستخدام المجاني. الرجاء الترقية لمواصلة الاستخدام.")
    st.stop()  # إيقاف التطبيق مؤقتًا

# 🧠 دالة استدعاء GPT لإصدار الحكم
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

# 📄 قراءة ملفات PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# 📄 قراءة ملفات Word
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# 🖥️ واجهة Streamlit
st.title("⚖️ القاضي الذكي")

# اختيار طريقة الإدخال
input_method = st.radio("📎 اختر طريقة إدخال القضية:", ["كتابة يدوية", "رفع ملف PDF / Word"])

user_input = ""

# الكتابة اليدوية
if input_method == "كتابة يدوية":
    user_input = st.text_area("✍️ اكتب هنا وقائع القضية أو النزاع:", height=300)

# رفع الملفات
else:
    uploaded_file = st.file_uploader("📄 ارفع ملف PDF أو Word", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            user_input = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]:
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
            st.session_state['الحكم'] = result
            st.success("✅ تم إصدار الحكم.")
            st.subheader("📜 الحكم الصادر:")
            st.text_area("📜 الناتج:", result, height=400)

# 🔄 التفاعل مع الحكم
if "الحكم" in st.session_state:
    st.markdown("---")
    st.subheader("🔄 هل توافق على الحكم؟ أو لديك توضيح إضافي؟")

    with st.form("response_form"):
        user_reply = st.text_area("🗣️ اكتب ملاحظتك أو اعتراضك هنا:", height=150)
        submitted = st.form_submit_button("📨 إرسال للمراجعة")

        if submitted:
            with st.spinner("🤖 يتم مراجعة ملاحظتك من قبل القاضي الذكي..."):
                follow_up_prompt = f"""
قمت بإصدار الحكم التالي:
{st.session_state['الحكم']}

ثم قدم المستخدم التوضيح التالي:
{user_reply}

رجاءً راجع التوضيح، وأعد صياغة الحكم أو فسّره بشكل إضافي إذا لزم الأمر.
"""
                follow_up = ask_judge_agent(follow_up_prompt)
                st.success("✅ تم مراجعة الملاحظة.")
                st.subheader("📌 رد القاضي الذكي:")
                st.text_area("📬 الرد:", follow_up, height=300)
import streamlit as st
import datetime

st.title("⌛ اختبار التايمر")

if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.datetime.now()

elapsed = datetime.datetime.now() - st.session_state["start_time"]
remaining = datetime.timedelta(seconds=10) - elapsed

if remaining.total_seconds() > 0:
    st.info(f"⏳ الوقت المتبقي لك: {str(remaining).split('.')[0]}")
else:
    st.warning("🕐 انتهى وقتك المجاني.")
    st.stop()

st.write("✅ تقدر تستخدم الموقع الآن.")
