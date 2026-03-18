import os
import json
import asyncio
import edge_tts
from google import genai
from google.genai import types
import sys

# إعداد العميل الجديد (SDK 2026)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def run_pipeline(video_title):
    print(f"--- [START] Processing: {video_title} ---")
    
    prompt = f"""
    Create a video script and scene timing for a 30s video: '{video_title}'.
    Requirements:
    - High-impact educational content.
    - Output must be valid JSON only.
    - 'script' field: text for voiceover.
    - 'scenes' field: list of objects with 'text', 'start_time', 'end_time', and 'icon'.
    """

    # إجبار النموذج على إخراج JSON فقط عبر الـ Schema
    response = client.models.generate_content(
        model='gemini-2.5-flash', # استخدم الإصدار الأحدث المستقر
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
        ),
    )

    try:
        data = json.loads(response.text)
        # التأكد من وجود المفاتيح المطلوبة
        if 'script' not in data:
            raise KeyError("Gemini missed the 'script' key.")
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw Response: {response.text}")
        return

    # حفظ ملف البيانات للمرحلة التالية
    with open("video_data.json", "w") as f:
        json.dump(data, f)

    # توليد الصوت
    print("[+] Generating Audio...")
    communicate = edge_tts.Communicate(data['script'], "en-US-ChristopherNeural")
    await communicate.save("voiceover.mp3")
    
    # تشغيل الرندر (تأكد أن ملف render_engine.py موجود)
    print("[+] Starting Render Engine...")
    os.system("manim -pqh -r 1080,1920 render_engine.py VideoRenderer")
    print("--- [FINISHED] ---")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Technology"
    asyncio.run(run_pipeline(title))
