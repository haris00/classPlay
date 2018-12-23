function populateChart(chart)
{
    // https://www.chartjs.org/docs/latest/charts/bar.html
    // to further change the properties of the chart, use the above link
    var ctx = document.getElementById("chart");
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chart["x"],
        xAxisID: 'Options',
        yAxisID: 'percent of students',
        datasets: [{
            label: 'Options',
            data: chart["y"],
            borderWidth: 1,
            backgroundColor: bar_color_list(chart["x"], chart["correct_answers"])
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    min: 0,
                    max: 100
                }
            }]
        }
    }
});
}

function bar_color_list(options, correct_answers)
{
    var bar_color_list = [];
    options.forEach(function(option) {
        if (correct_answers.includes(option)){
        bar_color_list.push('rgba(0, 255, 0, 0.3)');
        }
        else {
        bar_color_list.push('rgba(255, 0, 0, 0.3)');
        }
  });

  return bar_color_list;
}