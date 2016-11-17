let get_vars = function() {
    let x_axis = $('#x_axis').find(":selected").val()
    let y_axis = $('#y_axis').find(":selected").val();
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

$(document).ready(function() {

    $("button#generate").click(function() {
        let vars = get_vars();
        send_graph(vars);
    })

    $('select#x_axis').change(function() {
      $('#y_axis').find(':disabled').prop('disabled', false);

      let a_team = $('#x_axis').find(':selected').val()
      $('#y_axis [value="' + a_team + '"]').prop('disabled', true);
    })

    $('select#y_axis').change(function() {
      $('#x_axis').find(':disabled').prop('disabled', false);

      let a_team = $('#y_axis').find(':selected').val()
      $('#x_axis [value="' + a_team + '"]').prop('disabled', true);
    })

})
