function startTimer(questionTime) {
    var timer = new Timer();
    timer.start({countdown: true, startValues: {seconds: questionTime}});
    timer.addEventListener('secondsUpdated', function (e) {
        $('#question_timer').html(timer.getTimeValues().toString());
    });

    $(document).ready(function() {
    $('#controls').find('.startButton').click(function () {
    timer.start();
    });

    $('#controls').find('.pauseButton').click(function () {
    timer.pause();
    });

    });

    timer.addEventListener('targetAchieved', function (e) {
        console.log(location.href);
        current_question = parseInt(location.href.substr(-1));
        next_location = location.href.slice(0,-1) + (current_question + 1).toString();
        location.assign(next_location);
});
}

function convertNumberToLetter(number) {
  var letter = String.fromCharCode(number + 64);
  return letter;
}