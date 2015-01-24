var gameID;
var players = [];
var countDownToGameStart = null;

$(document).ready(function () {

    $.sammy('#main', function () {

        this.get('#/', function (context) {
            ShowPage("PreGameScreen");
        });

    }).run("#/");

    // ko.applyBindings(new InitGamePage());

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
    console.log("Getting game state");

    $.ajax({
        url: '/game/getHostState',
        dataType: 'json',
        data: { room_id: id },
        cache: false,
        success: function (response)
        {
            console.log("State: " + response);

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
                            for (var i = 0; i < arrayLength; i++)
                            {                                
                                var player = response.Players[i];                              

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
                            GetNewGameState();
                        },
                        failure: function (response) {
                            alert("Could not fetch players for game " + id);

                            console.log(response);
                        }
                    });

                    break;

                case 1:     // COUNT DOWN TO GAME START STATE
                    console.log("got count down");
                    if (countDownToGameStart == null)
                    {
                        countDownToGameStart = 10;

                        CountDownToGameStart();
                    }

                    // fetch new status
                    GetNewGameState();
                    break;
                case 2:
                    $.ajax(
                    {
                        url: '/game/getHostQuestStory',
                        data: { room_id: id },
                        dataType: 'json',
                        cache: false,
                        success: function (response) {

                            console.log(response);

                            // load viewmodel 
                            var vm = {
                                Title: ko.observable(response.Title),
                                Text: ko.observable(response.Text)
                            };
                            ko.applyBindings(vm);

                            // navigate to new screen
                            ShowPage("QuestBackgroundScreen");

                            // start timer to move to next state
                            setTimer(function ()
                            {
                                // timeout finished, move to state 3
                                $.ajax(
                                {

                                });


                            }, 10000);
                        },
                        failure: function (response) {
                            alert("State 2 fail");

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

function GetNewGameState()
{
    setTimeout(function () { GetGameState(gameID); }, 2000);
}

function CountDownToGameStart()
{
    $("#countDown").text(countDownToGameStart);

    countDownToGameStart -= 1;

    if (countDownToGameStart < 0) countDownToGameStart = 0;

    setTimeout(CountDownToGameStart, 1000);
}