from typing import List
from app.models.schemas import Course


class CourseRecommender:
    """Mock course recommender - in production, this would scrape/API real courses"""

    # Mock course database
    COURSES_DB = [
        Course(
            title="Complete Python Developer Bootcamp",
            provider="Udemy",
            url="https://udemy.com/python-bootcamp",
            duration="40 hours",
            level="Beginner",
            skills_covered=["Python", "Flask", "Django", "SQL"]
        ),
        Course(
            title="React - The Complete Guide",
            provider="Udemy",
            url="https://udemy.com/react-complete",
            duration="48 hours",
            level="Intermediate",
            skills_covered=["React", "JavaScript", "Redux", "Hooks"]
        ),
        Course(
            title="Machine Learning A-Z",
            provider="Udemy",
            url="https://udemy.com/machine-learning-az",
            duration="44 hours",
            level="Intermediate",
            skills_covered=["Machine Learning", "Python", "TensorFlow", "Data Science"]
        ),
        Course(
            title="Docker and Kubernetes Complete Guide",
            provider="Udemy",
            url="https://udemy.com/docker-kubernetes",
            duration="22 hours",
            level="Advanced",
            skills_covered=["Docker", "Kubernetes", "CI/CD", "DevOps"]
        ),
        Course(
            title="AWS Certified Solutions Architect",
            provider="A Cloud Guru",
            url="https://acloudguru.com/aws-architect",
            duration="30 hours",
            level="Intermediate",
            skills_covered=["AWS", "Cloud Computing", "EC2", "S3"]
        ),
        Course(
            title="Full Stack Web Development",
            provider="Coursera",
            url="https://coursera.org/fullstack",
            duration="60 hours",
            level="Beginner",
            skills_covered=["HTML", "CSS", "JavaScript", "Node.js", "MongoDB"]
        ),
        Course(
            title="Data Science Specialization",
            provider="Coursera",
            url="https://coursera.org/data-science",
            duration="100 hours",
            level="Intermediate",
            skills_covered=["Data Science", "R", "Python", "Machine Learning", "SQL"]
        ),
        Course(
            title="Advanced SQL for Data Analysis",
            provider="DataCamp",
            url="https://datacamp.com/sql-advanced",
            duration="16 hours",
            level="Advanced",
            skills_covered=["SQL", "PostgreSQL", "Data Analysis"]
        ),
        Course(
            title="FastAPI - Modern Python Web Development",
            provider="TestDriven.io",
            url="https://testdriven.io/fastapi",
            duration="20 hours",
            level="Intermediate",
            skills_covered=["FastAPI", "Python", "REST API", "Docker"]
        ),
        Course(
            title="TypeScript: The Complete Developer's Guide",
            provider="Udemy",
            url="https://udemy.com/typescript-complete",
            duration="25 hours",
            level="Intermediate",
            skills_covered=["TypeScript", "JavaScript", "React"]
        ),
    ]

    @staticmethod
    def recommend_courses(missing_skills: List[str], limit: int = 5) -> List[Course]:
        """Recommend courses based on missing skills"""
        recommendations = []
        skill_set = set([skill.lower() for skill in missing_skills])

        for course in CourseRecommender.COURSES_DB:
            # Check if any course skill matches missing skills
            course_skills = set([skill.lower() for skill in course.skills_covered])
            if skill_set.intersection(course_skills):
                recommendations.append(course)

        # Sort by number of matching skills (descending)
        recommendations.sort(
            key=lambda c: len(set([s.lower() for s in c.skills_covered]).intersection(skill_set)),
            reverse=True
        )

        return recommendations[:limit]


course_recommender = CourseRecommender()
