odoo.define('quan_ly_tai_chinh.dashboard_charts', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    // Widget to handle chart rendering
    publicWidget.registry.FinanceDashboardCharts = publicWidget.Widget.extend({
        selector: '.o_finance_dashboard',

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._loadCharts();
            });
        },

        _loadCharts: function () {
            var self = this;

            // Load Chart.js from CDN
            if (typeof Chart === 'undefined') {
                var script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js';
                script.onload = function () {
                    self._fetchAndRender();
                };
                document.head.appendChild(script);
            } else {
                self._fetchAndRender();
            }
        },

        _fetchAndRender: function () {
            var self = this;

            rpc.query({
                model: 'dashboard.tai.chinh',
                method: 'get_chart_data',
                args: []
            }).then(function (data) {
                self._renderCharts(data);
            }).catch(function (error) {
                console.log('Error loading chart data:', error);
                self._renderCharts(self._getDefaultData());
            });
        },

        _getDefaultData: function () {
            return {
                approval_status: { labels: ['Chờ duyệt', 'Đã duyệt', 'Từ chối'], values: [0, 0, 0] },
                asset_status: { labels: ['Đang khấu hao', 'Tạm dừng', 'Hoàn thành'], values: [0, 0, 0] },
                depreciation_trend: {
                    labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
                    values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                purchase_trend: {
                    labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
                    values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            };
        },

        _renderCharts: function (data) {
            var self = this;

            // Chart 1: Approval Status
            var approvalCtx = this.$('#approvalStatusChart')[0];
            if (approvalCtx) {
                new Chart(approvalCtx.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: data.approval_status.labels,
                        datasets: [{
                            data: data.approval_status.values,
                            backgroundColor: ['#f59e0b', '#22c55e', '#ef4444'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { padding: 15, font: { size: 11 } }
                            }
                        }
                    }
                });
            }

            // Chart 2: Asset Status
            var assetCtx = this.$('#assetStatusChart')[0];
            if (assetCtx) {
                new Chart(assetCtx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: data.asset_status.labels,
                        datasets: [{
                            label: 'Số lượng',
                            data: data.asset_status.values,
                            backgroundColor: ['#4361ee', '#f59e0b', '#22c55e'],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // Chart 3: Depreciation Trend
            var depreciationCtx = this.$('#depreciationTrendChart')[0];
            if (depreciationCtx) {
                new Chart(depreciationCtx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: data.depreciation_trend.labels,
                        datasets: [{
                            label: 'Khấu hao',
                            data: data.depreciation_trend.values,
                            borderColor: '#4361ee',
                            backgroundColor: 'rgba(67, 97, 238, 0.1)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // Chart 4: Purchase Trend
            var purchaseCtx = this.$('#purchaseTrendChart')[0];
            if (purchaseCtx) {
                new Chart(purchaseCtx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: data.purchase_trend.labels,
                        datasets: [{
                            label: 'Mua sắm',
                            data: data.purchase_trend.values,
                            borderColor: '#22c55e',
                            backgroundColor: 'rgba(34, 197, 94, 0.1)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }
        }
    });

    return publicWidget.registry.FinanceDashboardCharts;
});
