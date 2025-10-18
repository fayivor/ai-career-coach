from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer, util
import torch
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIModels:
    def __init__(self):
        self.chatbot_model = None
        self.summarizer = None
        self.ner_model = None
        self.sentence_transformer = None

    async def load_models(self):
        """Load all AI models on startup"""
        try:
            logger.info("Loading AI models...")

            # For chatbot - using a lighter model due to resource constraints
            # In production, you'd use Mistral-7B-Instruct
            logger.info("Loading chatbot model...")
            self.chatbot_model = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                device=-1  # CPU
            )

            # Summarizer
            logger.info("Loading summarizer model...")
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1
            )

            # NER model
            logger.info("Loading NER model...")
            self.ner_model = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                device=-1
            )

            # Sentence transformer for skill matching
            logger.info("Loading sentence transformer...")
            self.sentence_transformer = SentenceTransformer(
                'sentence-transformers/all-MiniLM-L6-v2'
            )

            logger.info("All models loaded successfully!")

        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise

    def generate_chat_response(self, message: str) -> str:
        """Generate chatbot response"""
        try:
            # Prepare career coaching context
            prompt = f"Career Coach: You are a professional career coach. Help the user with their career questions.\n\nUser: {message}\n\nCareer Coach:"

            response = self.chatbot_model(
                prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )

            return response[0]['generated_text'].split("Career Coach:")[-1].strip()

        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return "I'm here to help with your career questions. Could you please rephrase that?"

    def summarize_text(self, text: str) -> str:
        """Summarize resume text"""
        try:
            if len(text) < 100:
                return text

            # BART works best with text between 56-1024 tokens
            max_chunk = 1024
            if len(text) > max_chunk:
                text = text[:max_chunk]

            summary = self.summarizer(
                text,
                max_length=150,
                min_length=50,
                do_sample=False
            )

            return summary[0]['summary_text']

        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return "Unable to generate summary."

    def extract_entities(self, text: str) -> dict:
        """Extract named entities from text"""
        try:
            entities = self.ner_model(text)

            # Group entities by type
            grouped = {}
            for entity in entities:
                entity_type = entity['entity'].split('-')[-1]
                if entity_type not in grouped:
                    grouped[entity_type] = []
                grouped[entity_type].append(entity['word'])

            return grouped

        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {}

    def calculate_skill_similarity(self, current_skills: List[str], required_skills: List[str]) -> dict:
        """Calculate skill gap using sentence transformers"""
        try:
            # Encode skills
            current_embeddings = self.sentence_transformer.encode(current_skills, convert_to_tensor=True)
            required_embeddings = self.sentence_transformer.encode(required_skills, convert_to_tensor=True)

            # Calculate cosine similarities
            similarities = util.cos_sim(current_embeddings, required_embeddings)

            matched_skills = []
            missing_skills = []

            for i, req_skill in enumerate(required_skills):
                max_sim = torch.max(similarities[:, i]).item()
                if max_sim > 0.7:  # Threshold for skill match
                    matched_skills.append(req_skill)
                else:
                    missing_skills.append(req_skill)

            total_required = len(required_skills)
            matched_count = len(matched_skills)
            gap_percentage = ((total_required - matched_count) / total_required * 100) if total_required > 0 else 0

            return {
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "gap_percentage": round(gap_percentage, 2)
            }

        except Exception as e:
            logger.error(f"Error calculating skill similarity: {str(e)}")
            return {
                "matched_skills": [],
                "missing_skills": required_skills,
                "gap_percentage": 100.0
            }


# Global instance
ai_models = AIModels()
