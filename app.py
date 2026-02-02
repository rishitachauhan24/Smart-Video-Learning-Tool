import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)

def extract_video_id(youtube_url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    """Get transcript from YouTube video"""
    try:
        # Create API instance
        api = YouTubeTranscriptApi()
        
        # List all available transcripts
        transcript_list = api.list(video_id)
        
        # Try to get the first available transcript
        for transcript in transcript_list:
            try:
                # Fetch the transcript
                data = transcript.fetch()
                
                # Extract text from FetchedTranscriptSnippet objects
                transcript_text = ' '.join([item.text for item in data])
                
                if transcript_text:
                    return transcript_text
            except Exception as e:
                continue
        
        return None
    except Exception as e:
        return None

def generate_summary(transcript):
    """Generate summary using Google Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return "⚠️ API Key not configured. Please add GOOGLE_API_KEY to .env file"
            
        prompt = f"""
        You are an educational content analyzer. Analyze the following video transcript and provide a comprehensive summary.
        
        Transcript:
        {transcript[:8000]}
        
        Provide a clear, concise summary in 150-200 words that captures the main ideas and key concepts.
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or 'quota' in error_msg.lower():
            return """
            ⚠️ **API Quota Limit Reached**
            
            Your Google Gemini API free tier limit has been exceeded for today.
            
            **Solutions:**
            1. 🕒 Wait 24 hours for quota reset
            2. 🔑 Generate a new API key at: https://makersuite.google.com/app/apikey
            3. 💳 Upgrade to paid tier for higher limits
            
            **Current Limits (Free Tier):**
            - 15 requests per minute
            - 1500 requests per day
            """
        return f"❌ Error generating summary. Please check your internet connection and try again."

def generate_key_points(transcript):
    """Generate key learning points using Google Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return "⚠️ API Key not configured. Please add GOOGLE_API_KEY to .env file"
            
        prompt = f"""
        You are an educational content analyzer. Analyze the following video transcript and extract the most important learning points.
        
        Transcript:
        {transcript[:8000]}
        
        Provide exactly 5-7 key learning points in bullet format. Each point should be:
        - Clear and concise
        - Educational and informative
        - Directly derived from the transcript
        
        Format each point as:
        • Point text here
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or 'quota' in error_msg.lower():
            return """
            ⚠️ **API Quota Limit Reached**
            
            Your Google Gemini API free tier limit has been exceeded for today.
            
            **Solutions:**
            1. 🕒 Wait 24 hours for quota reset
            2. 🔑 Generate a new API key at: https://makersuite.google.com/app/apikey
            3. 💳 Upgrade to paid tier for higher limits
            """
        return f"❌ Error generating key points. Please check your internet connection and try again."

def generate_quiz(transcript):
    """Generate exactly 10 quiz questions using Google Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return None
            
        prompt = f"""
        You are an educational quiz creator. Based on the following video transcript, create EXACTLY 10 multiple-choice questions.
        
        Transcript:
        {transcript[:8000]}
        
        Requirements:
        1. Generate EXACTLY 10 questions (no more, no less)
        2. Each question must have 4 options (A, B, C, D)
        3. Indicate the correct answer
        4. Questions should test understanding of key concepts from the video
        5. Cover different topics from the transcript
        
        Format each question EXACTLY as follows (strictly follow this format):
        
        Q1: [Question text here]
        A) [Option A text]
        B) [Option B text]
        C) [Option C text]
        D) [Option D text]
        ANSWER: A
        
        Q2: [Question text here]
        A) [Option A text]
        B) [Option B text]
        C) [Option C text]
        D) [Option D text]
        ANSWER: B
        
        Continue this exact pattern for all 10 questions. Use only A, B, C, or D for the ANSWER field.
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or 'quota' in error_msg.lower():
            st.error("""
            ⚠️ **API Quota Limit Reached**
            
            Your Google Gemini API free tier limit has been exceeded for today.
            
            **Solutions:**
            - 🕒 Wait 24 hours for quota reset
            - 🔑 Create new API key: https://makersuite.google.com/app/apikey
            - 💳 Upgrade to paid tier
            """)
        else:
            st.error(f"❌ Error generating quiz. Please try again.")
        return None

