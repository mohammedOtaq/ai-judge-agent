import streamlit as st
import json
import os
import openai

st.set_page_config(page_title="إضافة سابقة", layout="centered")

# مفتاح OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# إعداد الملفات
file_path = "precedents.json"
attachments_dir = "attachments"
os.makedirs(attachments_dir, exist_ok=True)

def load_precedents():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_precedent(new_entry):
    precedents = load_precedents()
    precedents.append(new_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(precedents, f, ensure_ascii=False, indent=2)

# واجهة النموذج
st.title("➕ إضافة سابقة قضائية جديدة")

with st.form("precedent_form"):
    case_number = st.text_input("📁 رقم القضية", "999/2025")
    case_type = st.selectbox("⚖️ نوع القضية", ["مدني جزئي", "مدني كلي", "تجاري", "إيجار"])
    legal_articles = st.text_input("📚 المواد القانونية (مفصولة بفاصلة)", "267,742")
    summary = st.text_area("📝 وصف مختصر للقضية")
    decision = st.text_area("📌 القرار")
    reasoning = st.text_area("📖 الحيثيات")
    keywords = st.text_input("🔍 كلمات مفتاحية (مفصولة بفاصلة)", "إيجار, عقد, ضرر")

    uploaded_files = st.file_uploader(
        "📎 مرفقات القضية (PDF، صور، أو Word)", 
        type=["pdf", "jpg", "png", "jpeg", "docx"],
        accept_multiple_files=True
    )

    submitted = st.form_submit_button("💾 حفظ السابقة")

    if submitted:
        saved_files = []
        for file in uploaded_files:
            file_path_out = os.path.join(attachments_dir, file.name)
            with open(file_path_out, "wb") as f:
                f.write(file.getbuffer())
            saved_files.append(file.name)

        new_case = {
            "رقم_القضية": case_number.strip(),
            "نوع_القضية": case_type,
            "المواد": [x.strip() for x in legal_articles.split(",")],
            "الوصف": summary.strip(),
            "القرار": decision.strip(),
            "الحيثيات": reasoning.strip(),
            "الكلمات_المفتاحية": [x.strip() for x in keywords.split(",")],
            "المرفقات": saved_files
        }

        save_precedent(new_case)
        st.success("✅ تم حفظ السابقة القضائية والمرفقات بنجاح!")

# 🤖 المساعد القضائي
st.markdown("---")
st.subheader("🤖 استشارة القاضي الذكي")

if st.button("استشارة AI Agent"):
    prompt = f"""هذه قضية جديدة:
رقم القضية: {case_number}
نوعها: {case_type}
المواد القانونية: {legal_articles}
الوصف: {summary}
الحيثيات: {reasoning}
ما هو الحكم المتوقع لهذه القضية مع التسبيب؟"""

    with st.spinner("🤖 جاري تحليل القضية..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت قاضٍ خبير في القانون المدني. أجب بصيغة قضائية رسمية."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            result = response['choices'][0]['message']['content']
            st.success("✅ تم توليد الحكم الذكي:")
            st.text_area("📋 الحكم الذكي المقترح:", result, height=300)
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء الاستشارة: {e}")
import streamlit as st
import json
import os

st.set_page_config(page_title="السوابق القضائية", layout="centered")
st.title("📚 عرض السوابق القضائية")

def load_precedents(file_path="precedents.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

precedents = load_precedents()

if not precedents:
    st.info("لا توجد سوابق محفوظة بعد.")
else:
    all_keywords = set(kw for case in precedents for kw in case.get("الكلمات_المفتاحية", []))
    keyword = st.selectbox("فلترة حسب الكلمة المفتاحية", ["الكل"] + sorted(all_keywords))

    filtered = [c for c in precedents if keyword == "الكل" or keyword in c.get("الكلمات_المفتاحية", [])]

    st.markdown(f"### عدد النتائج: {len(filtered)}")
    for case in filtered:
        with st.expander(f"📝 {case['رقم_القضية']} – {case['الوصف']}"):
            st.write(f"**القرار:** {case['القرار']}")
            st.text_area("الحيثيات:", case["الحيثيات"], height=200)
import streamlit as st
import json
import os
import openai

st.set_page_config(page_title="إضافة سابقة", layout="centered")

# مفتاح OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# إعداد الملفات
file_path = "precedents.json"
attachments_dir = "attachments"
os.makedirs(attachments_dir, exist_ok=True)

def load_precedents():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_precedent(new_entry):
    precedents = load_precedents()
    precedents.append(new_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(precedents, f, ensure_ascii=False, indent=2)

# واجهة النموذج
st.title("➕ إضافة سابقة قضائية جديدة")

with st.form("precedent_form"):
    case_number = st.text_input("📁 رقم القضية", "999/2025")
    case_type = st.selectbox("⚖️ نوع القضية", ["مدني جزئي", "مدني كلي", "تجاري", "إيجار"])
    legal_articles = st.text_input("📚 المواد القانونية (مفصولة بفاصلة)", "267,742")
    summary = st.text_area("📝 وصف مختصر للقضية")
    decision = st.text_area("📌 القرار")
    reasoning = st.text_area("📖 الحيثيات")
    keywords = st.text_input("🔍 كلمات مفتاحية (مفصولة بفاصلة)", "إيجار, عقد, ضرر")

    uploaded_files = st.file_uploader(
        "📎 مرفقات القضية (PDF، صور، أو Word)", 
        type=["pdf", "jpg", "png", "jpeg", "docx"],
        accept_multiple_files=True
    )

    submitted = st.form_submit_button("💾 حفظ السابقة")

    if submitted:
        saved_files = []
        for file in uploaded_files:
            file_path_out = os.path.join(attachments_dir, file.name)
            with open(file_path_out, "wb") as f:
                f.write(file.getbuffer())
            saved_files.append(file.name)

        new_case = {
            "رقم_القضية": case_number.strip(),
            "نوع_القضية": case_type,
            "المواد": [x.strip() for x in legal_articles.split(",")],
            "الوصف": summary.strip(),
            "القرار": decision.strip(),
            "الحيثيات": reasoning.strip(),
            "الكلمات_المفتاحية": [x.strip() for x in keywords.split(",")],
            "المرفقات": saved_files
        }

        save_precedent(new_case)
        st.success("✅ تم حفظ السابقة القضائية والمرفقات بنجاح!")

# 🤖 المساعد القضائي
st.markdown("---")
st.subheader("🤖 استشارة القاضي الذكي")

if st.button("استشارة AI Agent"):
    prompt = f"""هذه قضية جديدة:
رقم القضية: {case_number}
نوعها: {case_type}
المواد القانونية: {legal_articles}
الوصف: {summary}
الحيثيات: {reasoning}
ما هو الحكم المتوقع لهذه القضية مع التسبيب؟"""

    with st.spinner("🤖 جاري تحليل القضية..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت قاضٍ خبير في القانون المدني. أجب بصيغة قضائية رسمية."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            result = response['choices'][0]['message']['content']
            st.success("✅ تم توليد الحكم الذكي:")
            st.text_area("📋 الحكم الذكي المقترح:", result, height=300)
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء الاستشارة: {e}")
