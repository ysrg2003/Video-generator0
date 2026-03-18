from manim import *
import json
import os

class VideoRenderer(Scene):
    def construct(self):
        # 1. تحميل البيانات
        if not os.path.exists("video_data.json"):
            return
            
        with open("video_data.json", "r") as f:
            data = json.load(f)

        # 2. إعداد الصوت
        if os.path.exists("voiceover.mp3"):
            self.add_sound("voiceover.mp3")
        
        # 3. معالجة المشاهد
        for i, scene in enumerate(data['scenes']):
            # --- التحويل البرمجي للأرقام لضمان عدم حدوث TypeError ---
            try:
                start = float(scene['start_time'])
                end = float(scene['end_time'])
            except (ValueError, KeyError):
                continue # تخطي المشهد إذا كانت البيانات تالفة

            duration = end - start
            if duration <= 0: continue

            # إنشاء العناصر البصرية
            text_val = scene['text'].upper()
            display_text = Text(text_val, font="Sans", weight=BOLD, font_size=50)
            display_text.set_color_by_gradient(BLUE_B, WHITE)
            
            icon_label = Text(scene.get('icon', '💡')[:1], font_size=60)
            full_scene = VGroup(icon_label, display_text).arrange(DOWN, buff=0.5).center()

            # تأثير الظهور
            self.play(
                FadeIn(full_scene, scale=0.8),
                run_time=min(0.8, duration * 0.4)
            )
            
            # وقت الانتظار
            self.wait(max(0.1, duration - 1.2))

            # تأثير الخروج
            self.play(
                FadeOut(full_scene, shift=DOWN * 0.3),
                run_time=0.4
            )

        # شعار النهاية
        logo = Text("AI GENERATED", font_size=20, color=GRAY).to_edge(DOWN)
        self.add(logo)
        self.wait(1)
