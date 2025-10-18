"""
Smart Career Coaching Knowledge Base
Provides instant, expert career advice based on keyword matching
"""
import re
from typing import List, Tuple


class CareerKnowledgeBase:
    """Expert career coaching responses organized by topic"""

    CAREER_TOPICS = {
        # Resume & CV
        "resume": {
            "keywords": ["resume", "cv", "curriculum vitae", "write resume", "update resume"],
            "responses": [
                "When crafting your resume, focus on quantifiable achievements rather than just responsibilities. Use action verbs and include metrics wherever possible (e.g., 'Increased sales by 30%' instead of 'Responsible for sales').",
                "Tailor your resume for each job application. Highlight the skills and experiences most relevant to the position. Use keywords from the job description to pass ATS (Applicant Tracking Systems).",
                "Keep your resume concise - ideally one page for early career, two pages for experienced professionals. Use clear section headers: Summary, Experience, Education, Skills, and Projects."
            ]
        },

        # Interview Preparation
        "interview": {
            "keywords": ["interview", "job interview", "interview tips", "prepare interview", "interview questions"],
            "responses": [
                "Research the company thoroughly before your interview. Understand their products, culture, recent news, and competitors. Prepare thoughtful questions to ask the interviewer.",
                "Use the STAR method (Situation, Task, Action, Result) to answer behavioral questions. Practice common questions like 'Tell me about yourself' and 'Why do you want this job?'",
                "Prepare 3-5 stories that demonstrate your key skills and achievements. Have examples ready for teamwork, problem-solving, leadership, and handling challenges."
            ]
        },

        # Career Change
        "career change": {
            "keywords": ["career change", "switch career", "transition", "new career", "change jobs"],
            "responses": [
                "When changing careers, identify transferable skills from your current role. Focus on skills like communication, project management, problem-solving, and leadership that apply across industries.",
                "Build a bridge to your new career through side projects, freelancing, or volunteer work. This demonstrates commitment and helps you gain relevant experience.",
                "Network extensively in your target industry. Attend industry events, join professional groups on LinkedIn, and conduct informational interviews to learn and make connections."
            ]
        },

        # Salary Negotiation
        "salary": {
            "keywords": ["salary", "negotiate", "pay", "compensation", "raise", "offer"],
            "responses": [
                "Research market rates for your role using sites like Glassdoor, Payscale, and Levels.fyi. Know your worth before entering negotiations. Consider total compensation including benefits, bonuses, and equity.",
                "When negotiating, focus on your value, not your needs. Highlight your achievements, skills, and market data. Practice your negotiation conversation beforehand.",
                "Don't accept the first offer immediately. It's professional to ask for time to consider. Counter with a specific number backed by research, and be prepared to justify it."
            ]
        },

        # Skill Development
        "skills": {
            "keywords": ["learn", "skills", "courses", "training", "improve", "develop skills"],
            "responses": [
                "Identify in-demand skills in your field through job postings and industry reports. Focus on both technical skills and soft skills like communication and leadership.",
                "Create a learning plan with specific, measurable goals. Use platforms like Coursera, Udemy, and LinkedIn Learning. Apply new skills immediately through projects.",
                "Build a portfolio showcasing your skills. For tech: GitHub projects. For design: Behance. For writing: Medium articles. Demonstrable work speaks louder than certificates."
            ]
        },

        # Networking
        "network": {
            "keywords": ["network", "networking", "connections", "linkedin", "professional network"],
            "responses": [
                "Networking is about building genuine relationships, not collecting contacts. Focus on how you can help others, not just what you can get. Follow up consistently.",
                "Optimize your LinkedIn profile with a professional photo, compelling headline, and detailed experience. Share industry insights and engage with others' content regularly.",
                "Attend industry meetups, conferences, and workshops. Prepare a concise personal pitch. After meeting someone, send a personalized follow-up within 24-48 hours."
            ]
        },

        # Remote Work
        "remote": {
            "keywords": ["remote work", "work from home", "wfh", "remote job", "virtual work"],
            "responses": [
                "For remote work success, create a dedicated workspace and maintain a consistent schedule. Set clear boundaries between work and personal time.",
                "Over-communicate with your team. Use video calls for important discussions, keep your calendar updated, and provide regular status updates. Be responsive during working hours.",
                "Build remote-friendly skills: written communication, self-management, and proficiency with collaboration tools (Slack, Zoom, Asana). Highlight these in applications."
            ]
        },

        # Leadership & Management
        "leadership": {
            "keywords": ["leadership", "manager", "lead", "management", "team lead"],
            "responses": [
                "Great leaders focus on empowering their team rather than micromanaging. Provide clear goals, resources, and support. Trust your team members to execute.",
                "Develop emotional intelligence: self-awareness, empathy, and relationship management. Regular one-on-ones with team members are crucial for understanding their needs and concerns.",
                "Lead by example. Demonstrate the work ethic, communication style, and values you expect from your team. Be transparent about decisions and challenges."
            ]
        },

        # Work-Life Balance
        "work-life balance": {
            "keywords": ["work-life balance", "burnout", "stress", "overwhelmed", "work life"],
            "responses": [
                "Set clear boundaries: define working hours and stick to them. Learn to say no to non-essential commitments. Prioritize tasks using methods like Eisenhower Matrix.",
                "Take regular breaks throughout the day. Use techniques like Pomodoro (25 min work, 5 min break). Schedule time for exercise, hobbies, and relationships.",
                "If experiencing burnout, communicate with your manager. Discuss workload, delegate where possible, and consider taking time off to recharge."
            ]
        },

        # Job Search
        "job search": {
            "keywords": ["job search", "finding job", "job hunting", "looking for job", "apply"],
            "responses": [
                "Quality over quantity in job applications. Target 5-10 companies you're genuinely interested in. Customize each application and try to find internal referrals.",
                "Use multiple job search strategies: company websites, LinkedIn, industry-specific boards, networking, and recruiters. Track your applications in a spreadsheet.",
                "Follow up on applications after 1-2 weeks if you haven't heard back. Reach out to hiring managers or recruiters on LinkedIn with a brief, professional message."
            ]
        },

        # Tech Careers
        "software": {
            "keywords": ["software engineer", "developer", "programming", "coding", "software development"],
            "responses": [
                "Build a strong GitHub portfolio with 3-5 substantial projects. Contribute to open source. Practice data structures and algorithms on LeetCode or HackerRank.",
                "Learn in-demand technologies: cloud platforms (AWS/Azure), containers (Docker/Kubernetes), and modern frameworks (React, FastAPI, etc.). Stay updated with industry trends.",
                "Prepare for technical interviews: practice coding problems, system design, and behavioral questions. Use Cracking the Coding Interview and similar resources."
            ]
        },

        # Data Science & AI/ML
        "data science": {
            "keywords": ["data scientist", "machine learning", "data analysis", "analytics", "ml engineer", "ai engineer", "artificial intelligence", "become ai", "become ml", "andrew", "coursera", "ml course", "ai course", "learning path"],
            "responses": [
                "To become an AI/ML engineer: 1) Learn Python and math (linear algebra, calculus, statistics). 2) Master ML frameworks (TensorFlow, PyTorch, scikit-learn). 3) Build projects showcasing real ML applications. 4) Study algorithms deeply - understand when and why to use each one.",
                "Build a portfolio of data science projects on Kaggle or GitHub. Include end-to-end projects: data collection, cleaning, analysis, modeling, and visualization. Show both technical skills and business impact.",
                "Master core skills: Python, SQL, statistics, machine learning algorithms, and data visualization. Stay current with frameworks (TensorFlow, PyTorch) and deployment tools (Docker, AWS). Communication is crucial - practice explaining complex concepts simply.",
                "Start with Andrew Ng's 'Machine Learning' course on Coursera (the classic one) or his newer 'Deep Learning Specialization'. Both are excellent. Fast.ai is great for practical deep learning. DataCamp is good for hands-on practice. Pick one, complete it fully, then build projects.",
                "Andrew Ng's Machine Learning course on Coursera is the gold standard for beginners. It covers fundamentals thoroughly. After that, take his Deep Learning Specialization for neural networks. Combine with Fast.ai for practical PyTorch skills."
            ]
        },

        # General Career Advice
        "general": {
            "keywords": ["career advice", "career tips", "professional growth", "career development"],
            "responses": [
                "Success in any career requires continuous learning, strong relationships, and adaptability. Set clear short-term and long-term goals. Review and adjust them quarterly.",
                "Build your personal brand: What do you want to be known for? Share your expertise through blog posts, speaking, or mentoring. Become a go-to person in your niche.",
                "Seek feedback regularly and act on it. Find mentors who've achieved what you aspire to. Be a mentor to others - teaching reinforces your own knowledge."
            ]
        }
    }

    @classmethod
    def get_response(cls, message: str) -> str:
        """Get the most relevant career advice based on user message"""
        message_lower = message.lower()

        # Find matching topics based on keywords
        matches: List[Tuple[str, int]] = []

        for topic, data in cls.CAREER_TOPICS.items():
            match_count = sum(1 for keyword in data["keywords"] if keyword in message_lower)
            if match_count > 0:
                matches.append((topic, match_count))

        # Sort by number of keyword matches
        matches.sort(key=lambda x: x[1], reverse=True)

        if matches:
            # Get the best matching topic
            best_topic = matches[0][0]
            responses = cls.CAREER_TOPICS[best_topic]["responses"]

            # Return a random response from the topic
            import random
            return random.choice(responses)

        # Default response if no keywords match
        return cls._get_default_response(message_lower)

    @classmethod
    def _get_default_response(cls, message: str) -> str:
        """Provide a helpful default response"""
        if "?" in message:
            return ("Great question! I can help you with: resume writing, interview preparation, "
                   "career transitions, salary negotiation, skill development, networking, remote work, "
                   "leadership, work-life balance, and job search strategies. What specific area interests you?")
        elif any(word in message for word in ["hello", "hi", "hey", "greetings"]):
            return ("Hello! I'm your AI Career Coach. I can help you with career advice, "
                   "resume tips, interview preparation, salary negotiation, and more. What career "
                   "topic would you like to discuss?")
        elif any(word in message for word in ["thanks", "thank you", "appreciate"]):
            return ("You're welcome! Feel free to ask me anything else about your career development. "
                   "I'm here to help you succeed!")
        else:
            return ("I'm here to help with your career development. Ask me about resumes, interviews, "
                   "career changes, salary negotiation, skills, networking, or any career-related topic!")


career_kb = CareerKnowledgeBase()
