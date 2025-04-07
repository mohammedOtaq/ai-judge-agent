import streamlit as st
from openai import OpenAI

# إعداد صفحة Streamlit
st.set_page_config(page_title="القاضي الذكي", layout="centered")
st.title("⚖️ القاضي الذكي - استشارة قانونية بالذكاء الاصطناعي")

# تحميل مفتاح OpenAI من ملف الأسرار
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# نموذج إدخال البيانات
with st.form("case_form"):
    case_number = st.text_input("📁 رقم القضية", "123/2025")
    case_type = st.selectbox("⚖️ نوع القضية", ["مدني", "تجاري", "جنائي"])
    summary = st.text_area("📝 ملخص القضية")
    submitted = st.form_submit_button("🔍 استشارة القاضي الذكي")

    if submitted:
        # صياغة الطلب إلى النموذج
        prompt = f"""
        هذه قضية:
        رقم القضية: {case_number}
        نوعها: {case_type}
        ملخص القضية: {summary}
        ما هو الحكم المتوقع مع التسبيب القانوني؟
        """

        with st.spinner("🤖 جاري تحليل القضية..."):
            try:
                # إرسال الطلب إلى OpenAI باستخدام GPT-4o
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت قاضٍ محترف متخصص في إصدار الأحكام القانونية."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4
                )

                result = response.choices[0].message.content
                st.success("✅ تم إصدار الحكم المقترح:")
                st.text_area("📋 الحكم الذكي:", result, height=300)

            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")
