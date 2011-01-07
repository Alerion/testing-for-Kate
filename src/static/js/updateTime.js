//Update end times on page every 1 second
//Use: setInterval(updateTime, 1000);
var updateTime = function(){
    var time_template = $.template('${seconds:time}').compile()
    var time_re = /^(\d+):(\d{2}):(\d{2})$/;
    return function(){
        $('.time').each(function(i, item){
            var item = $(item);
            var value = time_re.exec($(item).html());
            value = (value[1]-0) * 3600 + (value[2]-0) * 60 + (value[3]-0);
            (value > 0) && item.html(time_template.apply({seconds: value-1}));
        })
    }
}();