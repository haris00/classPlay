from classPlay.course.models import Course
from classPlay.quiz.models import Quiz, QuizRun, StudentQuizRunQuestionAttempt, StudentQuizRunAnswers
from classPlay.question.models import QuizQuestion, Question, MCQ, MCQAnswers
from classPlay import db
from sqlalchemy import desc


def create_quiz(course_id):
    last_quiz = Quiz.query.filter_by(course_id=course_id).order_by(desc(Quiz.quiz_number)).limit(1).first()
    quiz_number = 0
    if last_quiz:
        quiz_number = last_quiz.quiz_number
    quiz_number += 1
    quiz = Quiz(quiz_number=quiz_number, course_id=course_id)
    db.session.add(quiz)
    db.session.commit()


def create_quiz_run(quiz_id):
    last_quiz_run = QuizRun.query.filter_by(quiz_id=quiz_id).order_by(desc(QuizRun.run_number)).limit(1).first()
    quiz_run_number = 0
    if last_quiz_run:
        quiz_run_number = last_quiz_run.run_number
    quiz_run_number += 1
    quiz_run = QuizRun(run_number=quiz_run_number, quiz_id=quiz_id)
    db.session.add(quiz_run)
    db.session.flush()
    quiz_run_id = quiz_run.id
    db.session.commit()
    return quiz_run_id


def create_question(course_id, quiz_number, time_limit, question_text, question_type="MCQ"):
    quiz = Quiz.query.filter_by(course_id=course_id, quiz_number=quiz_number).first()
    question_number = 0
    if quiz:
        quiz_id = quiz.id
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        for quiz_question in quiz_questions:
            question_id = quiz_question.id
            question = Question.query.filter_by(id=question_id).first()
            question_number = max(question_number, question.question_number)
        question_number += 1
        question = Question(question_type=question_type, time_limit=time_limit, question_number=question_number)
        db.session.add(question)
        db.session.flush()
        quiz_question = QuizQuestion(question_id=question.id, quiz_id=quiz_id)
        db.session.add(quiz_question)
        db.session.add(question)
        if question_type == "MCQ":
            mcq = MCQ(question_id=question.id, question_text=question_text)
        db.session.add(mcq)
        db.session.commit()


def create_mcq_option(course_id, quiz_number, question_number, option_text, correct_answer):
    # TODO: handle errors if doesn't exist
    quiz = Quiz.query.filter_by(course_id=course_id, quiz_number=quiz_number).first()
    if quiz:
        quiz_id = quiz.id
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        for quiz_question in quiz_questions:
            question_id = quiz_question.id
            question = Question.query.filter_by(id=question_id).first()
            if question.question_number == question_number:
                break
        if question.question_type == "MCQ":
            mcq_option = MCQAnswers(option_text=option_text, correct_answer=correct_answer, question_id=question_id)
        db.session.add(mcq_option)
        db.session.commit()


def insert_student_quiz_attempt_answer(student_id, question_id, quiz_run_id, answer_ids):
    student_quiz_run_question_attempt = StudentQuizRunQuestionAttempt(student_id=student_id,
                                                                      quiz_run_id=quiz_run_id, question_id=question_id)
    db.session.add(student_quiz_run_question_attempt)
    db.session.flush()
    student_quiz_run_question_attempt_id = student_quiz_run_question_attempt.id
    for answer_id in answer_ids:
        student_quiz_run_answers = StudentQuizRunAnswers(
            student_quiz_run_question_attempt_id=student_quiz_run_question_attempt_id, answer_id=int(answer_id))
        db.session.add(student_quiz_run_answers)
    db.session.commit()