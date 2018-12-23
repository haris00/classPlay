import string


def get_chart_from_answers(answers, correct_answers):
    correct_answer_in_alphabet = list()
    uppercase_string = string.ascii_uppercase
    uppercase_string_index = 0
    sorted_answers_values = sorted(answers.items())
    x = list()
    y = list()
    for chart_values in sorted_answers_values:
        if chart_values[0] in correct_answers:
            correct_answer_in_alphabet.append(uppercase_string[uppercase_string_index])
        x.append(uppercase_string[uppercase_string_index])
        uppercase_string_index +=1
        y.append(chart_values[1])

    return {"x": x,
            "y": y,
            "correct_answers": correct_answer_in_alphabet}
