import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import tempfile

# ✅ مفتاح OpenAI مباشر (تأكد من سريته لاحقًا)
client = OpenAI(api_key="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")

# ✅ دالة توليد الحكم القضائي من GPT
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

# ✅ دالة تصدير الحكم إلى PDF
def export_to_pdf(hukm_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in hukm_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# ✅ واجهة Streamlit
st.set_page_config(page_title="القاضي الذكي", layout="centered")
st.title("⚖️ استشارة القاضي الذكي")

# ✍️ إدخال نص القضية من المستخدم
user_input = st.text_area(
    "✍️ اكتب هنا وقائع القضية أو النزاع:",
    height=300,
    placeholder="مثال: قام المدعى بتأجير سيارة للمدعى عليه مقابل مبلغ وقدره..."
)

# 🧠 زر إصدار الحكم
if st.button("🧠 إصدار الحكم من القاضي الذكي"):
    if user_input.strip() == "":
        st.warning("يرجى كتابة نص القضية أولاً.")
    else:
        with st.spinner("📚 يتم قراءة القضية وتحليلها..."):
            result = ask_judge_agent(user_input)
            st.success("✅ تم إصدار الحكم بنجاح")
            st.subheader("📜 الحكم الصادر:")
            st.text_area("الناتج:", result, height=400)

            # 📄 تحميل PDF
            pdf_path = export_to_pdf(result)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 تحميل الحكم كـ PDF",
                    data=pdf_file,
                    file_name="الحكم_القضائي.pdf",
                    mime="application/pdf"
                )
