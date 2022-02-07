from fuzzywuzzy import fuzz
import pymorphy2
from questions import faq
morph = pymorphy2.MorphAnalyzer()

def classify_question(text):
    text = ' '.join(morph.parse(word)[0].normal_form for word in text.split())
    questions = list(faq.keys())
    scores = list()
    for question in questions:
        norm_question = ' '.join(morph.parse(word)[0].normal_form for word in question.split())
        scores.append(fuzz.token_sort_ratio(norm_question.lower(), text.lower()))
    answer = faq[questions[scores.index(max(scores))]]

    return answer

