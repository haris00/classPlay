// writing html inside javascript is very BAD approach.
// We should instead manipulate DOM elements to achieve the desired result
// The following code should be re-factored accordingly
function displayQuestion(quiz_number, question_number, question) {
  question_html = `
  <span><h3>Quiz ${quiz_number}</h3></span>
  <span><h5><i>Question</i> ${question_number}</h5></span>
  <span>${question.question_text}</span>
    <ul class="list-group">
  `;
  question.mcq_options.forEach(function(option) {
    if (option.correct_answer)
       question_html += `<li class="list-group-item active">${option.option_text}</li>`;
    else
        question_html += `<li class="list-group-item">${option.option_text}</li>`;
    });
  question_html += `</ul>`;
  document.getElementById("question").innerHTML = question_html;
}

function navigateToMetrics(courseId, questionId){
  var run_id = ($("#quiz_run_"+String(questionId)).val());
  location.assign(`/professor/course/question_metrics/${courseId}/${run_id}/${questionId}`);
}
