from QASystem.answer_question import Answer
from QASystem.question_classifier import QuestionClassifier


class QA:
    def __init__(self):
        self.extractor = QuestionClassifier()
        self.searcher = Answer()

    def answer(self, input_ques):
        all_query = self.extractor.extractor_question(input_ques)
        if str(all_query) == '-1':
            print("sorry")
            return '-1'
        sqls = self.searcher.question_parser(all_query)
        final_answer = self.searcher.searching(sqls)
        if str(final_answer) == '-1':
            return '-1';
        else:
            return final_answer


def end(question):
    # if __name__ == '__main__':
    handler = QA()

    answer = handler.answer(question)
    if str(answer) == '-1':
        return '-1';
    else:
        return answer
