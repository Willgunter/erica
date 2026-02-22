"""AI Sparring Partner service for knowledge checks using Gemini."""

import os
from typing import Any

import google.generativeai as genai
import logging

from ..gemini import init_gemini_model

_logger = logging.getLogger(__name__)


class AISparringPartner:
    """Intelligent AI sparring partner that guides learners through knowledge checks."""
    
    def __init__(self):
        gemini_key = os.environ.get("GEMINI_API_KEY")
        _logger.debug("[AISparring] Initializing: has_gemini_key=%s", bool(gemini_key))
        if gemini_key:
            self.model, _ = init_gemini_model(genai, gemini_key, _logger, "AISparring")
        else:
            self.model = None
            _logger.warning("[AISparring] GEMINI_API_KEY missing; fallback guidance enabled.")
    
    def generate_guiding_response(
        self,
        question: str,
        student_answer: str,
        module_context: dict[str, Any],
        conversation_history: list[dict[str, str]] = None
    ) -> str:
        """
        Generate a guiding response that helps the student think deeper,
        rather than just providing the answer.
        """
        if not self.model:
            _logger.debug("[AISparring] Using fallback guidance response.")
            return self._fallback_response(student_answer)
        
        try:
            _logger.info("[AISparring] Calling Gemini for guiding response | module=%s", module_context.get("module_id"))
            history_text = ""
            if conversation_history:
                history_text = "\n".join([
                    f"{msg['role']}: {msg['content']}"
                    for msg in conversation_history[-4:]  # Last 4 messages
                ])
            
            prompt = f"""
You are Erica, an AI sparring partner helping a student learn {module_context.get('title', 'this topic')}.

Your role is to GUIDE, not QUIZ. You should:
1. Acknowledge what the student got right
2. Gently probe deeper with Socratic questions
3. Help them discover gaps in understanding
4. Encourage critical thinking
5. Be warm, supportive, and conversational

Module Context:
- Title: {module_context.get('title', 'N/A')}
- Objective: {module_context.get('objective', 'N/A')}

Current Question: {question}

Student's Answer: {student_answer}

Recent Conversation:
{history_text if history_text else "This is the first exchange."}

Respond in 2-3 sentences that guide the student to think deeper. Don't give away the answer directly.
Be encouraging and use phrases like "That's a good start", "Can you expand on that?", "What if we consider...?"

Your response:
"""
            
            response = self.model.generate_content(prompt)
            reply = response.text.strip()
            _logger.debug("[AISparring] Gemini guiding response length=%d", len(reply))
            return reply
        
        except Exception as e:
            _logger.exception("[AISparring] Guiding response generation failed: %s", e)
            if "not found" in str(e).lower():
                self.model = None
                _logger.warning("[AISparring] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            return self._fallback_response(student_answer)
    
    def _fallback_response(self, student_answer: str) -> str:
        """Fallback response if AI fails."""
        responses = [
            "That's a good start! Can you elaborate on that a bit more?",
            "I like where you're going with this. What else can you tell me?",
            "Interesting perspective! How does this connect to what we just learned?",
            "Good thinking! Can you explain why you think that?",
        ]
        import random
        return random.choice(responses)
    
    def generate_followup_question(
        self,
        original_question: str,
        student_answer: str,
        module_context: dict[str, Any]
    ) -> str:
        """Generate a thoughtful follow-up question based on the student's answer."""
        if not self.model:
            _logger.debug("[AISparring] Using fallback follow-up question.")
            return "Can you give me a specific example of how you'd apply this?"
        
        try:
            _logger.info("[AISparring] Calling Gemini for follow-up question | module=%s", module_context.get("module_id"))
            prompt = f"""
You are Erica, an AI learning partner. The student just answered a question about {module_context.get('title', 'this topic')}.

Original Question: {original_question}
Student's Answer: {student_answer}

Generate ONE thoughtful follow-up question that:
1. Builds on what they said
2. Encourages them to apply the concept
3. Connects to real-world scenarios
4. Deepens their understanding

Keep it conversational and supportive. Just provide the question, nothing else.
"""
            
            response = self.model.generate_content(prompt)
            followup = response.text.strip()
            _logger.debug("[AISparring] Gemini follow-up length=%d", len(followup))
            return followup
        
        except Exception as e:
            _logger.exception("[AISparring] Follow-up question generation failed: %s", e)
            if "not found" in str(e).lower():
                self.model = None
                _logger.warning("[AISparring] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            return "Can you give me a specific example of how you'd apply this?"
