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
