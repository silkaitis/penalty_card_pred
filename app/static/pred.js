
// $("#home_teams").change(function() {
//   if ($(this).data('options') == undefined) {
//     /*Taking an array of all options-2 and kind of embedding it on the select1*/
//     $(this).data('options', $('#away_teams option').clone());
//   }
//   var id = $(this).val();
//   var options = $(this).data('options').filter('[value=' + id + ']');
//   $('#away_teams').html(options);
// });
//
// $(document).ready(function () {
//     $("home_teams").change(function () {
//         var val = $(this).val();
//         if (val == "manchester_united") {
//             $("away_teams option[value='manchester_united']").remove()}
//     });
// });
//
// $( "home_teams" ).change(function( event ) {
//   var target = $( event.target );
//   $("away_teams option[value='manchester_united']").remove()
//   }
// });
//
// $("#away_teams option[value='manchester_united']").remove();
let get_teams = function() {
    let home = $('#home_teams').find(":selected").text()
    let away = $('#away_teams').find(":selected").text();
    return {'home': home,
            'away': away}
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

})