def parse_quiz(quiz_text):
    """Parse quiz text into structured format"""
    import re
    
    if not quiz_text:
        return []
    
    questions = []
    # Split by question numbers
    quiz_parts = re.split(r'Q\d+:', quiz_text)
    
    for part in quiz_parts[1:]:  # Skip first empty part
        if not part.strip():
            continue
            
        lines = [line.strip() for line in part.strip().split('\n') if line.strip()]
        
        if len(lines) < 5:
            continue
        
        question_data = {
            'question': lines[0],
            'options': {},
            'answer': None
        }
        
        # Extract options
        for line in lines[1:]:
            if line.startswith('A)'):
                question_data['options']['A'] = line[2:].strip()
            elif line.startswith('B)'):
                question_data['options']['B'] = line[2:].strip()
            elif line.startswith('C)'):
                question_data['options']['C'] = line[2:].strip()
            elif line.startswith('D)'):
                question_data['options']['D'] = line[2:].strip()
            elif 'ANSWER:' in line.upper() or 'CORRECT ANSWER:' in line.upper():
                # Extract answer
                answer_match = re.search(r'[ABCD]', line.upper())
                if answer_match:
                    question_data['answer'] = answer_match.group()
        
        # Only add if we have all components
        if question_data['question'] and len(question_data['options']) == 4 and question_data['answer']:
            questions.append(question_data)
    
    return questions[:10]  # Return max 10 questions

