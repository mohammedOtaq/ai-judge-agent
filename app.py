import streamlit as st
import openai

# التحقق من مفتاح الـ API: نستخدم st.secrets إذا كان موجودًا، وإلا يُطلب من المستخدم إدخاله.
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.text_input("أدخل مفتاح OpenAI API الخاص بك:", type="password")
    if not api_key:
        st.info("يرجى إدخال مفتاح OpenAI API للمتابعة.")
        st.stop()

openai.api_key = api_key

# تصميم واجهة المستخدم
st.title("القاضي الذكي")
inquiry = st.text_input("الاستفسار:")
case_text = st.text_area("تفاصيل القضية:")

def analyze_case(inquiry, case_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت قاضٍ ذكي تقوم بتحليل القضايا."},
            {"role": "user", "content": f"الاستفسار: {inquiry}\nتفاصيل القضية: {case_text}"}
        ]
    )
    return response.choices[0].message["content"]

if st.button("تحليل القضية"):
    st.write("جارٍ تحليل القضية...")
    try:
        result = analyze_case(inquiry, case_text)
        st.success(result)
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")
