from classPlay.question.models import QuizQuestion, Question, MCQ, MCQAnswers
from sqlalchemy import asc

def get_quiz_content(quizes, quiz_id=None):
    """Returns data for all quizes. If quiz_id is not none, then provides data just for that quiz"""
    quiz_content_object = []
    for quiz in quizes:
        quiz_content = dict()
        if quiz_id is not None and quiz_id == quiz.id:
            continue
        quiz_content["quiz_id"] = quiz.id
        quiz_content["quiz_number"] = quiz.quiz_number
        quiz_content_object.append(quiz_content)

    for quiz_index, quiz in enumerate(quiz_content_object):
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz["quiz_id"]).all()
        quiz_content_object[quiz_index]["questions"] = []
        for question_index, question in enumerate(quiz_questions):
            question = Question.query.filter_by(id=question.id).first()
            question_content = dict()
            question_content["time_limit"] = question.time_limit
            question_content["question_id"] = question.id
            question_content["question_number"] = question.question_number
            if question.question_type == "MCQ":
                mcq_question = MCQ.query.filter_by(question_id=question.id).first()
                question_content["question_text"] = mcq_question.question_text
                # sorting is MUST to make sure that professor options order and student option order is same
                mcq_answers = MCQAnswers.query.filter_by(question_id=mcq_question.id).\
                    order_by(asc(MCQAnswers.id)).all()
                mcq_options = []
                for mcq_answer in mcq_answers:
                    mcq_options_content = dict()
                    mcq_options_content["option_text"] = mcq_answer.option_text
                    mcq_options_content["correct_answer"] = mcq_answer.correct_answer
                    mcq_options.append(mcq_options_content)
                question_content["mcq_options"] = mcq_options
                quiz_content_object[quiz_index]["questions"].append(question_content)
            else:
                continue

    return quiz_content_object
