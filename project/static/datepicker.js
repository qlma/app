
$('#picker_start_time').datetimepicker({
    timepicker: true,
    datepicker: true,
    format: 'Y-m-d H:i',
    weeks: true,
    hours12: true,
    step: 5,
    disabledWeekDays: [5,6],
    allowTimes: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
    onShow: function(ct){
        this.setOptions({
        maxDate: $('#picker_end_time').val() ? $('#picker_end_time').val() : false
        })
    }
})
$('#picker_end_time').datetimepicker({
    timepicker: true,
    datepicker: true,
    format: 'Y-m-d H:i',
    weeks: true,
    hours12: true,
    step: 5,
    disabledWeekDays: [5,6],
    allowTimes: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
    onShow: function(ct){
        this.setOptions({
        minDate: $('#picker_start_time').val() ? $('#picker_start_time').val() : false
        })
    }
});