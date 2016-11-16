let get_teams = function() {
    let home = $('#home_teams').find(":selected").text()
    let away = $('#away_teams').find(":selected").text()
    let ref = $('#referee').find(":selected").val();
    return {'home': home,
            'away': away,
            'ref': ref}
};

let send_teams = function(coefficients) {
    $.ajax({
        url: '/pred',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            match_up(data)
            display_yellows(data)
            display_reds(data);
        },
        data: JSON.stringify(coefficients)
    });
};
let match_up = function(soln) {
  $("span#match_up").html(soln.home + ' versus ' + soln.away)
};

let display_yellows = function(soln) {
    $("span#yellows").html('Yellows: ' + soln.home_yellow + ' - ' + soln.away_yellow)
};

let display_reds = function(soln) {
    $("span#reds").html('Reds: ' + soln.home_red + ' - ' + soln.away_red)
};


$(document).ready(function() {

    $("button#predict").click(function() {
        let teams = get_teams();
        send_teams(teams);
    })

    $("select#home_teams").change(function() {
      $('#away_teams').find(':disabled').prop('disabled', false);

      let h_team = $('#home_teams').find(":selected").val()
      $('#away_teams [value="' + h_team + '"]').prop('disabled', true);
    })

    $('select#away_teams').change(function() {
      $('#home_teams').find(':disabled').prop('disabled', false);

      let a_team = $('#away_teams').find(':selected').val()
      $('#home_teams [value="' + a_team + '"]').prop('disabled', true);
    })

})
