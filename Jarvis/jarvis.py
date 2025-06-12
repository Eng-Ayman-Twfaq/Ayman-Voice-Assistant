# -*- coding: utf-8 -*-
import sys
import os
import json
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import random
import pyautogui
from gtts import gTTS
import tempfile
import time
import subprocess
import pygame
import urllib.parse6
import numpy as np
import psutil
from vosk import Model, KaldiRecognizer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLabel, QWidget, QComboBox,
                           QScrollArea, QFrame, QSystemTrayIcon, QMenu, QMessageBox,
                           QInputDialog, QLineEdit, QFileDialog, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import (QIcon, QPixmap, QColor, QFont, QTextCursor, QLinearGradient, 
                        QPainter, QPen, QBrush, QTextFormat, QTextCharFormat)
from PyQt5.QtWidgets import QStyle

# ==============================================
# الجزء الخاص بالمساعد الصوتي
# ==============================================

class ArabicAssistant:
    def play_listening_sound(self):
        try:
            # جرب تشغيل صوت من ملف
            pygame.mixer.Sound('beep.wav').play()
        except:
            # إذا لم يو جد الملف، استخدم صوت النظام
            try:
                import winsound
                winsound.Beep(1000, 300)  # صوت بيب بتردد 1000 هرتز لمدة 300 مللي ثانية
            except:
                # إذا فشل كل شيء، استخدم التحدث
                self.speak("بييب")
    def search_wikipedia(self, query):
        try:
            wikipedia.set_lang("ar")
            search_results = wikipedia.search(query)
            
            if not search_results:
                return "لم أجد نتائج عن هذا الموضوع في ويكيبيديا"
                
            page = wikipedia.page(search_results[0])
            summary = page.summary[:500] + "..." if len(page.summary) > 500 else page.summary
            return f"العنوان: {page.title}\n\n{summary}\n\nرابط المقال: {page.url}"
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return "حدث خطأ أثناء محاولة جلب المعلومات من ويكيبيديا"
    def __init__(self):
        pygame.mixer.init()
        self.engine = self.init_tts_engine()
        self.recognizer = self.init_speech_recognizer()
        self.setup_voice_parameters()
        # self.check_system_voices()
        self.app_paths = {
            'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'photoshop': 'C:/Program Files/Adobe/Adobe Photoshop 2023/Photoshop.exe',
            'notepad': 'notepad.exe'
        }
        self.conversation_context = []
        self.max_context_length = 5
        
        try:
            self.vosk_model = Model(lang="ar")
        except:
            self.vosk_model = None
            print("لم يتم تحميل نموذج Vosk، سيتم استخدام Google كبديل")

    def init_tts_engine(self):
        try:
            return pyttsx3.init()
        except Exception as e:
            print(f"خطأ في تهيئة محرك الصوت: {e}")
            return None
    
    def init_speech_recognizer(self):
        r = sr.Recognizer()
        r.pause_threshold = 0.8
        r.phrase_time_limit = 20
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        r.dynamic_energy_adjustment_damping = 0.15
        r.operation_timeout = 15
        return r
    
    def setup_voice_parameters(self):
        if self.engine:
            self.engine.setProperty('rate', 145)
            self.engine.setProperty('volume', 0.9)
            self.engine.setProperty('voice', self.find_best_voice())
    
    def find_best_voice(self):
        if not self.engine:
            return None
            
        voices = self.engine.getProperty('voices')
        arabic_voices = [
            'Lamees', 'Naayf', 'Arabic', 'ar-SA', 'ar-EG',
            'Microsoft Naayf', 'Microsoft Hoda'
        ]
        
        for voice in voices:
            if any(ar_voice.lower() in voice.name.lower() for ar_voice in arabic_voices):
                print(f"تم اختيار الصوت العربي: {voice.name}")
                return voice.id
        
        print("⚠ تحذير: لم يتم العثور على صوت عربي، سيستخدم الصوت الافتراضي")
        return voices[0].id if voices else None
    
    def speak(self, text):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if not self.has_arabic_voice():
                    self.speak_with_gtts(text)
                    return
                
                if self.engine:
                    self.engine.say(text)
                    self.engine.runAndWait()
                    return
                
            except Exception as e:
                print(f"محاولة {attempt+1} فشلت: {str(e)}")
                time.sleep(1)
        
        self.speak_with_system(text)
    
    def has_arabic_voice(self):
        if not self.engine:
            return False
        current_voice = self.engine.getProperty('voice')
        return 'arabic' in current_voice.lower() or 'ar-' in current_voice.lower()
    
    def speak_with_gtts(self, text):
        try:
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"ar_voice_{time.time_ns()}.mp3")
            
            tlds = ['com.eg', 'com.sa', 'com', 'co.uk']
            for tld in tlds:
                try:
                    tts = gTTS(text=text, lang='ar', tld=tld, slow=False)
                    tts.save(temp_file)
                    break
                except:
                    continue
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            try:
                os.remove(temp_file)
            except:
                pass
            
        except Exception as e:
            raise Exception(f"خطأ في gTTS: {e}")
    
    def speak_with_system(self, text):
        try:
            if os.name == 'nt':
                subprocess.Popen(['mshta', 'vbscript:Execute("CreateObject(""SAPI.SpVoice"").Speak(""' + text + '"")(window.close)"'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['spd-say', text], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"فشل جميع طرق التحدث: {e}")
            print(f"النص: {text}")
    
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"الوقت الحالي هو {current_time}"
    
    def get_date(self):
        months = {
            1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
            5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }
        now = datetime.datetime.now()
        return f"التاريخ الحالي هو {now.day} {months[now.month]} {now.year}"
    
    def greet_user(self):
        hour = datetime.datetime.now().hour
        
        if 5 <= hour < 12:
            greeting = "صباح الخير"
        elif 12 <= hour < 18:
            greeting = "مساء الخير"
        else:
            greeting = "مساء الخير"
        
        return f"{greeting}! أنا مساعدك الصوتي الذكي، كيف يمكنني مساعدتك اليوم؟"
    
    def take_command(self):
        with sr.Microphone() as source:
            print("\nجاري الاستماع...")
            
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=8, 
                    phrase_time_limit=15
                )
                
                print("جاري معالجة الصوت...")
                query = self.recognizer.recognize_google(audio, language='ar-EG')
                
                print(f"تم التعرف على: {query}")
                return query.lower()
            
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"خطأ في الخدمة: {e}")
                return None
            except Exception as e:
                print(f"خطأ غير متوقع: {e}")
                return None
    
    def search_wikipedia(self, query):
        try:
            wikipedia.set_lang("ar")
            search_results = wikipedia.search(query)
            
            if not search_results:
                return "لم أجد نتائج عن هذا الموضوع في ويكيبيديا"
                
            page = wikipedia.page(search_results[0])
            summary = page.summary[:500]
            cleaned_text = ' '.join(summary.split()[:100])
            return f"وفقاً لويكيبيديا:\n{cleaned_text}"
            
        except wikipedia.exceptions.PageError:
            return "لم أجد نتائج عن هذا الموضوع في ويكيبيديا"
        except wikipedia.exceptions.DisambiguationError as e:
            return "هناك عدة نتائج، الرجاء تحديد أكثر"
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return "حدث خطأ أثناء البحث"
    
    def open_website(self, url):
        try:
            wb.open(url)
            return f"تم فتح الموقع {url}"
        except Exception as e:
            print(f"خطأ في فتح الموقع: {e}")
            return "عذراً، لم أستطع فتح الموقع"
    
    def play_random_music(self):
        music_dirs = [
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/Downloads"),
            "C:/Music"
        ]
        
        for dir_path in music_dirs:
            if os.path.exists(dir_path):
                songs = [f for f in os.listdir(dir_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
                if songs:
                    song = random.choice(songs)
                    os.startfile(os.path.join(dir_path, song))
                    return f"جاري تشغيل {os.path.splitext(song)[0]}"
        
        return "لم أجد أي ملفات موسيقى في المجلدات المعتادة"
    
    def take_screenshot(self):
        try:
            screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
            
            img = pyautogui.screenshot()
            img.save(filename)
            return f"تم حفظ لقطة الشاشة في {filename}"
        except Exception as e:
            print(f"خطأ في لقطة الشاشة: {e}")
            return "حدث خطأ أثناء أخذ لقطة الشاشة"
    
    def tell_joke(self):
        arabic_jokes = [
            "لمبة لم تشتغل لماذا ؟ لايوجد لديها شهادة",
            "ماذا قال البحر للشاطئ؟ خلاص تعبت.. جيت أموج",
            "لماذا لا يلعب السمك كرة القدم؟ لأنهم خايفين من الشباك!"
        ]
        return random.choice(arabic_jokes)
    
    def open_application(self, app_name):
        try:
            app_key = app_name.lower()
            if app_key in self.app_paths:
                subprocess.Popen(self.app_paths[app_key])
                return f"تم فتح {app_name}"
            else:
                return f"عفواً، التطبيق {app_name} غير مسجل في النظام"
        except Exception as e:
            print(f"خطأ في فتح التطبيق: {e}")
            return f"حدث خطأ أثناء محاولة فتح {app_name}"

    def search_google(self, query):
        try:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            wb.open(search_url)
            return f"جاري البحث في جوجل عن: {query}"
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return "عذراً، لم أستطع إجراء البحث"

    def search_youtube(self, query):
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            wb.open(search_url)
            return f"جاري البحث في يوتيوب عن: {query}"
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return "عذراً، لم أستطع إجراء البحث على يوتيوب"

# ==============================================
# الجزء الخاص بالواجهة الرسومية المطورة
# ==============================================

class ListenThread(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self._is_running = True
    
    def run(self):
        try:
            command = self.assistant.take_command()
            if command and self._is_running:
                self.finished_signal.emit(command)
            elif not command and self._is_running:
                self.error_signal.emit("لم يتم التعرف على الكلام")
        except Exception as e:
            self.error_signal.emit(f"خطأ: {str(e)}")
    
    def stop(self):
        self._is_running = False
        self.terminate()

class VoiceAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = ArabicAssistant()
        self.is_listening = False
        self.current_action = None
        self.init_ui()
        self.setup_tray_icon()
        self.setup_animations()
        
    def init_ui(self):
        self.setWindowTitle("المساعد الذكي - الإصدار المتميز")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_colors()
        self.setup_fonts()
        self.create_widgets()
        self.setup_layout()
        self.setup_style_sheet()
        self.greet_user()

    def setup_colors(self):
        self.primary_color = QColor(58, 150, 221)  # أزرق
        self.secondary_color = QColor(147, 112, 219)  # بنفسجي
        self.background_color = QColor(25, 25, 35)  # خلفية داكنة
        self.text_color = QColor(240, 240, 240)  # نص أبيض
        self.highlight_color = QColor(255, 193, 7)  # لون تمييز
        self.error_color = QColor(231, 76, 60)  # أحمر للخطأ
        self.success_color = QColor(46, 204, 113)  # أخضر للنجاح
        self.user_bubble = QColor(30, 144, 255)  # أزرق لفقاعات المستخدم
        self.assistant_bubble = QColor(138, 43, 226)  # بنفسجي لفقاعات 

    def setup_fonts(self):
        self.arabic_font = QFont("Arial", 12)
        self.arabic_font.setBold(True)
        self.title_font = QFont("Arial", 20, QFont.Bold)
        self.status_font = QFont("Arial", 10)

    def create_widgets(self):
        # شريط العنوان
        self.header = QLabel("المساعد الصوتي الذكي")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(self.title_font)
        self.header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.primary_color.name()}, stop:1 {self.secondary_color.name()});
            color: white;
            padding: 15px;
            border-radius: 10px;
        """)

        # منطقة المحادثة
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setFont(self.arabic_font)
        self.conversation_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.background_color.name()};
                color: {self.text_color.name()};
                border: 2px solid {self.primary_color.name()};
                border-radius: 15px;
                padding: 15px;
            }}
        """)

        # زر الميكروفون الرئيسي
        self.mic_button = QPushButton("🎤 اضغط للتحدث")
        self.mic_button.setFixedSize(200, 200)
        self.mic_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.mic_button.setStyleSheet(f"""
            QPushButton {{
                background: radial-gradient(circle, {self.primary_color.name()}, {self.secondary_color.name()});
                color: white;
                border-radius: 100px;
                border: 3px solid {self.highlight_color.name()};
            }}
            QPushButton:hover {{
                background: radial-gradient(circle, {self.secondary_color.name()}, {self.primary_color.name()});
            }}
        """)
        self.mic_button.clicked.connect(self.toggle_listening)

        # مؤشر الحالة
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(20, 20)
        self.status_indicator.setStyleSheet(f"""
            background-color: gray;
            border-radius: 10px;
            border: 2px solid white;
        """)

        self.status_label = QLabel("جاهز")
        self.status_label.setFont(self.status_font)
        self.status_label.setStyleSheet(f"color: {self.text_color.name()};")

        # قائمة الأوامر السريعة
        self.quick_commands = QComboBox()
        self.quick_commands.addItems([
            "أوامر سريعة",
            "الوقت الحالي",
            "تاريخ اليوم",
            "ابحث في ويكيبيديا",
            "افتح يوتيوب",
            "افتح جوجل",
            "تشغيل الموسيقى",
            "لقطة الشاشة",
            "نكتة عربية",
            "من نحن"
        ])
        self.quick_commands.setStyleSheet("""
    QComboBox {
        color: white;                 /* لون النص */
        background-color: #333333;    /* لون الخلفية الداكن */
        border: 1px solid #555;      /* إطار */
        border-radius: 5px;           /* زوايا مدورة */
        padding: 5px;
    }
    QComboBox QAbstractItemView {
        color: white;                /* لون النص في القائمة المنسدلة */
        background-color: #444;      /* خلفية القائمة المنسدلة */
    }
    QComboBox::drop-down {
        border: none;                /* إزالة الحدود من زر السهم */
    }
""")
        self.quick_commands.setFont(self.arabic_font)
        self.quick_commands.currentIndexChanged.connect(self.execute_quick_command)

        # أزرار القائمة السفلية
        self.create_footer_buttons()

    def create_footer_buttons(self):
        self.footer = QWidget()
        footer_layout = QHBoxLayout()
        
        buttons = [
            ("الإعدادات", "⚙️", self.show_settings),
            ("المساعدة", "❓", self.show_help),
            ("خروج", "🚪", self.close_app)
        ]
        
        for text, icon, handler in buttons:
            btn = QPushButton(f"{icon} {text}")
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {self.primary_color.name()}, stop:1 {self.secondary_color.name()});
                    color: white;
                    border-radius: 10px;
                    padding: 8px 15px;
                    margin: 0 5px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {self.secondary_color.name()}, stop:1 {self.primary_color.name()});
                }}
            """)
            btn.clicked.connect(handler)
            footer_layout.addWidget(btn)
        
        footer_layout.addStretch()
        self.footer.setLayout(footer_layout)

    def setup_layout(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # إضافة شريط العنوان
        main_layout.addWidget(self.header)
        
        # إضافة منطقة المحادثة
        main_layout.addWidget(self.conversation_display)
        
        # لوحة التحكم المركزية
        control_layout = QHBoxLayout()
        
        # اللوحة اليسرى (مؤشر الحالة)
        left_panel = QVBoxLayout()

        status_label = QLabel("حالة النظام:")
        status_label.setStyleSheet("color: white;")  # تغيير لون النص إلى أبيض

        left_panel.addWidget(status_label)
        left_panel.addWidget(self.status_indicator)
        left_panel.addWidget(self.status_label)
        left_panel.addStretch()
        
        # اللوحة اليمنى (الأوامر السريعة)
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("الأوامر السريعة:")) 
        right_panel.addWidget(self.quick_commands)
        right_panel.addStretch()
        
        # إضافة اللوحات الجانبية وزر الميكروفون
        control_layout.addLayout(left_panel)
        control_layout.addWidget(self.mic_button)
        control_layout.addLayout(right_panel)
        
        # إضافة لوحة التحكم إلى التخطيط الرئيسي
        main_layout.addLayout(control_layout)
        
        # إضافة القائمة السفلية
        main_layout.addWidget(self.footer)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_style_sheet(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.background_color.name()};
            }}
            QComboBox {{
                background-color: {self.primary_color.name()};
                color: white;
                border-radius: 10px;
                padding: 5px;
                min-width: 200px;
                font-size: 14px;
            }}
            QScrollBar:vertical {{
                width: 12px;
                background: {self.background_color.name()};
            }}
            QScrollBar::handle:vertical {{
                background: {self.primary_color.name()};
                min-height: 20px;
                border-radius: 6px;
            }}
        """)

    def setup_animations(self):
        # Pulsing animation for status indicator
        self.pulse_animation = QPropertyAnimation(self.status_indicator, b"geometry")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setStartValue(self.status_indicator.geometry())
        self.pulse_animation.setEndValue(self.status_indicator.geometry().adjusted(-2, -2, 4, 4))
        self.pulse_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.is_listening = True
        self.mic_button.setText("🎤 جاري الاستماع...")
        self.update_status("listening")
        
        # التحقق قبل تشغيل الصوت
        if hasattr(self.assistant, 'play_listening_sound'):
            self.assistant.play_listening_sound()
        
        self.listen_thread = ListenThread(self.assistant)
        self.listen_thread.finished_signal.connect(self.handle_command)
        self.listen_thread.error_signal.connect(self.show_error)
        self.listen_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.mic_button.setText("🎤 اضغط للتحدث")
        self.update_status("idle")
        
        if hasattr(self, 'listen_thread'):
            self.listen_thread.stop()

    def update_status(self, state):
        color_map = {
            "idle": "gray",
            "listening": self.primary_color.name(),
            "processing": self.secondary_color.name(),
            "error": self.error_color.name(),
            "success": self.success_color.name()
        }
        
        text_map = {
            "idle": "جاهز",
            "listening": "جاري الاستماع...",
            "processing": "جاري المعالجة...",
            "error": "خطأ!",
            "success": "تم بنجاح"
        }
        
        self.status_indicator.setStyleSheet(f"""
            background-color: {color_map[state]};
            border-radius: 10px;
            border: 2px solid white;
        """)
        self.status_label.setText(text_map[state])
        
        if state == "listening":
            self.pulse_animation.start()
        else:
            self.pulse_animation.stop()

    def add_message(self, sender, message, msg_type):
        cursor = self.conversation_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        bubble_color = self.assistant_bubble.name() if msg_type == "assistant" else self.user_bubble.name()
        text_color = "white"
        align = "left" if msg_type == "user" else "right"
        
        html = f"""
        <div style='margin:10px; text-align:{align}; direction:rtl;'>
            <div style='
                background: {bubble_color};
                color: {text_color};
                border-radius: 15px;
                padding: 8px 15px;
                display: inline-block;
                max-width: 80%;
                margin-{'right' if align == 'right' else 'left'}: 10px;
            '>
                <div style='font-size:0.8em; color:#eee;'>{timestamp}</div>
                <div><b>{sender}:</b> {message}</div>
            </div>
        </div>
        """
        self.conversation_display.insertHtml(html)
        self.conversation_display.ensureCursorVisible()
        
        # Scroll to bottom
        scroll_bar = self.conversation_display.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def handle_command(self, command):
        if not command:
            return
            
        self.add_message("أنت", command, "user")
        self.update_status("processing")
        
        response = ""
        
        # حالة البحث في يوتيوب
        if self.current_action == "youtube_search":
            search_query = command
            encoded_query = urllib.parse.quote_plus(search_query)
            wb.open(f"https://www.youtube.com/results?search_query={encoded_query}")
            response = f"جاري البحث في يوتيوب عن: {search_query} 🎬"
            self.current_action = None
            
        # حالة البحث في جوجل
        elif self.current_action == "google_search":
            search_query = command
            encoded_query = urllib.parse.quote_plus(search_query)
            wb.open(f"https://www.google.com/search?q={encoded_query}")
            response = f"جاري البحث في جوجل عن: {search_query} 🔍"
            self.current_action = None
            
        # حالة البحث في ويكيبيديا
        elif self.current_action == "wikipedia_search":
            try:
                result = self.assistant.search_wikipedia(command)
                response = f"وفقاً لويكيبيديا:\n{result} 📚"
                self.current_action = None
            except Exception as e:
                response = "حدث خطأ أثناء البحث، الرجاء المحاولة مرة أخرى"
        
        # الأوامر العادية (غير البحث)
        elif any(word in command for word in ["الوقت", "الساعة"]):
            response = self.assistant.get_time()
            
        elif any(word in command for word in ["التاريخ", "اليوم"]):
            response = self.assistant.get_date()
            
        elif "افتح جوجل" in command:
            self.current_action = "google_search"
            wb.open("https://google.com")
            response = "ماذا تريد أن تبحث في جوجل؟ انتظر صوت التنبيه ثم قل كلمة البحث 🎤"
            
        elif "افتح يوتيوب" in command:
            self.current_action = "youtube_search"
            wb.open("https://youtube.com")
            response = "ماذا تريد أن تبحث في يوتيوب؟ رجاءً قل كلمة البحث بعد الصفير... 🔊"
            
        elif "ابحث في ويكيبيديا" in command:
            self.current_action = "wikipedia_search"
            response = "قل لي الموضوع الذي تريد البحث عنه في ويكيبيديا، سأستمع لك الآن..."
            
        elif "شغل موسيقى" in command or "تشغيل الموسيقى" in command:
            response = self.assistant.play_random_music()
            
        elif "لقطة شاشة" in command or "سكرين شوت" in command:
            response = self.assistant.take_screenshot()
            
        elif "نكتة" in command or "اضحكني" in command:
            response = self.assistant.tell_joke()
            
        elif "من برمجك" in command:
           response = " تم برمجتي من قبل المطور : أيمن توفيق،    "
            
        elif any(word in command for word in ["توقف", "اخرج", "ايقاف"]):
            response = "مع السلامة، أراك لاحقاً!"
            self.add_message("المساعد", response, "assistant")
            self.assistant.speak(response)
            QTimer.singleShot(1000, self.close_app)
            return
            
        else:
            response = "عذراً، لم أفهم الأمر. هل يمكنك تكراره؟"
        
        self.add_message("المساعد", response, "assistant")
        self.assistant.speak(response)
        self.update_status("success")
        QTimer.singleShot(2000, lambda: self.update_status("idle"))

    def execute_quick_command(self, index):
        if index == 0:  # العنصر الأول هو "أوامر سريعة"
            return
            
        command = self.quick_commands.currentText()
        self.quick_commands.setCurrentIndex(0)
        
        # إضافة أمر المستخدم إلى المحادثة
        self.add_message("أنت", f"تشغيل: {command}", "user")
        
        if command == "الوقت الحالي":
            response = self.assistant.get_time()
        elif command == "تاريخ اليوم":
            response = self.assistant.get_date()
        elif command == "ابحث في ويكيبيديا":
            self.current_action = "wikipedia_search"
            response = "قل لي الموضوع الذي تريد البحث عنه في ويكيبيديا"
        elif command == "افتح يوتيوب":
            self.current_action = "youtube_search"
            wb.open("https://youtube.com")
            response = "ماذا تريد أن تبحث في يوتيوب؟"
        elif command == "افتح جوجل":
            self.current_action = "google_search"
            wb.open("https://google.com")
            response = "ماذا تريد أن تبحث في جوجل؟"
            
        elif command == "تشغيل الموسيقى":
            response = self.assistant.play_random_music()
            self.add_message("المساعد", response, "assistant")
            self.assistant.speak(response)
            
        elif command == "لقطة الشاشة":
            response = self.assistant.take_screenshot()
            self._message("المساعد", response, "assistant")
            self.assistant.speak(response)
            
        elif command == "نكتة عربية":
            response = self.assistant.tell_joke()
            self.add_message("المساعد", response, "assistant")
            self.assistant.speak(response)
            
        elif command == "من برمجك":
            response = " تم برمجتي من قبل المطور : أيمن توفيق،    "
            self.add_message("المساعد", response, "assistant")
            self.assistant.speak(response)


        self.add_message("المساعد", response, "assistant")
        self.assistant.speak(response)

    def show_error(self, error_msg):
        self.add_message("النظام", error_msg, "error")
        self.update_status("error")
        QTimer.singleShot(2000, lambda: self.update_status("idle"))

    def show_settings(self):
        settings_dialog = QMessageBox(self)
        settings_dialog.setWindowTitle("إعدادات المساعد")
        settings_dialog.setText("إعدادات المساعد الصوتي:")
        settings_dialog.setInformativeText("""
        <ul>
            <li>سرعة الصوت: متوسطة</li>
            <li>نوع الصوت: عربي</li>
            <li>حساسية الميكروفون: عالية</li>
        </ul>
        <p>سيتم إضافة المزيد من الخيارات في التحديثات القادمة</p>
        """)
        settings_dialog.setStandardButtons(QMessageBox.Ok)
        settings_dialog.exec_()

    def show_help(self):
        help_dialog = QMessageBox(self)
        help_dialog.setWindowTitle("مساعدة المساعد الصوتي")
        help_dialog.setText("كيفية استخدام المساعد الصوتي العربي:")
        help_dialog.setInformativeText("""
        <h3>الأوامز المتاحة:</h3>
        <ul>
            <li><b>الوقت/الساعة:</b> معرفة الوقت الحالي</li>
            <li><b>التاريخ/اليوم:</b> معرفة تاريخ اليوم</li>
            <li><b>ابحث في ويكيبيديا عن [موضوع]:</b> البحث في الموسوعة</li>
            <li><b>افتح يوتيوب/جوجل:</b> فتح المواقع الشهيرة</li>
            <li><b>شغل موسيقى:</b> تشغيل موسيقى عشوائية</li>
            <li><b>خذ لقطة شاشة:</b> حفظ صورة للشاشة</li>
            <li><b>قل نكتة:</b> سماع نكتة عربية</li>
            <li><b>من نحن:</b> معلومات عن المطورين</li>
            <li><b>توقف/اخرج:</b> إغلاق المساعد</li>
        </ul>
        """)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.exec_()

    def greet_user(self):
        greeting = self.assistant.greet_user()
        self.add_message("المساعد", greeting, "assistant")
        self.assistant.speak(greeting)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("إظهار النافذة")
        exit_action = tray_menu.addAction("خروج")
        
        show_action.triggered.connect(self.show_normal)
        exit_action.triggered.connect(self.close_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_clicked)

    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()

    def show_normal(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def close_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "المساعد الصوتي",
            "يعمل المساعد في الخلفية، انقر نقرًا مزدوجًا لعرض النافذة",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # تحميل ملف الأنيميشن
    app.setStyleSheet("""
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    """)
    
    window = VoiceAssistantGUI()
    window.show()
    sys.exit(app.exec_())
