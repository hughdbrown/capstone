var NavViewer = Backbone.View.extend({
    el: 'nav',

    events: {
        "change #chart": "change_chart",
        "change #period": "change_period",
        "change #team": "change_team",
        "change #status": "change_status"
    },

    initialize: function() {
        console.log("NavViewer.initialize");
        this.charts = {
            motion: new MotionChartViewer()
        };
        var default_chart = $('#chart').val();
        this.load_chart(default_chart);
    },

    load_chart: function(new_chart_name) {
        var old_chart_name = this.current_chart;
        console.log("NavViewer.load_chart from '" + old_chart_name + "' to '" + new_chart_name + "'");

        if (this.active_view && this.active_view.unload) {
            this.active_view.unload();
        }
        this.current_chart = new_chart_name;
        this.active_view = this.charts[(this.current_chart = new_chart_name)];
        $(this.active_view.el).html("");
        this.active_view.load();
    },

    change_chart: function(e) {
        var new_chart_name = $('#chart').val();
        this.load_chart(new_chart_name);
    },
    change_period: function(e) {
        var _period = $('#period').val();
        console.log("NavViewer.change_period to " + _period);
        this.active_view.load();
    },
    change_team: function(e) {
        var _team = $('#team').val();
        console.log("NavViewer.change_team to "+ _team);
        this.active_view.load();
    },
    change_status: function(e) {
        var _status = $('#status').val();
        console.log("NavViewer.change_status to " + _status);
        this.active_view.load();
    }
});
