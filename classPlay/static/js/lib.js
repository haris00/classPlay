function convertNumberToLetter(number) {
  var letter = String.fromCharCode(number + 64);
  return letter;
}

function getQuizState(professor_id, course_id) {
    var quiz_state = {};
    jQuery.ajax ({
        url: "/quiz/api/get_quiz_state",
        type: "GET",
        data: { "professor_id": professor_id, "course_id": course_id },
        async: false,
        cache: false,
        timeout: 30000,
        error: function(){
            console.log("Cannot get quiz state");
        },
        success: function( data ) {
        quiz_state = data ;
        }});
    return JSON.parse(quiz_state);
}

function setQuizState(data, success_function=function(){}) {
    jQuery.ajax ({
        url: "/professor/api/set_quiz_state",
        type: "POST",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: success_function});
}
