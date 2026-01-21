odoo.define('quan_ly_tai_chinh.dashboard_tai_chinh', function(require) {
    'use strict';

    const FormController = require('web.FormController');
    const rpc = require('web.rpc');

    FormController.include({
        _onLoadRecord: function() {
            const self = this;
            this._super(...arguments);
            
            if (this.modelName === 'dashboard.tai.chinh') {
                // Delay vẽ biểu đồ sau khi DOM render xong
                setTimeout(() => {
                    self._initChartsIfNeeded();
                }, 100);
            }
        },

        _initChartsIfNeeded: function() {
            if (typeof Chart === 'undefined') {
                console.warn('Chart.js library not found. Charts will not be displayed.');
                return;
            }

            try {
                this._drawApprovalStatusChart();
                this._drawAssetStatusChart();
                this._drawDepreciationTrendChart();
                this._drawPurchaseTrendChart();
            } catch (error) {
                console.error('Error initializing charts:', error);
            }
        },

        _drawApprovalStatusChart: function() {
            const ctx = document.getElementById('approvalStatusChart');
            if (!ctx) return;

            const data = {
                labels: ['Chờ Duyệt', 'Đã Duyệt', 'Từ Chối', 'Hoàn Thành'],
                datasets: [{
                    data: [
                        this.record.data.phe_duyet_cho_duyet || 0,
                        this.record.data.phe_duyet_da_duyet || 0,
                        this.record.data.phe_duyet_bi_tu_choi || 0,
                        this.record.data.phe_duyet_hoan_thanh || 0
                    ],
                    backgroundColor: [
                        '#FFC107',
                        '#28A745',
                        '#DC3545',
                        '#17A2B8'
                    ],
                    borderColor: [
                        '#FFB800',
                        '#20C997',
                        '#BB2D3B',
                        '#138496'
                    ],
                    borderWidth: 2
                }]
            };

            if (window.approvalChart) window.approvalChart.destroy();
            window.approvalChart = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { padding: 15, font: { size: 12 } }
                        }
                    }
                }
            });
        },

        _drawAssetStatusChart: function() {
            const ctx = document.getElementById('assetStatusChart');
            if (!ctx) return;

            const data = {
                labels: ['Đang Khấu Hao', 'Hoạt Động', 'Thanh Lý'],
                datasets: [{
                    data: [
                        this.record.data.tai_san_dang_khau_hao || 0,
                        (this.record.data.tong_tai_san || 0) - (this.record.data.tai_san_dang_khau_hao || 0),
                        0
                    ],
                    backgroundColor: [
                        '#007BFF',
                        '#6C757D',
                        '#FFC107'
                    ],
                    borderColor: [
                        '#0056B3',
                        '#545B62',
                        '#FFB800'
                    ],
                    borderWidth: 2
                }]
            };

            if (window.assetChart) window.assetChart.destroy();
            window.assetChart = new Chart(ctx, {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { padding: 15, font: { size: 12 } }
                        }
                    }
                }
            });
        },

        _drawDepreciationTrendChart: function() {
            const ctx = document.getElementById('depreciationTrendChart');
            if (!ctx) return;

            const trends = this.record.data.depreciation_trend_ids || [];
            const labels = trends.map(t => t.data ? t.data.month : '').sort();
            const amounts = [];
            
            labels.forEach(month => {
                const trend = trends.find(t => (t.data ? t.data.month : '') === month);
                amounts.push((trend && trend.data ? trend.data.amount : 0) / 1000000);
            });

            if (window.depreciationChart) window.depreciationChart.destroy();
            window.depreciationChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Khấu Hao (Triệu VNĐ)',
                        data: amounts,
                        borderColor: '#007BFF',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 5,
                        pointBackgroundColor: '#007BFF',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            labels: { padding: 15, font: { size: 12 } }
                        }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        },

        _drawPurchaseTrendChart: function() {
            const ctx = document.getElementById('purchaseTrendChart');
            if (!ctx) return;

            const trends = this.record.data.purchase_trend_ids || [];
            const labels = trends.map(t => t.data ? t.data.month : '').sort();
            const purchaseAmounts = [];
            const approvedAmounts = [];

            labels.forEach(month => {
                const trend = trends.find(t => (t.data ? t.data.month : '') === month);
                purchaseAmounts.push((trend && trend.data ? trend.data.amount : 0) / 1000000);
                approvedAmounts.push((trend && trend.data ? trend.data.amount_approved : 0) / 1000000);
            });

            if (window.purchaseChart) window.purchaseChart.destroy();
            window.purchaseChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Tổng Đề Xuất (Triệu VNĐ)',
                            data: purchaseAmounts,
                            backgroundColor: 'rgba(255, 193, 7, 0.7)',
                            borderColor: '#FFC107',
                            borderWidth: 2
                        },
                        {
                            label: 'Đã Duyệt (Triệu VNĐ)',
                            data: approvedAmounts,
                            backgroundColor: 'rgba(40, 167, 69, 0.7)',
                            borderColor: '#28A745',
                            borderWidth: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            labels: { padding: 15, font: { size: 12 } }
                        }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
    });
});
