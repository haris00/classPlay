function startTimer(questionTime){
    var timer = new Timer();
    timer.start({countdown: true, startValues: {seconds: questionTime}});
    timer.addEventListener('secondsUpdated', function (e) {
        $('#question_timer').html(timer.getTimeValues().toString());
    });
}