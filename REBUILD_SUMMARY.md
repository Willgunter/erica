# Erica Learning Platform - Rebuild Summary

## Overview
The learning platform has been rebuilt with enhanced AI-powered features for personalized learning experiences.

## What Was Fixed

### 1. **API Keys Configuration**
- ✅ Added `GEMINI_API_KEY` to `.env`
- ✅ Added `ELEVENLABS_API_KEY` to `.env`
- Both keys are now properly configured for the backend services

### 2. **Dependencies Updated**
Updated `requirements.txt` with:
- `manim>=0.18.0` - For animated video generation
- `elevenlabs>=1.0.0` - For AI voice generation
- `requests>=2.31.0` - For API calls

### 3. **Manim Video Generation (Visual Learners)**
**Location:** `/Users/aadeechheda/Projects/HackUNCP/erica/app/lesson_engine/media.py`

**Features:**
- AI-powered script generation using Gemini
- Creates engaging educational animations
- Automatically generates Python Manim scripts based on lesson content
- Renders videos using Manim CLI
- Fallback to simple animations if AI fails
- Error handling for rendering timeouts

**How it works:**
1. Takes module content and learning objectives
2. Uses Gemini to generate a Manim Python script with animations
3. Renders the script to MP4 video
4. Stores video in object storage
5. Returns video URL for playback

### 4. **Podcast Generation (Auditory Learners)**
**Location:** `/Users/aadeechheda/Projects/HackUNCP/erica/app/lesson_engine/media.py`

**Features:**
- AI-powered podcast script generation using Gemini
- Natural, conversational narration
- Professional voice synthesis using ElevenLabs
- Contextual to the learner's subject and goals
- Fallback to basic narration if AI fails

**How it works:**
1. Generates engaging podcast-style narration using Gemini
2. Converts narration to speech using ElevenLabs TTS
3. Uses professional voice (Rachel - voice_id: 21m00Tcm4TlvDq8ikWAM)
4. Stores MP3 in object storage
5. Returns audio URL for playback

### 5. **AI Sparring Partner (Knowledge Checks)**
**Location:** `/Users/aadeechheda/Projects/HackUNCP/erica/app/services/ai_sparring_service.py`

**Features:**
- Intelligent, Socratic questioning approach
- Guides learners instead of just quizzing
- Context-aware responses based on module content
- Encouraging and supportive tone
- Generates personalized follow-up questions

**How it works:**
1. Student answers a knowledge check question
2. AI analyzes the answer in context of the module
3. Generates guiding feedback (not just "correct/incorrect")
4. Helps student discover gaps in understanding
5. Asks follow-up questions to deepen comprehension

**Integration:**
- Connected to `/api/checkpoint` endpoint in `main.py`
- Automatically provides AI feedback for each answer
- Frontend displays AI responses in the knowledge check interface

### 6. **Frontend Updates**
**Location:** `/Users/aadeechheda/Projects/HackUNCP/erica/components/knowledge-check.tsx`

- Updated to display AI-generated feedback
- Maintains fallback to static responses if AI fails
- Seamless integration with existing UI

## How The Complete Flow Works

### Step 1: Onboarding (Step 1 of 5)
- User completes learning preferences
- System captures: subject, goals, study time, pacing, learning style
- Preferences determine whether to generate videos, podcasts, or both

### Step 2: Upload Content (Step 2 of 5)
- User uploads PDFs, slides, documents, or enters topics
- Files are parsed and chunked
- Content is ready for lesson generation

### Step 3: Learning (Step 3 of 5) - **REBUILT**
When user clicks "Generate my lesson":

1. **Lesson Planning:**
   - Analyzes uploaded content chunks
   - Creates personalized modules based on user profile
   - Determines pacing and teaching style

2. **Media Generation (Parallel):**
   - **For Visual Learners:**
     - Gemini generates Manim animation script
     - Manim renders educational video
     - Video stored and URL provided
   
   - **For Auditory Learners:**
     - Gemini generates podcast narration
     - ElevenLabs converts to professional audio
     - Audio stored and URL provided

3. **Lesson Playback:**
   - User progresses through modules step-by-step
   - Videos/podcasts play inline
   - Interactive practice areas for hands-on work

4. **Knowledge Checks (After each module):**
   - **AI Sparring Partner** asks 2-3 questions
   - Student responds in natural language
   - **Gemini provides intelligent, guiding feedback**
   - Helps student think deeper, not just memorize
   - Conversational approach, not quiz-style

