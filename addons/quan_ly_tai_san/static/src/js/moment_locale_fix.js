// File: quan_ly_tai_san/static/src/js/moment_locale_fix.js
odoo.define('quan_ly_tai_san.moment_locale_fix', function (require) {
    "use strict";
    
    // Đảm bảo moment đã được load
    if (typeof moment !== 'undefined') {
        // Kiểm tra và tạo locale vi nếu chưa có
        if (!moment.locales().includes('vi')) {
            moment.defineLocale('vi', {
                months: 'tháng 1_tháng 2_tháng 3_tháng 4_tháng 5_tháng 6_tháng 7_tháng 8_tháng 9_tháng 10_tháng 11_tháng 12'.split('_'),
                monthsShort: 'Thg 1_Thg 2_Thg 3_Thg 4_Thg 5_Thg 6_Thg 7_Thg 8_Thg 9_Thg 10_Thg 11_Thg 12'.split('_'),
                weekdays: 'chủ nhật_thứ hai_thứ ba_thứ tư_thứ năm_thứ sáu_thứ bảy'.split('_'),
                weekdaysShort: 'CN_T2_T3_T4_T5_T6_T7'.split('_'),
                weekdaysMin: 'CN_T2_T3_T4_T5_T6_T7'.split('_'),
                longDateFormat: {
                    LT: 'HH:mm',
                    LTS: 'HH:mm:ss',
                    L: 'DD/MM/YYYY',
                    LL: 'D MMMM [năm] YYYY',
                    LLL: 'D MMMM [năm] YYYY HH:mm',
                    LLLL: 'dddd, D MMMM [năm] YYYY HH:mm',
                },
                calendar: {
                    sameDay: '[Hôm nay lúc] LT',
                    nextDay: '[Ngày mai lúc] LT',
                    nextWeek: 'dddd [tuần tới lúc] LT',
                    lastDay: '[Hôm qua lúc] LT',
                    lastWeek: 'dddd [tuần trước lúc] LT',
                    sameElse: 'L'
                },
                relativeTime: {
                    future: '%s tới',
                    past: '%s trước',
                    s: 'vài giây',
                    ss: '%d giây',
                    m: 'một phút',
                    mm: '%d phút',
                    h: 'một giờ',
                    hh: '%d giờ',
                    d: 'một ngày',
                    dd: '%d ngày',
                    M: 'một tháng',
                    MM: '%d tháng',
                    y: 'một năm',
                    yy: '%d năm'
                },
                dayOfMonthOrdinalParse: /\d{1,2}/,
                ordinal: function (number) {
                    return number;
                },
                week: {
                    dow: 1,
                    doy: 4
                }
            });
            console.log('✅ Đã tạo locale vi cho moment.js');
        }
        
        // Đặt locale mặc định là vi
        moment.locale('vi');
    }
});