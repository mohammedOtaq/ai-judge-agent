import streamlit as st
import openai
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# استدعاء مفتاح OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# دالة إصدار الحكم
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
        return f"❌ خطأ أثناء الاتصال بـ OpenAI: {e}"

# واجهة Streamlit
st.set_page_config(page_title="⚖️ القاضي الذكي", layout="centered")
st.title("⚖️ القاضي الذكي")

user_input = st.text_area("✍️ اكتب هنا وقائع القضية أو النزاع:", height=300)

if st.button("🧠 إصدار الحكم"):
    if not user_input.strip():
        st.warning("يرجى كتابة نص القضية.")
    else:
        with st.spinner("📚 يتم تحليل القضية..."):
            result = ask_judge_agent(user_input)
            st.success("✅ تم إصدار الحكم.")
            st.subheader("📜 الحكم الصادر:")
            st.text_area("📜 الناتج:", result, height=400)
