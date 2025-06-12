# 🎙️ المساعد الصوتي العربي | Ayman Voice Assistant

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with PyQt5](https://img.shields.io/badge/UI-PyQt5-blueviolet)](https://pypi.org/project/PyQt5/)
[![Voice Recognition](https://img.shields.io/badge/Speech-Recognition-orange)](https://pypi.org/project/SpeechRecognition/)

مساعد صوتي ذكي باللغة العربية بواجهة رسومية مبنية باستخدام PyQt5، يدعم تنفيذ أوامر صوتية طبيعية مثل البحث، عرض الوقت والتاريخ، تشغيل الموسيقى، والتفاعل النصي/الصوتي مع المستخدم.

---

## 🖼️ لمحة سريعة

> *(أضف صورة GIF أو Screenshot من التطبيق هنا)*  
> ![demo](ayman.jfif)

---

## ⚙️ المزايا الرئيسية

✅ واجهة رسومية عربية أنيقة باستخدام PyQt5  
✅ دعم الأوامر الصوتية باللغة العربية  
✅ البحث في Google وYouTube وWikipedia  
✅ إظهار الوقت والتاريخ  
✅ دعم "System Tray" لتشغيل المساعد في الخلفية  
✅ مؤثرات بصرية وصوتية تفاعلية  
✅ دعم الأوامر السريعة من قائمة منسدلة

---

## 📦 متطلبات التشغيل

- Python 3.7 أو أحدث
- نظام يدعم الميكروفون ومكبرات الصوت
- الحزم التالية:

```bash
PyQt5
SpeechRecognition
pyttsx3
wikipedia
pyaudio
🚀 خطوات التشغيل
1. استنساخ المستودع
bash
Copy
Edit
git clone https://github.com/Eng-Ayman-Twfaq/Ayman-Voice-Assistant.git
cd arabic-voice-assistant
2. إنشاء وتفعيل البيئة الافتراضية (Virtual Environment)
⬢ على Windows:
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
🐧 على Linux / macOS:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. تثبيت المتطلبات
bash
Copy
Edit
pip install -r requirements.txt
إذا لم يعمل PyAudio مباشرة، نفّذ التالي على Windows:

bash
Copy
Edit
pip install pipwin
pipwin install pyaudio
4. تشغيل التطبيق
bash
Copy
Edit
python main.py
🎤 الأوامر الصوتية المدعومة
الأمر	الوظيفة
ما الوقت / كم الساعة	إظهار الوقت الحالي
ما التاريخ / ما اليوم	إظهار تاريخ اليوم
افتح جوجل	فتح موقع Google والانتظار لكلمة البحث
افتح يوتيوب	فتح موقع YouTube والانتظار لكلمة البحث
ابحث في ويكيبيديا عن [موضوع]	جلب ملخص من ويكيبيديا
شغل موسيقى / تشغيل الموسيقى	تشغيل مقطع موسيقي عشوائي
لقطة شاشة / سكرين شوت	أخذ لقطة للشاشة وحفظها
قل نكتة / نكتة عربية	سماع نكتة عربية
من برمجك؟	عرض اسم المطور
توقف / اخرج / إيقاف	إنهاء عمل البرنامج

📂 هيكلية الملفات
bash
Copy
Edit
📦 arabic-voice-assistant
├── main.py                # ملف التشغيل الرئيسي
├── assistant.py           # منطق الذكاء الصوتي
├── assets/                # صور وأصوات إضافية
├── screenshots/           # لقطات توضيحية
├── requirements.txt       # قائمة المتطلبات
└── README.md              # هذا الملف
👨‍💻 المطور
الاسم: أيمن توفيق

الهدف: تعزيز تجربة التفاعل الصوتي باللغة العربية

اللغة: العربية الفصحى 🇸🇦

📧 للتواصل: (أضف وسيلة تواصل إن أردت)

📄 الترخيص
تم إصدار هذا المشروع بموجب ترخيص MIT.
راجع LICENSE للمزيد من التفاصيل.

⭐ ساهم بدعمك
إذا أعجبك المشروع، لا تنسَ دعمي بنجمة ⭐
وأهلاً بمساهماتك واقتراحاتك لتطويره 🔧