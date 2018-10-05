from flask import redirect, url_for


def user_redirect(current_user):
    # TODO: Find a better way to find out what type of user it is.
    # Accessing protected members directly is not a good idea.
    user_type = current_user.query._primary_entity._label_name
    if user_type is "Student":
        return redirect(url_for('student.student_account', id=current_user.id))
    elif user_type is "Professor":
        return redirect(url_for('professor.professor_account', id=current_user.id))
