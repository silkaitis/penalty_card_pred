let get_teams = function() {
    let home = $('#home_teams').find(":selected").val()
    let away = $('#away_teams').find(":selected").val()
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
            display_teams(data)
            display_yellows(data)
            display_reds(data);
        },
        data: JSON.stringify(coefficients)
    });
};

let display_teams = function(soln) {
  let home = $('#home_teams').find(":selected").text()
  let away = $('#away_teams').find(":selected").text()
  let ref = $('#referee').find(":selected").text();
  $("span#hometeam").html(home)
  $("span#awayteam").html(away)
  $("span#referee").html(ref)
}
let display_yellows = function(soln) {
    $("span#home_yellow").html(soln.home_yellow)
    $("span#away_yellow").html(soln.away_yellow)
};

let display_reds = function(soln) {
    $("span#home_red").html(soln.home_red)
    $("span#away_red").html(soln.away_red)
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
