$(document).ready(function () {

    var gameID;

    $.ajax({
        url: '/game/create',
        dataType: 'json',
        cache: false,
        success: function (response)
        {
            gameID = response.room_id;
            $('#gameID').text(gameID);

            addPlayersToLists(gameID);

            console.log(gameID);
        },
        failure: function (response)
        {
            alert("Error hosting game, could not retrieve game ID");

            console.log(response);
        }
    });

});

function addPlayersToLists(gameID) {
   /* $.ajax( {
            // Get list of players from server in a loop, pseudocode:
            for player in players:
                if player.room_id == gameID:
                    if player.role == "DPS":
                        $('.dps').append("<p>" + player.nick   + "</p>")
                    if player.role == "Tank":
                        $('.tanks').append("<p>" + player.nick   + "</p>")
                    if player.role == "Support":
                        $('.healers').append("<p>" + player.nick   + "</p>")
        }); */
}