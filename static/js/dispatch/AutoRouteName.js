$('.inputRoute').change(function(){
    let departure = $('#route_departure').val();
    let arrival = $('#route_arrival').val();
    let stopover = $('#route_stopover').val();
    let a = `${departure} > ${stopover} > ${arrival}`
    $('#routeName').val(a);
})