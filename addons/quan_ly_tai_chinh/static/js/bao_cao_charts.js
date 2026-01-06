// static/src/js/bao_cao_charts.js
odoo.define('quan_ly_tai_chinh.bao_cao_charts', function (require) {
    "use strict";
    
    var core = require('web.core');
    var Widget = require('web.Widget');
    var registry = require('web.view_registry');
    
    var _t = core._t;
    
    var BaoCaoChart = Widget.extend({
        template: 'BaoCaoChart',
        events: {
            'click .chart-refresh': '_onRefreshChart',
        },
        
        init: function (parent, data) {
            this._super(parent);
            this.chartData = JSON.parse(data || '{}');
            this.chart = null;
        },
        
        start: function () {
            this._super();
            this._renderChart();
            return this;
        },
        
        _renderChart: function () {
            var self = this;
            var ctx = this.$el.find('canvas')[0];
            
            if (!ctx) return;
            
            // Destroy existing chart
            if (this.chart) {
                this.chart.destroy();
            }
            
            // Create new chart
            var chartType = this.$el.hasClass('chart-bar') ? 'bar' : 'pie';
            
            var options = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                var label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== undefined) {
                                    label += new Intl.NumberFormat('vi-VN', {
                                        style: 'currency',
                                        currency: 'VND'
                                    }).format(context.parsed.y);
                                } else {
                                    label += new Intl.NumberFormat('vi-VN', {
                                        style: 'currency',
                                        currency: 'VND'
                                    }).format(context.parsed);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: chartType === 'bar' ? {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return new Intl.NumberFormat('vi-VN', {
                                    style: 'currency',
                                    currency: 'VND'
                                }).format(value);
                            }
                        }
                    }
                } : {}
            };
            
            this.chart = new Chart(ctx, {
                type: chartType,
                data: this.chartData,
                options: options
            });
        },
        
        _onRefreshChart: function () {
            this._renderChart();
        },
    });
    
    // Register chart widget
    core.action_registry.add('bao_cao_chart', BaoCaoChart);
    
    return {
        BaoCaoChart: BaoCaoChart,
    };
});