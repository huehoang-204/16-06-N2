odoo.define('quan_ly_tai_san.datepicker_fix', function (require) {
    "use strict";

    var DatePicker = require('web.datepicker');
    var DateWidget = DatePicker.DateWidget;
    var DateTimeWidget = DatePicker.DateTimeWidget;

    // Override phương thức init của DateWidget
    DateWidget.include({
        init: function (parent, options) {
            // Gọi hàm gốc trước
            this._super.apply(this, arguments);
            
            // Fix locale option
            if (this.options.locale === 'vi' && typeof moment !== 'undefined') {
                // Kiểm tra xem moment có locale vi không
                if (!moment.locales().includes('vi')) {
                    // Nếu không có, chuyển sang locale en
                    this.options.locale = 'en';
                    console.warn('Moment.js không có locale "vi". Đã chuyển sang "en".');
                }
            }
        },
        
        start: function () {
            // Double check trước khi khởi tạo datetimepicker
            if (this.options.locale === 'vi' && typeof moment !== 'undefined') {
                if (!moment.locales().includes('vi')) {
                    this.options.locale = 'en';
                }
            }
            
            return this._super.apply(this, arguments);
        }
    });

    // Áp dụng tương tự cho DateTimeWidget
    DateTimeWidget.include({
        init: function (parent, options) {
            this._super.apply(this, arguments);
            
            if (this.options.locale === 'vi' && typeof moment !== 'undefined') {
                if (!moment.locales().includes('vi')) {
                    this.options.locale = 'en';
                }
            }
        }
    });
});