"""
OpenAI GPT-based chatbot service for AI Career Coach
Provides conversational AI using GPT models with career coaching context
"""

import os
from openai import OpenAI
from typing import List, Dict

class GPTChatbot:
    def __init__(self, api_key: str = None):
        """
        Initialize GPT chatbot with OpenAI API key

        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []

        # System prompt that defines the AI Career Coach personality
        self.system_prompt = """You are an expert AI Career Coach with deep knowledge in:
- Career transitions and development
- Technical skills (programming, data science, AI/ML, web development, cloud computing)
- Resume writing and interview preparation
- Learning paths and course recommendations
- Job search strategies
- Soft skills development

Your role is to:
1. Provide personalized, actionable career advice
2. Help users identify skill gaps and create learning plans
3. Recommend specific courses, resources, and certifications
4. Guide career transitions with practical steps
5. Be encouraging and supportive while being honest about challenges

Keep responses conversational, concise (2-4 paragraphs max), and focused on practical next steps.
When recommending courses, prioritize well-known platforms like Coursera, Udemy, freeCodeCamp, etc.
"""

    def chat(self, user_message: str, use_history: bool = True) -> str:
        """
        Send a message to GPT and get a response

        Args:
            user_message: The user's message
            use_history: Whether to include conversation history (default: True)

        Returns:
            GPT's response as a string
        """
        try:
            # Build messages list
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add conversation history if enabled
            if use_history and self.conversation_history:
                messages.extend(self.conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5 for faster responses and lower cost
                messages=messages,
                max_tokens=500,  # Limit response length
                temperature=0.7,  # Balance between creativity and consistency
            )

            # Extract the response
            assistant_message = response.choices[0].message.content.strip()

            # Update conversation history
            if use_history:
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})

                # Keep only last 10 messages to avoid token limits
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]

            return assistant_message

        except Exception as e:
            return f"I'm having trouble processing your request right now. Error: {str(e)}"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_history_length(self) -> int:
        """Get the number of messages in conversation history"""
        return len(self.conversation_history)

# Singleton instance
_chatbot_instance = None

def get_gpt_chatbot(api_key: str = None) -> GPTChatbot:
    """
    Get or create the GPT chatbot singleton instance

    Args:
        api_key: OpenAI API key (only needed on first call)

    Returns:
        GPTChatbot instance
    """
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = GPTChatbot(api_key=api_key)
    return _chatbot_instance
