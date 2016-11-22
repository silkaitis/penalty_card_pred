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

let get_vars_tc = function() {
    let tc_sort = $('#tc_sort').find(":selected").val()
    let tc_sortn = $('#tc_sort').find(":selected").text()
    let tc_f = $('#tc_f').find(":selected").val()
    let tc_fn = $('#tc_f').find(":selected").text()
    let tc_s = $('#tc_s').find(":selected").val()
    let tc_sn = $('#tc_s').find(":selected").text();
    return {'x': tc_sort,
            'xn': tc_sortn,
            'y': tc_f,
            'yn': tc_fn,
            'v': tc_s,
            'vn': tc_sn}
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

let send_graph_tc = function(coefficients) {
    $.ajax({
        url: '/graph_binary_tc',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            document.getElementById("tc_graph").src=data;
        },
        data: JSON.stringify(coefficients)
    });
};

$(document).ready(function() {

    $("button#generate").click(function() {
        let vars = get_vars();
        send_graph(vars);
    })

    $("button#tc_generate").click(function() {
        let vars = get_vars_tc();
        send_graph_tc(vars);
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

    $('select#tc_sort').change(function() {
      let sel_a = $('#tc_sort').find(':selected').val()
      let sel_b = $('#tc_f').find(':selected').val()
      let sel_c = $('#tc_s').find(':selected').val()

      $('#tc_f').find(':disabled').prop('disabled', false);
      $('#tc_s').find(':disabled').prop('disabled', false);

      $('#tc_f [value="' + sel_a + '"]').prop('disabled', true);
      $('#tc_f [value="' + sel_c + '"]').prop('disabled', true);

      $('#tc_s [value="' + sel_a + '"]').prop('disabled', true);
      $('#tc_s [value="' + sel_b + '"]').prop('disabled', true);
    })

    $('select#tc_f').change(function() {
      let sel_a = $('#tc_sort').find(':selected').val()
      let sel_b = $('#tc_f').find(':selected').val()
      let sel_c = $('#tc_s').find(':selected').val()

      $('#tc_sort').find(':disabled').prop('disabled', false);
      $('#tc_s').find(':disabled').prop('disabled', false);

      $('#tc_sort [value="' + sel_b + '"]').prop('disabled', true);
      $('#tc_sort [value="' + sel_c + '"]').prop('disabled', true);

      $('#tc_s [value="' + sel_a + '"]').prop('disabled', true);
      $('#tc_s [value="' + sel_b + '"]').prop('disabled', true);
    })

    $('select#tc_s').change(function() {
      let sel_a = $('#tc_sort').find(':selected').val()
      let sel_b = $('#tc_f').find(':selected').val()
      let sel_c = $('#tc_s').find(':selected').val()

      $('#tc_sort').find(':disabled').prop('disabled', false);
      $('#tc_f').find(':disabled').prop('disabled', false);

      $('#tc_sort [value="' + sel_b + '"]').prop('disabled', true);
      $('#tc_sort [value="' + sel_c + '"]').prop('disabled', true);

      $('#tc_f [value="' + sel_a + '"]').prop('disabled', true);
      $('#tc_f [value="' + sel_c + '"]').prop('disabled', true);
    })

})
