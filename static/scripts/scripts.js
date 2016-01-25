var data_establishment;
var data_graph = [];
$(function(){
	$("#search-establishment").click(function(){
		data_graph = []
		$(".loading").show();
		from = $("#from").val();
		to = $("#to").val();
		data_graph.push(["Año","Establecimientos"]);
		$.get( "/api/establecimientos", { from: from, to: to },  function( data ) {
			if (data != 'not-data'){
	    		data_establishment = JSON.parse(data);
	    		$.each(data_establishment.data, function( index, value ) {
	    			data_temp = [value.year,parseInt(value.total)]
	    			data_graph.push(data_temp)
	    		});
	    		// alert(data_graph)
			  	// $(".body").html(data_graph);
			  	drawChart(data_graph);
			  	$(".loading").hide();
		  	}
		  	else{
		  		$(".loading").hide();
		  		$(".body").html("No existen datos");
		  	}
		});
	});
});
// Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      // google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart(data_graph) {

        // Create the data table.
        var data = new google.visualization.arrayToDataTable(data_graph);


        // Set chart options
        var options = {
          title: "Número de establecimientos por año",
          legend: { position: 'none' },
          'height':300
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }