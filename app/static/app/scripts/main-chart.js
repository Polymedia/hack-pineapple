/**
 * Created by balkarov on 08.07.2016.
 */
$(function () {
    var containerID = '#container';

    $(containerID).highcharts({
        chart: {
            type: "spline",
            backgroundColor: "#000000"
        },
        credits: {enabled: false},
        exporting: {enabled: false},
        title: {
            text: null
        },
        subtitle: {
            text: null
        },
        xAxis: {
            tickmarkPlacement: 'on',
            gridLineColor: "#999999",
            gridLineWidth: 1,
            lineWidth: 0,
            gridLineDashStyle: 'ShortDot',
            title: {
                text: "Возраст",
                style: {
                    fontSize: "14px",
                    fontFamily: "Arial",
                    color: "#999999"
                }
            },
            categories: ["35", "37", "39", "41", "43", "45", "47", "49", "51", "53", "55", "57", "59", "61"],
            labels: {
                style: {
                    fontSize: "14px",
                    fontFamily: "Arial",
                    color: "#999999"
                }
            }
        },
        yAxis: {
            lineWidth: 0,
            gridLineWidth: 1,
            gridLineColor: "#999999",
            gridLineDashStyle: 'ShortDot',
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                    return this.value + "%";
                },
                style: {
                    fontSize: "14px",
                    fontFamily: "Arial",
                    color: "#999999"
                }
            }
        },
        legend: {
            enabled: false
        },

        plotOptions: {
            spline: {
                lineWidth: 4,
                marker: {
                    enabled: false
                }
            }
        },
        tooltip: {
            crosshairs: true,
            valueSuffix: '%'
        },
        series: [{
            name: ' ',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
            color: "#810000"
        }
        ]
    });

    $("#smoke-btn").click(function () {
        var chart = $(containerID).highcharts();
        chart.series[0].setData([10.0, 12.9, 1.5, 15.5, 8.2, 1.5, 5.2, 6.5, 53.3, 15.3, 23.9, 4.6]);
    });

    $("#weight-btn").click(function () {
        var chart = $(containerID).highcharts();
        chart.xAxis[0].setCategories(["87", "89", "91", "93", "95", "97", "99", "101", "103", "105", "107", "109", "111", "113"]);
        chart.xAxis[0].axisTitle.attr({
            text: 'Вес'
        });
        setTimeout(function () {
            chart.series[0].setData([40.0, 22.9, 12.5, 45.5, 12.2, 5.5, 23.2, 2.5, 3.3, 45.3, 63.9, 1.6]);
        }, 500);

    });
});