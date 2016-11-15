let get_vars = function() {
    let x_axis = $('#x_axis').find(":selected").text()
    let y_axis = $('#y_axis').find(":selected").text();
    return {'x': x_axis,
            'y': y_axis}
};

let send_graph = function(coefficients) {
    $.ajax({
        url: '/graph_binary',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            document.getElementById("graph").src=data;
        },
        data: JSON.stringify(coefficients)
    });
};

// let match_up = function(soln) {
//   $("span#match_up").html(soln.home + ' versus ' + soln.away)
// };
//
// let display_yellows = function(soln) {
//     $("span#yellows").html('Yellows: ' + soln.home_yellow + ' - ' + soln.away_yellow)
// };
//
// let display_reds = function(soln) {
//     $("span#reds").html('Reds: ' + soln.home_red + ' - ' + soln.away_red)
// };


$(document).ready(function() {

    $("button#generate").click(function() {
        let vars = get_vars();
        send_graph(vars);
    })

    $('select#x_axis').change(function() {
        let vars = get_vars();
        send_graph(vars);
    })
})
