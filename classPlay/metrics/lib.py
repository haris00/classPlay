from classPlay.quiz.models import Quiz, QuizRun, StudentQuizRunAnswers, StudentQuizRunQuestionAttempt
from classPlay.question.models import Question, QuizQuestion, MCQ, MCQAnswers
from classPlay.course.models import Course, StudentCourse
from classPlay.student.models import Student
from classPlay import db
from copy import deepcopy


def all_students_scores(course_id):
    """returns data in same format as student_scores function but also adds student first name, last name and email.
    For example:
        all_student_scores = [ {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "scores":  student_scores(student_id, course_id)
        }]"""
    student_ids = db.session.query(Student.id, Student.first_name, Student.last_name, Student.email).join(StudentCourse).filter(StudentCourse.course_id == course_id)
    all_student_scores = list()
    for student_id, first_name, last_name, email in student_ids:
        student_score = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "scores":  student_scores(student_id, course_id)
        }
        all_student_scores.append(deepcopy(student_score))


def student_scores(student_id, course_id):
    """To return data in the following format (example)
    [
    {"quiz_number":1,
     "quiz_runs" : [
        {
            "quiz_run_number":1,
            "marks":22
        },
        {
            "quiz_run_number":2,
            "marks":22
        }
    ]
    },
    {"quiz_number":2,
     "quiz_runs" : [
        {
            "quiz_run_number":1,
            "marks":22
        },
        {
            "quiz_run_number":2,
            "marks":22
        }
    ]
    }

    ]
    """
    quiz_run_data = db.session.query(Course.id, Quiz.quiz_number, QuizRun.run_number, QuizRun.id).distinct().join(Quiz, QuizRun, StudentQuizRunQuestionAttempt).filter(Course.id == course_id, StudentQuizRunQuestionAttempt.student_id == student_id).all()
    if not quiz_run_data:
        # No quiz was attempted
        return None
    student_scores = list()
    quiz_runs = list()
    last_quiz_number = quiz_run_data[0][1]
    for course_id, quiz_number, quiz_run_number, quiz_run_id in quiz_run_data:
        if last_quiz_number != quiz_number:
            student_scores.append({"quiz_number": last_quiz_number,
                                   "quiz_runs": deepcopy(quiz_runs)})
            quiz_runs = list()
            last_quiz_number = quiz_number

        quiz_runs.append({"quiz_run_number":quiz_run_number,
                          "marks": quiz_run_result(student_id, quiz_run_id)})


    student_scores.append({"quiz_number": last_quiz_number,
                           "quiz_runs": deepcopy(quiz_runs)})

    return student_scores


def quiz_run_result(student_id, quiz_run_id):
    """Returns the number of correct and wrong answer by student in a quiz run in the following format
    {
        "correct_answers": 0,
        "incorrect_answers": 0
    }
    """
    student_quiz_run_question_attempt_any = StudentQuizRunQuestionAttempt.query. \
        filter_by(quiz_run_id=quiz_run_id, student_id=student_id).first()
    if not student_quiz_run_question_attempt_any:
        # Means that student did not attempt this specific quiz run at all
        return None

    quiz_run_results = {
        "correct_answers": 0,
        "incorrect_answers": 0
    }
    quiz_run = QuizRun.query.filter_by(id=quiz_run_id).first()
    quiz_id = quiz_run.quiz_id
    questions = db.session.query(Question).join(QuizQuestion).\
        filter(QuizQuestion.quiz_id == quiz_id).all()
    for question in questions:
        is_answer_correct_ = is_answer_correct(student_id, question.id, quiz_run_id)
        if is_answer_correct_ is None:
            # If a student did not answer the question, we assume it as incorrect
            quiz_run_results["incorrect_answers"] += 1
        else:
            if is_answer_correct_:
                quiz_run_results["correct_answers"] += 1
            else:
                quiz_run_results["incorrect_answers"] += 1

    return quiz_run_results


def is_answer_correct(student_id, question_id, quiz_run_id):
    """Returns true if answer to the question was correct.
    Returns False if answer (even one of them) was incorrect.
    Returns None if question was not attempted by the student"""
    question = Question.query.filter_by(id=question_id).first()
    question_type = question.question_type
    student_quiz_run_question_attempt = StudentQuizRunQuestionAttempt.query. \
        filter_by(quiz_run_id=quiz_run_id, student_id=student_id, question_id=question_id).first()
    if not student_quiz_run_question_attempt:
        # Means that student did not attempt this specific question in this specific quiz run at all
        return None
    answers = StudentQuizRunAnswers.query. \
        filter_by(student_quiz_run_question_attempt_id=student_quiz_run_question_attempt.id).all()

    if question_type == 'MCQ':
        mcq = MCQ.query.filter_by(id=question_id).first()
    for answer in answers:
        mcq_answer = MCQAnswers.query.filter_by(question_id=mcq.id, id=answer.answer_id).first()
        if not mcq_answer.correct_answer:
            return False

    return True


def answers_selected(quiz_run_id, question_id):
    student_quiz_run_question_attempts = StudentQuizRunQuestionAttempt.query.filter_by(quiz_run_id=quiz_run_id,
                                                                                       question_id=question_id).all()
    answer_id_count = dict()
    for student_quiz_run_question_attempt in student_quiz_run_question_attempts:
        student_quiz_answers = StudentQuizRunAnswers.query.filter_by(
            student_quiz_run_question_attempt_id=student_quiz_run_question_attempt.id).all()
        for student_quiz_answer in student_quiz_answers:
            answer_id_count[student_quiz_answer.answer_id] = answer_id_count.get(student_quiz_answer.answer_id, 0) + 1

    # marking the remaining ids (which none of the students answered) as zero
    question = Question.query.filter_by(id=question_id).first()
    if question.question_type == 'MCQ':
        mcq = MCQ.query.filter_by(question_id=question.id).first()
        mcq_answers = MCQAnswers.query.filter_by(question_id=mcq.id).all()
    for mcq_answer in mcq_answers:
        answer_id_count[mcq_answer.id] = answer_id_count.get(mcq_answer.id, 0)

    # convert to percentages
    total_answers = sum(answer_id_count.values())
    for option, answer_count in answer_id_count.iteritems():
        try:
            answer_id_count[option] = (answer_count/float(total_answers)) * 100
        except ZeroDivisionError:
            answer_id_count[option] = 0;

    return answer_id_count


def get_correct_answers(question_id, correct_answer=True):
    """Returns all the correct or incorrect answers (depending on correct_answer argument input)"""
    correct_answers = list()
    question = Question.query.filter_by(id=question_id).first()
    question_type = question.question_type
    if question_type == 'MCQ':
        mcq = MCQ.query.filter_by(question_id=question.id).first()
        mcq_answers = MCQAnswers.query.filter_by(question_id=mcq.id, correct_answer=correct_answer).all()
        for mcq_answer in mcq_answers:
            correct_answers.append(mcq_answer.id)

    return correct_answers
