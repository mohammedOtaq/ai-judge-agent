import streamlit as st
import json
import os

# إعداد الصفحة
st.set_page_config(page_title="عرض السوابق القضائية", layout="wide")
st.title("📚 عرض السوابق القضائية")

# مسار ملف السوابق
file_path = "precedents.json"

# دالة لتحميل السوابق من الملف
def load_precedents():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# تحميل السوابق
precedents = load_precedents()

# التحقق من وجود السوابق
if not precedents:
    st.info("لا توجد سوابق قضائية محفوظة حتى الآن.")
else:
    st.write(f"تم العثور على {len(precedents)} سابقة قضائية:")
    for idx, precedent in enumerate(precedents, start=1):
        with st.expander(f"سابقة {idx}: قضية رقم {precedent.get('رقم_القضية', 'غير محدد')}"):
            st.markdown(f"**رقم القضية:** {precedent.get('رقم_القضية', 'غير محدد')}")
            st.markdown(f"**نوع القضية:** {precedent.get('نوع_القضية', 'غير محدد')}")
            st.markdown("**المواد القانونية:**")
            for article in precedent.get("المواد", []):
                st.write(f"- {article}")
            st.markdown("**الوصف:**")
            st.write(precedent.get("الوصف", ""))
            st.markdown("**القرار:**")
            st.write(precedent.get("القرار", ""))
            st.markdown("**الحيثيات:**")
            st.write(precedent.get("الحيثيات", ""))
            st.markdown("**الكلمات المفتاحية:**")
            st.write(", ".join(precedent.get("الكلمات_المفتاحية", [])))
            attachments = precedent.get("المرفقات", [])
            if attachments:
                st.markdown("**المرفقات:**")
                for attachment in attachments:
                    st.write(attachment)

