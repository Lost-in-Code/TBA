var gameID;
var players = [];

$(document).ready(function () {

    $.ajax({
        url: '/game/create',
        dataType: 'json',
        cache: false,
        success: function (response)
        {
            gameID = response.room_id;
            $('#gameID').text(gameID);

            console.log(gameID);

            // start game loop
            GetGameState(gameID);            
        },
        failure: function (response)
        {
            alert("Error hosting game, could not retrieve game ID");

            console.log(response);
        }
    });

});

function GetGameState(id)
{
    //console.log("Getting game state");

    $.ajax({
        url: '/game/getHostState',
        dataType: 'json',
        data: { room_id: id },
        cache: false,
        success: function (response)
        {
            //console.log("State: " + response);

            switch(response)
            {
                case 0:       // INIT FASE
                    //console.log("Fetching status for state 0");

                    // fetch players
                    $.ajax({
                        url: '/game/getHostStatus?room_id=' + id,
                        dataType: 'json',
                        cache: false,
                        success: function (response)
                        {
                            // add the player in the right group onscreen
                            var arrayLength = response.Players.length;
                            for (var i = 0; i < arrayLength; i++) {
                                
                                var player = response.Players[i];                              
                                //console.log(player);
                                if ($.inArray(player.Nick, players) == -1)
                                {
                                    console.log("Player " + player.Nick + " (role "+ player.Role +") joined the game.")

                                    switch (player.Role) 
                                    {
                                        case "1":       // DPS list
                                            $("#dpslist").append("<div>" + player.Nick + "</div>");
                                            break;
                                        case "2":       // Tank list
                                            $("#tanklist").append("<div>" + player.Nick + "</div>");
                                            break;
                                        case "3":       // Healer list
                                            $("#healerlist").append("<div>" + player.Nick + "</div>");
                                            break;
                                    }

                                    players.push(player.Nick);
                                }                                
                            }

                            // fetch new status
                            setTimeout(GetGameState(id), 5000);
                        },
                        failure: function (response) {
                            alert("Could not fetch players for game " + id);

                            console.log(response);
                        }
                    });

                    break;
            }
        },
        failure: function (response)
        {
            Alert("Could not get game status");
        }
    });
}