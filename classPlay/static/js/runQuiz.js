function setupStateCalls(questionTime,professor_id,course_id,question_number) {
    quiz_state = getQuizState(professor_id, course_id);
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
    "professor_id":professor_id,
    "course_id":course_id,
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
        "professor_id":professor_id,
        "course_id":course_id,
        "state": {
            "status":"paused",
            "time_limit": remainingTime
        }
    };
       quiz_state_success_function = function(timer){
        timer.pause();
    };
    setQuizState(data,quiz_state_success_function(timer));
    });

    });

    // on timer-expiry
    timer.addEventListener('targetAchieved', function (e) {
           data = {
            "professor_id":professor_id,
            "course_id":course_id,
            "state": {
                "question_number":question_number+1,
                "time_limit": "not_set"
            }
        };
           quiz_state_success_function = function(){
           location.assign(location.href);
        };
        setQuizState(data,quiz_state_success_function);

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

function getQuizState(professor_id, course_id) {
    var quiz_state = {};
    jQuery.ajax ({
        url: "/professor/api/get_quiz_state",
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

