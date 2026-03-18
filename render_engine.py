from manim import *
import json
import os

class VideoRenderer(Scene):
    def construct(self):
        # 1. تحميل البيانات الناتجة من Gemini
        with open("video_data.json", "r") as f:
            data = json.load(f)

        # 2. إعدادات الصوت
        self.add_sound("voiceover.mp3")
        
        # 3. معالجة المشاهد ديناميكياً
        for i, scene in enumerate(data['scenes']):
            # إنشاء النص مع تأثير "Glow" بسيط
            text_val = scene['text'].upper()
            display_text = Text(text_val, font="Sans", weight=BOLD, font_size=55)
            display_text.set_color_by_gradient(BLUE_B, WHITE)
            
            # محاكاة الأيقونات (يمكنك استبدالها بـ SVGMobject إذا رفعت أيقوناتك)
            icon_circle = Circle(radius=1.2, color=BLUE_D, fill_opacity=0.2)
            icon_label = Text(scene.get('icon', '💡')[:1], font_size=60) # يأخذ أول حرف أو إيموجي
            icon_group = VGroup(icon_circle, icon_label).next_to(display_text, UP, buff=0.8)

            full_scene = VGroup(icon_group, display_text).center()

            # --- التوقيت الذكي ---
            start = scene['start_time']
            end = scene['end_time']
            duration = end - start

            # تأثير الظهور (Pop-up)
            self.play(
                Create(icon_circle),
                Write(display_text),
                FadeIn(icon_label, scale=0.5),
                run_time=min(1.0, duration * 0.3)
            )
            
            # البقاء نشطاً بناءً على توقيت Gemini
            self.wait(max(0.1, duration - 1.5))

            # تأثير الخروج (Fade out)
            self.play(
                FadeOut(full_scene, shift=DOWN * 0.5),
                run_time=0.5
            )

        # نهاية الفيديو
        logo = Text("CREATED BY AI", font_size=24, color=GRAY).to_edge(DOWN)
        self.play(FadeIn(logo))
        self.wait(1)