# Streamlit UI Configuration
st.set_page_config(
    page_title="Smart Video Learning Tool",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 28px;
        font-weight: bold;
        color: #1E88E5;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 3px solid #1E88E5;
        padding-bottom: 5px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .success-box {
        padding: 15px;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        border-radius: 5px;
        margin: 15px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        border-radius: 5px;
        margin: 15px 0;
    }
    .quiz-question {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<div class="main-header">🎓 Smart Video Learning Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform any YouTube video into complete study material with AI</div>', unsafe_allow_html=True)

# Check if API key is configured
if not GOOGLE_API_KEY:
    st.error("⚠️ Google API Key not found! Please create a .env file with your GOOGLE_API_KEY")
    st.info("""
    **Setup Instructions:**
    1. Create a `.env` file in the project folder
    2. Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`
    3. Get API key from: https://makersuite.google.com/app/apikey
    """)
    st.stop()

# Input Section
st.markdown("---")
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    youtube_url = st.text_input(
        "📺 Enter YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the YouTube video link here"
    )
    
    process_button = st.button("🚀 Generate Learning Material", use_container_width=True)

# Process Video
if process_button and youtube_url:
    # Extract video ID
    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        st.error("❌ Invalid YouTube URL. Please check and try again.")
    else:
        # Show video
        st.markdown("---")
        st.markdown('<div class="section-header">📹 Video Preview</div>', unsafe_allow_html=True)
        st.video(youtube_url)
        
        # Get transcript
        with st.spinner("📝 Extracting video transcript..."):
            transcript = get_transcript(video_id)
        
        if not transcript:
            st.error("❌ Could not extract transcript. Make sure the video has subtitles/captions enabled.")
        else:
            st.success(f"✅ Transcript extracted successfully! ({len(transcript.split())} words)")
            
            # Create tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🎯 Key Points", "📊 Quiz", "📄 Full Transcript"])
            
            # Summary Tab
            with tab1:
                st.markdown('<div class="section-header">📝 Video Summary</div>', unsafe_allow_html=True)
                with st.spinner("🤖 AI is generating summary..."):
                    summary = generate_summary(transcript)
                st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
            
            # Key Points Tab
            with tab2:
                st.markdown('<div class="section-header">🎯 Key Learning Points</div>', unsafe_allow_html=True)
                with st.spinner("🤖 AI is extracting key points..."):
                    key_points = generate_key_points(transcript)
                st.markdown(f'<div class="success-box">{key_points}</div>', unsafe_allow_html=True)
            
            # Quiz Tab
            with tab3:
                st.markdown('<div class="section-header">📊 Quiz - Test Your Understanding</div>', unsafe_allow_html=True)
                st.info("📌 Answer all 10 questions based on the video content")
                
                # Initialize session state with video-specific key
                quiz_key = f"quiz_{video_id}"
                if quiz_key not in st.session_state:
                    with st.spinner("🤖 AI is creating quiz questions..."):
                        quiz_text = generate_quiz(transcript)
                        st.session_state[quiz_key] = parse_quiz(quiz_text) if quiz_text else []
                
                questions = st.session_state.get(quiz_key, [])
                
                if questions:
                    # Initialize session state for this quiz
                    if f'answers_{video_id}' not in st.session_state:
                        st.session_state[f'answers_{video_id}'] = {}
                    if f'submitted_{video_id}' not in st.session_state:
                        st.session_state[f'submitted_{video_id}'] = False
                    
                    user_answers = st.session_state[f'answers_{video_id}']
                    is_submitted = st.session_state[f'submitted_{video_id}']
                    
                    # Display each question
                    for idx, q in enumerate(questions, 1):
                        st.markdown(f"### 📝 Question {idx} of {len(questions)}")
                        st.markdown(f"**{q['question']}**")
                        st.markdown("")  # spacing
                        
                        # Create options with better formatting
                        options_display = {
                            'A': f"A) {q['options'].get('A', '')}",
                            'B': f"B) {q['options'].get('B', '')}",
                            'C': f"C) {q['options'].get('C', '')}",
                            'D': f"D) {q['options'].get('D', '')}"
                        }
                        
                        # Get current answer (from session state or None)
                        current_answer = user_answers.get(idx)
                        
                        # Radio button for options
                        selected = st.radio(
                            f"Choose your answer:",
                            options=['A', 'B', 'C', 'D'],
                            format_func=lambda x, opts=options_display: opts[x],
                            key=f"question_{video_id}_{idx}",
                            index=['A', 'B', 'C', 'D'].index(current_answer) if current_answer in ['A', 'B', 'C', 'D'] else None,
                            disabled=is_submitted
                        )
                        
                        # Save answer to session state
                        if selected:
                            user_answers[idx] = selected
                        
                        # Show result if submitted
                        if is_submitted and selected:
                            if selected == q['answer']:
                                st.success(f"✅ Correct! The answer is **{q['answer']}) {q['options'][q['answer']]}**")
                            else:
                                st.error(f"❌ Incorrect. The correct answer is **{q['answer']}) {q['options'][q['answer']]}**")
                        
                        st.markdown("---")
                    
                    # Buttons section
                    st.markdown("")  # spacing
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        if not is_submitted:
                            if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                                # Check if all questions are answered
                                if len(user_answers) < len(questions):
                                    st.warning(f"⚠️ Please answer all {len(questions)} questions before submitting!")
                                else:
                                    st.session_state[f'submitted_{video_id}'] = True
                                    st.rerun()
                    
                    with col2:
                        if st.button("🔄 Try Again", use_container_width=True):
                            st.session_state[f'answers_{video_id}'] = {}
                            st.session_state[f'submitted_{video_id}'] = False
                            st.rerun()
                    
                    # Show score if submitted
                    if is_submitted:
                        st.markdown("---")
                        correct = sum(1 for idx, q in enumerate(questions, 1) 
                                    if user_answers.get(idx) == q['answer'])
                        total = len(questions)
                        percentage = (correct / total) * 100
                        
                        # Score display with color coding
                        if percentage >= 80:
                            st.success(f"### 🎉 Excellent! Your Score: {correct}/{total} ({percentage:.1f}%)")
                            st.info("🌟 Outstanding performance! You have mastered this content!")
                        elif percentage >= 60:
                            st.info(f"### 👍 Good Job! Your Score: {correct}/{total} ({percentage:.1f}%)")
                            st.info("💪 Well done! Keep up the good work!")
                        else:
                            st.warning(f"### 📚 Your Score: {correct}/{total} ({percentage:.1f}%)")
                            st.info("💡 Don't worry! Review the video and try again. You'll do better!")
                        
                        if percentage == 100:
                            st.balloons()
                
                elif st.session_state.get(quiz_key) is not None:
                    st.warning("⚠️ Could not generate quiz questions. The video content might be too short or unclear.")
                    if st.button("🔄 Retry Quiz Generation"):
                        del st.session_state[quiz_key]
                        st.rerun()
            
            # Transcript Tab
            with tab4:
                st.markdown('<div class="section-header">📄 Full Video Transcript</div>', unsafe_allow_html=True)
                st.text_area("Transcript", transcript, height=400)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Smart Video Learning Tool</strong> - AI-Powered Educational Assistant</p>
    <p>Transform videos into summaries, notes, and quizzes instantly! 🎓</p>
</div>
""", unsafe_allow_html=True)
