import streamlit as st
import openai
import os

# تعيين مفتاح الـ API باستخدام st.secrets أو متغير بيئة
# الخيار المفضل للتطبيقات المُستضافة: 
openai.api_key = st.secrets["OPENAI_API_KEY"]
# بديل: openai.api_key = os.getenv("OPENAI_API_KEY")

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
    return response.choices[0].message['content']

if st.button("تحليل القضية"):
    st.write("جارٍ تحليل القضية...")
    try:
        result = analyze_case(inquiry, case_text)
        st.success(result)
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")
