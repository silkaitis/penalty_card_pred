let get_vars = function() {
    let heat_x = $('#heat_x').find(":selected").val()
    let heat_xn = $('#heat_x').find(":selected").text()
    let heat_y = $('#heat_y').find(":selected").val()
    let heat_yn = $('#heat_y').find(":selected").text()
    let heat_v = $('#heat_v').find(":selected").val()
    let heat_vn = $('#heat_v').find(":selected").text();
    return {'x': heat_x,
            'xn': heat_xn,
            'y': heat_y,
            'yn': heat_yn,
            'v': heat_v,
            'vn': heat_vn}
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

    $('select#heat_x').change(function() {
      let sel_a = $('#heat_x').find(':selected').val()
      let sel_b = $('#heat_y').find(':selected').val()
      let sel_c = $('#heat_v').find(':selected').val()

      $('#heat_y').find(':disabled').prop('disabled', false);
      $('#heat_v').find(':disabled').prop('disabled', false);

      $('#heat_y [value="' + sel_a + '"]').prop('disabled', true);
      $('#heat_y [value="' + sel_c + '"]').prop('disabled', true);

      $('#heat_v [value="' + sel_a + '"]').prop('disabled', true);
      $('#heat_v [value="' + sel_b + '"]').prop('disabled', true);
    })

    $('select#heat_y').change(function() {
      let sel_a = $('#heat_x').find(':selected').val()
      let sel_b = $('#heat_y').find(':selected').val()
      let sel_c = $('#heat_v').find(':selected').val()

      $('#heat_x').find(':disabled').prop('disabled', false);
      $('#heat_v').find(':disabled').prop('disabled', false);

      $('#heat_x [value="' + sel_b + '"]').prop('disabled', true);
      $('#heat_x [value="' + sel_c + '"]').prop('disabled', true);

      $('#heat_v [value="' + sel_a + '"]').prop('disabled', true);
      $('#heat_v [value="' + sel_b + '"]').prop('disabled', true);
    })

    $('select#heat_v').change(function() {
      let sel_a = $('#heat_x').find(':selected').val()
      let sel_b = $('#heat_y').find(':selected').val()
      let sel_c = $('#heat_v').find(':selected').val()

      $('#heat_x').find(':disabled').prop('disabled', false);
      $('#heat_y').find(':disabled').prop('disabled', false);

      $('#heat_x [value="' + sel_b + '"]').prop('disabled', true);
      $('#heat_x [value="' + sel_c + '"]').prop('disabled', true);

      $('#heat_y [value="' + sel_a + '"]').prop('disabled', true);
      $('#heat_y [value="' + sel_c + '"]').prop('disabled', true);
    })

})
