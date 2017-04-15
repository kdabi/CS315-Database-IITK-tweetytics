
google.charts.load('current', {'packages':['corechart']});

function drawBarChart() {
  var options = {
    title : "Word Popularity Comparison",
    width : 795,
    height: 400,
    bar: {groupWidth: "95%"},
    legend: {position: "none"}
  };
  var arr = [['Word','Popularity']];
  $.ajax({
    url: '/app1/Word\ compare',
    type: 'POST',
    data: $('#word_form').serializeArray(),
    success:function(rt_data){
      for (var key in rt_data){
        arr.push([key,rt_data[key]]);
      }
      var data = google.visualization.arrayToDataTable(arr);
      var view = new google.visualization.DataView(data);
      var chart = new google.visualization.BarChart(document.getElementById('bar_div'));
      chart.draw(view, options);
    }
  });
  return false;
}

var form_bt = document.getElementById('button_form');

if(form_bt.attachEvent){
  form_bt.attachEvent("click", drawBarChart);
} else {
  form_bt.addEventListener("click", drawBarChart);
}

