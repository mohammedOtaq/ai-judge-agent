from openai import OpenAI

# ✅ المفتاح مباشرة أو من userdata
api_key = "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"

client = OpenAI(api_key=api_key)

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

# ✅ تشغيل داخل Colab
print("✍️ أدخل نص الدعوى:")
user_input = input()

if user_input.strip() == "":
    print("⚠️ يجب إدخال نص القضية.")
else:
    print("🔎 يتم تحليل الدعوى...")
    result = ask_judge_agent(user_input)
    print("\n📜 الحكم الصادر:\n")
    print(result)
