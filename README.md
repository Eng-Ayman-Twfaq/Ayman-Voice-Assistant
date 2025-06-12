# 🧠 Ayman Voice Assistant - المساعد الصوتي العربي 🎤🇸🇦

<p align="center">
  <img src="assets/icon.png" width="180" alt="Arabic Voice Assistant"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/UI-PyQt5-blueviolet" alt="PyQt5 UI">
  <img src="https://img.shields.io/badge/Speech-Recognition-orange" alt="Speech Recognition">
</p>

## 📝 نظرة عامة

**المساعد الصوتي العربي** هو تطبيق ذكي بواجهة رسومية مبنية باستخدام مكتبة **PyQt5**، يتيح للمستخدم التفاعل الطبيعي عبر الصوت باللغة العربية الفصحى. يدعم تنفيذ مجموعة من الأوامر الشائعة مثل:

- 📅 عرض الوقت والتاريخ  
- 🔍 البحث في Google، YouTube، Wikipedia  
- 🎶 تشغيل الموسيقى  
- 🖼️ التقاط لقطة شاشة  
- 😂 إلقاء نكتة  
- 👨‍💻 الإجابة عن أسئلة عامة  

تم تصميمه لتعزيز تجربة التفاعل بين الإنسان والحاسوب باللغة العربية بشكل سلس وبسيط.  
يعمل بكفاءة على أنظمة Windows وLinux وmacOS.

> 🎯 هدف المشروع: توفير تجربة صوتية عربية طبيعية باستخدام تقنيات الذكاء الاصطناعي مفتوحة المصدر.

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

## 🚀 خطوات التشغيل

### 1. استنساخ المستودع
```bash
git clone https://github.com/Eng-Ayman-Twfaq/Ayman-Voice-Assistant.git
cd arabic-voice-assistant
```

### 2. إنشاء وتفعيل البيئة الافتراضية (Virtual Environment)

#### ⬢ على Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 على Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

#### 🔧 ملاحظة حول PyAudio على Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

### 4. تشغيل التطبيق
```bash
python main.py
```

---

## 🎤 الأوامر الصوتية المدعومة

| الأمر                          | الوظيفة                                     |
|-------------------------------|----------------------------------------------|
| ما الوقت / كم الساعة           | عرض الوقت الحالي                             |
| ما التاريخ / ما اليوم          | عرض تاريخ اليوم                              |
| افتح جوجل                     | فتح Google والانتظار لكلمة البحث             |
| افتح يوتيوب                   | فتح YouTube والانتظار لكلمة البحث            |
| ابحث في ويكيبيديا عن [موضوع]  | جلب ملخص من ويكيبيديا                        |
| شغل موسيقى / تشغيل الموسيقى  | تشغيل مقطع موسيقي عشوائي                     |
| لقطة شاشة / سكرين شوت        | أخذ لقطة للشاشة                              |
| قل نكتة / نكتة عربية          | سماع نكتة عربية                              |
| من برمجك؟                    | عرض اسم المطور                               |
| توقف / اخرج / إيقاف          | إغلاق التطبيق                                |

---

## 📂 هيكلية الملفات

```
📦 arabic-voice-assistant
├── main.py                # ملف التشغيل الرئيسي
├── assistant.py           # منطق الذكاء الصوتي
├── assets/                # صور وأصوات إضافية
├── screenshots/           # لقطات توضيحية
├── requirements.txt       # قائمة المتطلبات
└── README.md              # هذا الملف
```

---

## 📦 المتطلبات

```bash
PyQt5
SpeechRecognition
pyttsx3
wikipedia
pyaudio
```

---

## 👨‍💻 المطور

تم تطوير هذا المشروع بواسطة:

<p align="center"> <a href="https://github.com/Eng-Ayman-Twfaq"> <img src="https://img.shields.io/badge/GitHub-Eng__Ayman__Twfaq-181717?style=for-the-badge&logo=github" alt="GitHub Profile"/> </a> <a href="mailto:ayman.tawfaq.developers@gmail.com"> <img src="https://img.shields.io/badge/Email-ayman.tawfaq.developers%40gmail.com-D14836?style=for-the-badge&logo=gmail" alt="Email"/> </a> <a href="https://wa.me/967770883615"> <img src="https://img.shields.io/badge/WhatsApp-%2B967770883615-25D366?style=for-the-badge&logo=whatsapp" alt="WhatsApp"/> </a> </p>
🌟 دعم المشروع
<p align="center"> <img src="https://img.shields.io/github/stars/Eng-Ayman-Twfaq/Human-Follower-Robot?style=social" alt="Stars"/> <img src="https://img.shields.io/github/followers/Eng-Ayman-Twfaq?style=social" alt="Followers"/> </p>
إذا أعجبك المشروع:

⭐ اضغط على زر Star لدعمه

👁️ تابع المطور على GitHub

📢 شاركه مع المهتمين بالروبوتات والمشاريع التعليمية

🚀 مشاريع قادمة
تابعنا على GitHub لمشاهدة المزيد من المشاريع المستقبلية 👇

<p align="center"> <a href="https://github.com/Eng-Ayman-Twfaq"> <img src="https://img.shields.io/badge/VIEW_MORE_PROJECTS-181717?style=for-the-badge&logo=github" alt="More Projects"/> </a> </p>