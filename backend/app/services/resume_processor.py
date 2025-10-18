from pdfminer.high_level import extract_text
from docx import Document
import io
import re
from typing import List


class ResumeProcessor:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            text = extract_text(io.BytesIO(file_content))
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting DOCX text: {str(e)}")

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Extract skills from resume text using pattern matching"""
        # Common technical skills
        skill_patterns = [
            r'Python', r'JavaScript', r'Java', r'C\+\+', r'React', r'Angular',
            r'Node\.js', r'SQL', r'MongoDB', r'Docker', r'Kubernetes',
            r'AWS', r'Azure', r'GCP', r'Machine Learning', r'Data Science',
            r'FastAPI', r'Django', r'Flask', r'TensorFlow', r'PyTorch',
            r'Git', r'CI/CD', r'Agile', r'Scrum', r'REST API', r'GraphQL',
            r'TypeScript', r'Vue\.js', r'Express\.js', r'PostgreSQL', r'Redis'
        ]

        skills = []
        text_lower = text.lower()

        for pattern in skill_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Get the original case match
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    skills.append(match.group(0))

        return list(set(skills))  # Remove duplicates

    @staticmethod
    def extract_experience(text: str) -> List[str]:
        """Extract work experience sections"""
        experience_patterns = [
            r'(?:Experience|Work History|Employment).*?(?=Education|Skills|$)',
            r'\d{4}\s*-\s*(?:\d{4}|Present).*?(?=\n\n|\d{4}\s*-|$)'
        ]

        experiences = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            experiences.extend(matches)

        # Clean up and limit
        experiences = [exp.strip()[:200] for exp in experiences if len(exp.strip()) > 20]
        return experiences[:5]  # Limit to 5 experiences

    @staticmethod
    def extract_education(text: str) -> List[str]:
        """Extract education information"""
        education_patterns = [
            r'(?:Bachelor|Master|PhD|B\.S\.|M\.S\.|MBA).*?(?=\n\n|Experience|Skills|$)',
            r'(?:University|College|Institute).*?(?=\n\n|Experience|$)'
        ]

        education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            education.extend(matches)

        # Clean up
        education = [edu.strip()[:200] for edu in education if len(edu.strip()) > 10]
        return list(set(education))[:3]  # Limit to 3 education entries


resume_processor = ResumeProcessor()
