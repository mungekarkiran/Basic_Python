import random

class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

question_prompts = [
    "What color are apples?\n(a) Red/Green\n(b) Purple\n(c) Orange\n\n",
    "What color are bananas?\n(a) Red/Green\n(b) Purple\n(c) Yellow\n\n",
    "What color are strawberries?\n(a) Red\n(b) Blue\n(c) Yellow\n\n",
    "What is the color of sky?\n(a) Red\n(b) Blue\n(c) Yellow\n\n",
    "What is the color of moon?\n(a) Red\n(b) Blue\n(c) White\n\n"
]

questions = [
    Question(question_prompts[0], "a"),
    Question(question_prompts[1], "c"),
    Question(question_prompts[2], "a"),
    Question(question_prompts[3], "b"),
    Question(question_prompts[4], "c")
]

def run_quiz(questions):
    score = 0
    summary = []
    random.shuffle(questions) # randomize the order of questions
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score += 1
            # print("Correct!")
            summary.append([question.prompt.split('\n')[0], answer, "Correct"])
        else:
            # print("Incorrect!")
            summary.append([question.prompt.split('\n')[0], answer, "Incorrect"])
    print(f"\n\nYou got {score}/{len(questions)} questions correct.")
    print(f"Summary : ")
    for ind, summ in enumerate(summary):
        print(f"{ind}: {summ}")

if __name__ == "__main__":
    run_quiz(questions)
