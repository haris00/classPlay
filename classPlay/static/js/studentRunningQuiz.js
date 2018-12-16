function submitAnswer(professorId, courseId, quizId, questionId, question_number){
    var answerIds = [];
    $("input:checkbox[name=answer]:checked").each(function(){
        answerIds.push($(this).val());
    });
    submit_success_function = function(data){
           $('#answer_status').html(data.message);
           $("#answer_status").removeClass();
           console.log(data.submission_status);
           if (data.submission_status == "success"){
                $("#answer_status").addClass("alert alert-success");
                $("#answer_submit_button").attr("disabled", true);
            }
           else if (data.submission_status == "error"){
                $("#answer_status").addClass("alert alert-danger");
                $("#answer_submit_button").attr("disabled", true);
            }
        };
    submit_error_function = function(data){
           console.log("error sending answers");
        };
    sendAnswers(professorId, courseId, quizId, questionId, question_number, answerIds, submit_success_function, submit_error_function);
}

function sendAnswers(professorId, courseId, quizId, questionId, question_number, answerIds, success_function=function(){}, error_function=function(){}) {
    data = {
            "course_id": courseId,
            "professor_id": professorId,
            "question_id": questionId,
            "question_number": question_number,
            "quiz_id": quizId,
            "answer_ids": answerIds
           };
    jQuery.ajax ({
        url: "/quiz/api/submit_answer",
        type: "POST",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: success_function,
        error: error_function});
}