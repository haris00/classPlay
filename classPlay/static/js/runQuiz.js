function setupStateCalls(questionTime,professorId,courseId,questionNumber) {
    quiz_state = getQuizState(professorId, courseId);
    var timer = new Timer();
    timer.start({countdown: true, startValues: {seconds: questionTime}});
    if (quiz_state['status'] == "paused"){
        timer.pause();
    }
    timer.addEventListener('secondsUpdated', function (e) {
        $('#question_timer').html(timer.getTimeValues().toString());
    });

    // start button
    $(document).ready(function() {
    $('#controls').find('.startButton').click(function () {
      data = {
    "professorId":professorId,
    "course_id":courseId,
    "state": {
        "status":"running",
    }
    };
    quiz_state_success_function = function(timer){
    timer.start();
    };
    setQuizState(data,quiz_state_success_function(timer));
    });

    // pause button
    $('#controls').find('.pauseButton').click(function () {
       var remainingTime = timer.getTimeValues().seconds;
       data = {
        "professor_id":professorId,
        "course_id":courseId,
        "state": {
            "status":"paused",
            "time_limit": remainingTime
        }
    };
       quiz_state_success_function = function(timer){
        timer.pause();
    };
    // TODO: This should only pause the quiz if json return is success
    // it's not behaving like this at the moment. See this
    setQuizState(data,quiz_state_success_function(timer));
    });

    });

    // on timer-expiry
    timer.addEventListener('targetAchieved', function (e) {
           data = {
            "professor_id":professorId,
            "course_id":courseId,
            "state": {
                "status":"displaying_metrics"
            }
        };
           quiz_state_success_function = function(){
           location.assign(location.href);
        };
        setQuizState(data,quiz_state_success_function);


//           data = {
//            "professor_id":professorId,
//            "course_id":courseId,
//            "state": {
//                "question_number":questionNumber+1,
//                "time_limit": "not_set"
//            }
//        };
//           quiz_state_success_function = function(){
//           location.assign(location.href);
//        };
//        setQuizState(data,quiz_state_success_function);

});
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
