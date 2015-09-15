var MotionChartViewer = JenkinsViewer.extend({
    initialize: function() {
        JenkinsViewer.prototype.initialize.call(this);

        console.log("Initializing MotionChart");
        this.base_url = this.server;
        this.chart = null;
        this.container = $(this.el)[0];
    },

    load: function() {
        var width = this.width,
            height = this.height;
        var container = this.container;
        var url = this.build_url();
        var that = this;

        function drawVisualization() {
            console.log("drawVisualization " + url);
            $.getJSON(url)
            .done(function (data) {
                /* Coerce to Date */
                var mapped_data = _.map(data, function(row){
                    /*
                    {"count": 7147, "minute": 9, "day": 27, "hour": 8, "country": "US"}
                    */
                    //var date = new Date(2015, 2, row.day, row.hour, row.minute);
                    var date = new Date(2015, 2, (row.day - 25) * 240 + (row.hour * 10) + row.minute, 0, 0); // row.hour, row.minute);
                    return [row.country, date, row.count];
                });
                console.log("Mapped items: " + mapped_data.length);

                console.log("Creating datatable");
                var data_table = new google.visualization.DataTable();
                data_table.addColumn('string', 'Country');
                data_table.addColumn('date', 'Date');
                data_table.addColumn('number', 'Count');
                var filtered = _.filter(mapped_data, function(row){
                    return row[0] == 'US' || row[0] == 'DE' || row[0] == 'IT' || row[0] == 'ES';
                });
                // data_table.addRows(mapped_data);
                data_table.addRows(filtered);

                console.log("Creating MotionChart");
                that.chart = new google.visualization.MotionChart(container);

                console.log("Drawing MotionChart in container");
                var options = {
                    showChartButtons: true,
                    showHeader: true,
                    showSidePanel: true,
                    state: '{"xLambda":1,"yZoomedIn":false,"xAxisOption":"_TIME","xZoomedIn":false,"duration":{"multiplier":1,"timeUnit":"D"},"yZoomedDataMin":43,"uniColorForNonSelected":false,"yAxisOption":"2","xZoomedDataMax":1489881600000,"yLambda":1,"dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMin":1427760000000,"showTrails":true,"orderedByX":false,"orderedByY":false,"iconType":"BUBBLE","nonSelectedAlpha":0.4,"time":"2017-03-19","iconKeySettings":[],"colorOption":"_UNIQUE_COLOR","playDuration":15000,"sizeOption":"2","yZoomedDataMax":9438}',
                    width: width,
                    height: height
                };
                that.chart.draw(data_table, options);
                console.log("Done");
            });
        }

        google.load("visualization", "1", {packages:["motionchart"]});
        google.setOnLoadCallback(drawVisualization);
    },

    unload: function() {
        this.chart = null;
    }
});
