import streamlit as st
from openai import OpenAI

# ✅ مفتاح OpenAI مباشر
client = OpenAI(api_key="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")

# ✅ توليد الحكم
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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ خطأ أثناء الاتصال بـ OpenAI: {e}"

# ✅ واجهة المستخدم
st.set_page_config(page_title="القاضي الذكي", layout="centered")
st.title("⚖️ استشارة القاضي الذكي")

user_input = st.text_area("✍️ اكتب هنا وقائع القضية أو النزاع:", height=300, placeholder="مثال: قام المدعى بتأجير سيارة للمدعى عليه مقابل مبلغ...")

if st.button("🧠 إصدار الحكم من القاضي الذكي"):
    if user_input.strip() == "":
        st.warning("يرجى كتابة نص القضية أولاً.")
    else:
        with st.spinner("📚 يتم قراءة القضية..."):
            result = ask_judge_agent(user_input)
            st.subheader("📜 الحكم الصادر:")
            st.text_area("الناتج:", result, height=400)
