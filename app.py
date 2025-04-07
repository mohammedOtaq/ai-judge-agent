import os
import json
from pathlib import Path

# إنشاء المجلدات
base = Path("ai_judge_agent")
pages = base / "pages"
base.mkdir(exist_ok=True)
pages.mkdir(parents=True, exist_ok=True)

# ملف app.py
with open(base / "app.py", "w", encoding="utf-8") as f:
    f.write("""
import streamlit as st
import json
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_precedents(file_path="precedents.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_case_to_json(case_data, file_path="judgments.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            all_cases = json.load(f)
    else:
        all_cases = []
    all_cases.append(case_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=2)

def save_to_precedents_from_ai(case_id, summary, decision_text):
    new_entry = {
        "رقم_القضية": case_id,
        "نوع_القضية": "مدني جزئي",
        "المواد": ["742", "745", "267"],
        "الوصف": summary.strip(),
        "القرار": decision_text.split("حكمت المحكمة")[0].strip() if "حكمت المحكمة" in decision_text else decision_text[:200],
        "الحيثيات": decision_text.strip(),
        "الكلمات_المفتاحية": ["GPT", "ذكاء اصطناعي", "إيجار"]
    }

    file_path = "precedents.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            precedents = json.load(f)
    else:
        precedents = []

    precedents.append(new_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(precedents, f, ensure_ascii=False, indent=2)

def ask_judge_agent(case_summary, previous_cases):
    context = ""
    for case in previous_cases[-3:]:
        context += f"\\n- الدعوى رقم {case['رقم_القضية']}, {case['الوصف']}, الحكم: {case['القرار']}"

    prompt = f'''
أنت قاضٍ مدني تصدر الأحكام بأسلوب قانوني صارم، بالاستناد إلى العقود والنصوص القانونية.
السوابق المتاحة:
{context}

القضية:
{case_summary}

رجاءً أصدِر حكمك متضمنًا القرار والحيثيات بصياغة قضائية.
'''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"حدث خطأ: {e}"

st.set_page_config(page_title="القاضي الذكي", layout="centered")
st.title("⚖️ المساعد القضائي الذكي")

case_id = st.text_input("رقم الدعوى", "999/2025")
claim_amount = st.number_input("المبلغ المطلوب (درهم)", step=500.0)
documents = st.multiselect("المستندات المقدمة", ["عقد إيجار", "كشف حساب", "تقرير خبرة", "واتساب"])
has_expert_report = "تقرير خبرة" in documents
defendant_present = st.radio("هل حضر المدعى عليه؟", ["نعم", "لا"]) == "نعم"

if st.button("إصدار الحكم"):
    case_data = {
        "رقم الدعوى": case_id,
        "المبلغ": claim_amount,
        "المستندات": documents,
        "حضر المدعى عليه": defendant_present,
        "تقرير خبرة": has_expert_report,
        "القرار": f"إلزام المدعى عليه بالمبلغ {claim_amount} درهم مع فائدة قانونية 5%",
        "الحيثيات": "استنادًا إلى العقد الموقع، وتقرير الخبرة، وغياب المدعى عليه، ترى المحكمة إلزامه بالمبلغ."
    }
    save_case_to_json(case_data)
    st.success("✅ تم إصدار الحكم وحفظه.")
    st.json(case_data)

st.markdown("---")
st.subheader("🤖 استشارة القاضي الذكي (GPT)")

if st.button("استشارة AI Agent"):
    summary = f\"""رقم الدعوى: {case_id}
المبلغ: {claim_amount} درهم
المستندات: {', '.join(documents)}
حضور المدعى عليه: {"نعم" if defendant_present else "لا"}
تقرير خبرة: {"موجود" if has_expert_report else "غير موجود"}\"""
    precedents = load_precedents()
    result = ask_judge_agent(summary, precedents)
    st.text_area("الحكم الذكي المقترح:", result, height=300)

    if st.button("📌 حفظ في السوابق"):
        save_to_precedents_from_ai(case_id, summary, result)
        st.success("تم حفظ الحكم الذكي كسابقة قضائية.")
""")

# صفحة عرض السوابق
with open(pages / "1_📚_عرض_السوابق_القضائية.py", "w", encoding="utf-8") as f:
    f.write("""
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
    all_keywords = set(kw for c in precedents for kw in c.get("الكلمات_المفتاحية", []))
    keyword = st.selectbox("فلترة حسب الكلمة المفتاحية", ["الكل"] + sorted(all_keywords))

    filtered = []
    for c in precedents:
        if keyword == "الكل" or keyword in c.get("الكلمات_المفتاحية", []):
            filtered.append(c)

    st.markdown(f"### عدد النتائج: {len(filtered)}")
    for case in filtered:
        with st.expander(f"📝 {case['رقم_القضية']} – {case['الوصف']}"):
            st.write(f"**القرار:** {case['القرار']}")
            st.text_area("الحيثيات:", case["الحيثيات"], height=200)
""")

# ملفات JSON
for filename in ["judgments.json", "precedents.json"]:
    with open(base / filename, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# ملف البيئة
with open(base / ".env", "w", encoding="utf-8") as f:
    f.write("OPENAI_API_KEY=\n")

# المتطلبات
with open(base / "requirements.txt", "w", encoding="utf-8") as f:
    f.write("streamlit\nopenai\npython-dotenv\nfpdf\nrequests")

print("✅ تم إنشاء مشروع ai_judge_agent بنجاح! 🎉")
