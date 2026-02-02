# 🎓 Smart Video Learning Tool

## 📌 Project Overview

**Smart Video Learning Tool** एक AI-powered educational application है जो किसी भी YouTube educational video को complete study material में convert कर देता है।

### ✨ Features

✅ **YouTube Transcript Extraction** - Automatically video का transcript निकाले  
✅ **AI-Powered Summary** - Video का concise summary generate करे  
✅ **Key Learning Points** - Important points और notes निकाले  
✅ **Auto Quiz Generation** - Video content से exactly 10 MCQ questions बनाए  
✅ **Beautiful UI** - User-friendly Streamlit interface  

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web UI framework
- **YouTube Transcript API** - Transcript extraction
- **Google Gemini AI** - Content generation (Summary, Key Points, Quiz)
- **python-dotenv** - Environment variable management

---

## 📋 Prerequisites

1. Python 3.8 या उससे ऊपर installed होना चाहिए
2. Google Gemini API Key (Free)
3. Internet connection

---

## 🚀 Installation & Setup

### Step 1: Clone या Download करें

```bash
cd SmartVideoLearningTool
```

### Step 2: Virtual Environment बनाएं (Recommended)

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Dependencies Install करें

```bash
pip install -r requirements.txt
```

### Step 4: Google Gemini API Key Setup

1. **API Key प्राप्त करें:**
   - Visit: https://makersuite.google.com/app/apikey
   - Google account से login करें
   - "Create API Key" पर click करें
   - API key copy करें

2. **`.env` file में API key डालें:**
   
   `.env` file खोलें और अपनी API key paste करें:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Step 5: Application Run करें

```bash
streamlit run app.py
```

Application browser में automatically खुल जाएगा: `http://localhost:8501`

---

## 📖 How to Use

1. **YouTube Video Link डालें**
   - किसी भी educational YouTube video का link paste करें
   - ध्यान दें: Video में subtitles/captions enabled होने चाहिए

2. **"Generate Learning Material" button click करें**

3. **Results देखें:**
   - **📝 Summary Tab** - Video का AI-generated summary
   - **🎯 Key Points Tab** - Main learning points
   - **📊 Quiz Tab** - 10 MCQ questions
   - **📄 Full Transcript Tab** - Complete video transcript

---

## 📂 Project Structure

```
SmartVideoLearningTool/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (DO NOT SHARE)
├── .env.example          # Environment template
├── .gitignore            # Git ignore file
└── README.md             # This file
```

---

## 🎯 Key Functions

### 1. `extract_video_id(youtube_url)`
YouTube URL से video ID निकालता है

### 2. `get_transcript(video_id)`
YouTube video का transcript extract करता है

### 3. `generate_summary(transcript)`
Google Gemini AI से summary generate करता है

### 4. `generate_key_points(transcript)`
Important learning points निकालता है

### 5. `generate_quiz(transcript)`
Exactly 10 MCQ questions बनाता है

---

## ⚠️ Important Notes

1. **API Key Security:**
   - `.env` file को कभी भी publicly share न करें
   - Git repository में commit न करें

2. **Video Requirements:**
   - Video में subtitles/captions होने चाहिए
   - Hindi या English captions support करता है

3. **API Limits:**
   - Google Gemini free tier daily limits apply होती हैं
   - बहुत सारे requests एक साथ न करें

---

## 🐛 Troubleshooting

### Problem: "Could not extract transcript"
**Solution:** Video में captions enabled हैं या नहीं check करें

### Problem: "Google API Key not found"
**Solution:** `.env` file में valid API key है या नहीं check करें

### Problem: Streamlit नहीं चल रहा
**Solution:** 
```bash
pip install --upgrade streamlit
streamlit run app.py
```

---

## 🎓 Learning Outcomes

इस project से आप सीखेंगे:

- ✅ Streamlit web apps बनाना
- ✅ YouTube APIs का use करना
- ✅ Google Gemini AI integration
- ✅ Environment variables management
- ✅ AI-powered content generation
- ✅ Modern UI/UX design

---

## 🤝 Contributing

Improvements और suggestions welcome हैं! Feel free to fork और pull request create करें।

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

**NavGurukul Student Project**  
AI-Based Smart Video Learning Tool

---

## 🙏 Credits

- **Streamlit** - UI Framework
- **Google Gemini** - AI Content Generation
- **YouTube Transcript API** - Transcript Extraction

---

## 📞 Support

किसी भी problem के लिए instructor से contact करें या project documentation देखें।

---

**Happy Learning! 🎓✨**
