function setupTimerCalls(questionTime,professorId,courseId,questionNumber) {
    var timer = new Timer();
    timer.start({countdown: true, startValues: {seconds: questionTime}});
    timer.addEventListener('secondsUpdated', function (e) {
        $('#count_timer').html(timer.getTimeValues().toString());
    });


    $(document).ready(function() {
        // next button
        $('#metrics_timer').find('.nextButton').click(nextQuestion);

        // pause button
        $('#metrics_timer').find('.pauseButton').click(pauseQuestion);

        // on timer-expiry
        timer.addEventListener('targetAchieved', nextQuestion);


        function pauseQuestion() {
        timer.pause();
        }

        function nextQuestion  (){
            console.log("next question");
            data = {
                "professor_id":professorId,
                "course_id":courseId,
                "state": {
                    "question_number":questionNumber+1,
                    "time_limit": "not_set",
                    "status": "running"
                }
            };
           quiz_state_success_function = function(){
                location.assign(location.href);
            };
            setQuizState(data,quiz_state_success_function);
        }
    });
}