### Step 4: Test (Step 4 of 5) - Existing
- Comprehensive test covering all modules
- Feedback provided only at the end
- Scores tracked per topic

### Step 5: Summary (Step 5 of 5) - Existing
- Statistical breakdown of performance
- Topics mastered vs. topics to review
- Saved to user's account history
- Option to replay the lesson

## API Keys Used

### Gemini API (Google)
**Key:** `AIzaSyC4mUXlAvMA1yJ5-KxICnsus1gkMY5rjWo`
**Used for:**
- Manim script generation
- Podcast narration generation
- AI sparring partner responses
- Follow-up question generation

### ElevenLabs API
**Key:** `sk_1bad932c710c2cae7d2094c96155c57a4cdd4cb5cb1934e3`
**Used for:**
- Text-to-speech for podcast generation
- Professional voice synthesis
- Natural-sounding educational audio

## Installation & Setup

### 1. Install Python Dependencies
```bash
cd /Users/aadeechheda/Projects/HackUNCP/erica
pip install -r requirements.txt
```

**Note:** Manim requires system dependencies:
- **macOS:** `brew install py3cairo ffmpeg pango`
- **Linux:** `sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg`

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Environment Variables
The `.env` file is already configured with your API keys:
```
GEMINI_API_KEY=AIzaSyC4mUXlAvMA1yJ5-KxICnsus1gkMY5rjWo
ELEVENLABS_API_KEY=sk_1bad932c710c2cae7d2094c96155c57a4cdd4cb5cb1934e3
INGEST_SYNC=true
DB_PATH=./erica.db
```

### 4. Run the Application

**Terminal 1 - Flask Backend:**
```bash
python app/main.py
```

**Terminal 2 - Next.js Frontend:**
```bash
npm run dev
```

**Access:** http://localhost:3001

## Testing the Flow

1. **Start the app** and go to http://localhost:3001
2. **Complete onboarding:**
   - Choose your subject
   - Select learning preferences (visual/auditory)
   - Set study time and pacing
3. **Upload content:**
   - Drop a PDF, PPTX, or text file
   - Or type in topics manually
4. **Click "Generate my lesson"**
   - Watch the lesson being generated
   - AI creates personalized modules
5. **Learn:**
   - Videos will play (if visual learner)
   - Podcasts will play (if auditory learner)
   - Progress through each module
6. **Knowledge Checks:**
   - Answer questions in your own words
   - **AI sparring partner provides intelligent feedback**
   - Guides you to think deeper
7. **Take the test** after all modules
8. **Review summary** with performance stats

## Key Improvements

✅ **Real AI-Generated Content** - No more placeholder videos/audio
✅ **Intelligent Tutoring** - AI sparring partner guides learning
✅ **Personalized Media** - Content adapts to learning style
✅ **Professional Quality** - ElevenLabs voice, Manim animations
✅ **Codecademy-Inspired** - Interactive, step-by-step learning
✅ **Error Handling** - Graceful fallbacks if AI services fail

## Technical Architecture

```
Frontend (Next.js/React)
    ↓
API Routes (/app/api/*)
    ↓
Flask Backend (main.py)
    ↓
    ├─ Lesson Engine
    │   ├─ Planner (creates modules)
    │   ├─ Media Generator
    │   │   ├─ Gemini → Manim Script → Video
    │   │   └─ Gemini → ElevenLabs → Podcast
    │   └─ Service (orchestrates)
    │
    ├─ AI Sparring Service
    │   └─ Gemini → Guiding Responses
    │
    └─ Checkpoint/Test Services
```

## Files Modified/Created

### Created:
- `/app/services/ai_sparring_service.py` - AI sparring partner logic

### Modified:
- `/app/lesson_engine/media.py` - Real media generation
- `/app/services/checkpoint_service.py` - AI integration
- `/app/main.py` - AI feedback endpoint
- `/components/knowledge-check.tsx` - AI feedback display
- `/requirements.txt` - New dependencies
- `/.env` - API keys

## Notes

- **Manim rendering** can take 10-30 seconds per video
- **ElevenLabs** has usage limits based on your plan
- **Gemini** responses are fast but require internet connection
- All services have **fallback mechanisms** if AI fails
- Media files are stored in `/app/object_storage/`
