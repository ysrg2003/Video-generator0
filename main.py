import os
import json
import asyncio
import edge_tts
import google.generativeai as genai
import sys

# إعداد Gemini من متغيرات البيئة (للحماية)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # تأكد من الاسم المتاح حالياً

async def run_pipeline(video_title):
    print(f"--- بدء معالجة فيديو: {video_title} ---")
    
    # 1. التخطيط بالذكاء الاصطناعي
    prompt = f"Create a structured JSON for a 30s video about: {video_title}. Style: Dark, minimalist, high-tech. Include 'script' and 'scenes' (with text and start/end times)."
    response = model.generate_content(prompt)
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    with open("video_data.json", "w") as f:
        f.write(clean_json)

    # 2. توليد الصوت
    data = json.loads(clean_json)
    communicate = edge_tts.Communicate(data['script'], "en-US-ChristopherNeural")
    await communicate.save("voiceover.mp3")
    
    # 3. تشغيل الرندر (نستخدم Manim عبر سطر الأوامر)
    # ملاحظة: سنستخدم سكريبت Manim خارجي أو مدمج
    os.system("manim -pql -r 1080,1920 render_engine.py VideoRenderer")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "How AI Works"
    asyncio.run(run_pipeline(title))
