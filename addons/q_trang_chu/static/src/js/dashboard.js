/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, useState, hooks } = owl;
const { onMounted, onWillStart } = hooks;

class DashboardMain extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            loading: true,
            data: {
                tai_san: {},
                tai_chinh: {},
                muon_tra: {},
                hoat_dong_gan_day: [],
                thong_bao: [],
            },
            charts: {},
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });

        onMounted(() => {
            this.initCharts();
            // Refresh data every 30 seconds
            this.refreshInterval = setInterval(() => {
                this.loadDashboardData();
                this.initCharts();
            }, 30000);
        });
        
        // Cleanup on component destroy
        hooks.onWillUnmount(() => {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
        });
    }

    async loadDashboardData() {
        try {
            // Clear the loading state
            this.state.loading = true;
            
            // Call the backend method
            const data = await this.orm.call(
                "dashboard.main",
                "get_dashboard_data",
                []
            );
            
            // Update state with fetched data
            this.state.data = {
                tai_san: data.tai_san || {},
                tai_chinh: data.tai_chinh || {},
                muon_tra: data.muon_tra || {},
                hoat_dong_gan_day: data.hoat_dong_gan_day || [],
                thong_bao: data.thong_bao || [],
            };
            this.state.loading = false;
            
            console.debug("Dashboard data loaded successfully:", this.state.data);
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.data = {
                tai_san: { total: 0, active: 0, dang_muon: 0, total_value: 0, depreciated_value: 0 },
                tai_chinh: {},
                muon_tra: { don_cho_duyet: 0, don_dang_muon: 0, qua_han: 0 },
                hoat_dong_gan_day: [],
                thong_bao: [],
            };
            this.state.loading = false;
        }
    }

    async initCharts() {
        try {
            const assetsByCategory = await this.orm.call(
                "dashboard.main",
                "get_chart_data",
                ["tai_san_theo_danh_muc"]
            );
            this.state.charts.assetsByCategory = assetsByCategory;

            const borrowingByMonth = await this.orm.call(
                "dashboard.main",
                "get_chart_data",
                ["muon_tra_theo_thang"]
            );
            this.state.charts.borrowingByMonth = borrowingByMonth;
        } catch (error) {
            console.error("Error loading chart data:", error);
        }
    }

    formatNumber(value) {
        if (!value) return "0";
        return new Intl.NumberFormat("vi-VN").format(value);
    }

    formatCurrency(value) {
        if (!value) return "0 ₫";
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND",
        }).format(value);
    }

    openTaiSan() {
        this.action.doAction("quan_ly_tai_san.tai_san_action");
    }

    openDonMuon() {
        this.action.doAction("quan_ly_tai_san.don_muon_tai_san_action");
    }

    openMuonTra() {
        this.action.doAction("quan_ly_tai_san.muon_tra_tai_san_action");
    }

    openPheDuyet() {
        this.action.doAction("quan_ly_tai_chinh.action_phe_duyet_mua_tai_san");
    }

    openKiemKe() {
        this.action.doAction("quan_ly_tai_san.kiem_ke_tai_san_action");
    }

    handleNotificationClick(notification) {
        if (notification.action === "don_muon_tai_san") {
            this.openDonMuon();
        } else if (notification.action === "muon_tra_tai_san") {
            this.openMuonTra();
        }
    }

    async refreshDashboard() {
        // Manually refresh dashboard data
        await this.loadDashboardData();
        await this.initCharts();
    }
}

DashboardMain.template = "q_trang_chu.DashboardMain";

registry.category("actions").add("q_trang_chu.dashboard_action", DashboardMain);
