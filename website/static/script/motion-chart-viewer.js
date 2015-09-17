var MotionChartViewer = JenkinsViewer.extend({
    initialize: function() {
        JenkinsViewer.prototype.initialize.call(this);

        console.log("Initializing MotionChart");
        this.base_url = this.server + "/data";
        this.chart = null;
        this.container = $(this.el)[0];
    },

    load: function() {
        var width = this.width,
            height = this.height;
        var container = this.container;
        var url = this.build_url();
        var that = this;

        that.called = false;
        console.log("MotionCharViewer.load");
        function drawVisualization() {
            console.log("drawVisualization " + url);

            $.getJSON(url).done(function (data) {
                console.log("1");
                var mapped_data = _.map(data, function(data){
                    /*
                    {"count": 5256, "minute": 7, "day": 27, "key": "United States of America", "hour": 22}
                    */
                    //var date = new Date(2015, 2, row.day, row.hour, row.minute);
                    try {
                        var day = data.day, hour = data.hour, minute = data.minute;
                        var date = new Date(2015, 2, (day - 25) * 240 + (hour * 10) + minute, 0, 0);
                        return [data.key, date, data.count];
                    }
                    catch(err){
                        console.log(err);
                    }
                });
                console.log("Mapped items: " + mapped_data.length);

                console.log("Creating datatable");
                var data_table = new google.visualization.DataTable();
                data_table.addColumn('string', 'Key');
                data_table.addColumn('date', 'Date');
                data_table.addColumn('number', 'Count');
                data_table.addRows(mapped_data);

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
            });
            that.called = true;
        }

        google.load("visualization", "1", {packages:["motionchart"]});
        google.setOnLoadCallback(drawVisualization);
        if (! that.called){
            drawVisualization();
            that.called = false;
        }
    },

    unload: function() {
        this.chart = null;
    }
});