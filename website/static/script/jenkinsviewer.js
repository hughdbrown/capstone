var JenkinsViewer = Backbone.View.extend({
    el: '#container',
    // server: "http://dmc358.mc.wgenhq.net:5000",
    server: "http://localhost:8000",
    url_fragment: function() {
        /***
        var _period = $('#period').val();
        var _team = $('#team').val();
        var _status = $('#status').val();
        return "when=" + _period +
            (_team === "all" ? "" : ("&" + "team=" + _team)) +
            (_status === "" ? "" : ("&" + "status=" + _status));
        ***/
        return "timestamp";
    },
    build_url: function() {
        /***
        return this.base_url + "?" + this.url_fragment();
        ***/
        return this.base_url + "/" + this.url_fragment();
    },
    initialize: function () {
        this.margin = {top: 8, right: 0, bottom: 0, left: 0};
        this.width = 1200 - this.margin.left - this.margin.right;
        this.height = 800 - this.margin.top - this.margin.bottom - 60;
        this.container = d3.select(this.el);

        /* style the container */
        this.container
            .style("position", "relative")
            .style("width", this.width + "px")
            .style("height", this.height + "px")
            .style("left", this.margin.left + "px")
            .style("top", this.margin.top + "px")
            .style("border", "1px solid black");
    }
});
