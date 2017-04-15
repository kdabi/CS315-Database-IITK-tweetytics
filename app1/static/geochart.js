
google.charts.load('current', {'packages':['geochart']});
google.charts.setOnLoadCallback(drawRegionsMap);

function drawRegionsMap() {

  var options = {
  colorAxis: {colors: ['yellow', 'red']}
  };

  var style = "height:400px; width:750px;";
  var arr = [['Country','Popularity']];
  document.getElementById('regions_div').style = style;
  $.ajax({
    url: '/app1/location',
    dataType: 'json',
    type: 'GET',
    success:function(rt_data){
      for (var key in rt_data){
        arr.push([key,rt_data[key]]);
      }
      var data = google.visualization.arrayToDataTable(arr);
      var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
      chart.draw(data, options);
    }
  });
}

