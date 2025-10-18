import sys
sys.path.insert(0, 'backend')

from app.services.career_knowledge import career_kb

# Test the knowledge base directly
test_messages = [
    "how can i become an AI engineer",
    "AI engineer",
    "hello",
    "interview tips"
]

for msg in test_messages:
    response = career_kb.get_response(msg)
    print(f"\nInput: {msg}")
    print(f"Response: {response}")
    print("-" * 80)
