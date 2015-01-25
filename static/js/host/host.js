var gameID;
var players = [];
var countDownToGameStart = -1;

var countDownTimer = 10;
var curState = 0;
var bossImages;

$(document).ready(function () {

    //<!-- Hide all pages -->
    $("#content").children().hide();
    $('#joinUrl').text('http://' + location.hostname + '/join');

    ShowPage("PreGameScreen");

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
        }
    });

});

function GetGameState(id)
{
    updatePlayers();
    $.ajax({
        url: '/game/getHostState',
        dataType: 'json',
        data: { room_id: id },
        cache: false,
        success: function (response)
        {
            switch(response)
            {
                case 0:
                    console.log("GAME STATE 0: GROUP ASSEMBLY");
                    curState = 0;
                    // fetch players
//                    $.ajax({
//                        url: '/game/getHostStatus?room_id=' + id,
//                        dataType: 'json',
//                        cache: false,
//                        success: function (response)
//                        {
//                            // update UI
//                            // add the player in the right group onscreen
//                            var arrayLength = response.Players.length;
//                            for (var i = 0; i < arrayLength; i++)
//                            {
//                                var player = response.Players[i];
//
//                                if ($.inArray(player.Nick, players) == -1)
//                                {
//                                    console.log("Player " + player.Nick + " (role "+ player.Role +") joined the game.")
//
//                                    switch (player.Role)
//                                    {
//                                        case "1":       // DPS list
//                                            $("#dpslist").append("<div>" + player.Nick + "</div>");
//                                            break;
//                                        case "2":       // Tank list
//                                            $("#tanklist").append("<div>" + player.Nick + "</div>");
//                                            break;
//                                        case "3":       // Healer list
//                                            $("#healerlist").append("<div>" + player.Nick + "</div>");
//                                            break;
//                                    }
//
//                                    players.push(player.Nick);
//                                }
//                            }
//
//                            // fetch new status
//                            GetNewGameState();
//                        }
//                    });
                    GetNewGameState();

                    break;

                case 1:
                    if (curState != 1) {
                        console.log("GAME STATE 1: COUNT DOWN");
                        countDownToGameStart = 10;
                        CountDownToGameStart();
                        curState = 1;
                    }
                    // fetch new status
                    GetNewGameState();

                    break;
                case 2:

                    console.log("GAME STATE 2: QUEST STORY");
                    
                    $.ajax(
                    {
                        url: '/game/getHostQuestStory',
                        data: { room_id: gameID },
                        dataType: 'json',
                        cache: false,
                        success: function (response)
                        {
                            // update UI
                            $("#questTitle").html(response.Title);
                            $("#questText").html(response.Text);
                            //$("body").css('background-image', 'url(/static/images/' + response.Imageurl + ')');
                            //$("body").css('-webkit-background-size', 'cover');

                            // navigate to new screen
                            ShowPage("QuestBackgroundScreen");

                            // tell the server we are done (10 sec)
                            countDownToGameStart = 10;
                            CountDownToGameStart();

                            setTimeout(function ()
                            {
                                $.ajax(
                                {
                                    url: '/game/preGameDone',
                                    data: { room_id: gameID },
                                    dataType: 'json',
                                    cache: false
                                });

                                GetNewGameState();
                                
                            }, 10000);
                        }
                    });
                    break;
                case 3:

                    console.log("GAME STATE 3: RAND EVENT");

                    $.ajax(
                    {
                        url: '/game/getHostRandomEvent',
                        data: { room_id: gameID },
                        dataType: 'json',
                        cache: false,
                        success: function (response)
                        {
                            // update UI
                            $("#randTitle").html(response.Title);
                            $("#randText").html(response.Text);
                            //$("body").css('background-image', 'url(/static/images/' + response.Imageurl + ')');
                            //$("body").css('-webkit-background-size', 'cover');
							

                            // navigate to new screen
                            ShowPage("RandEventScreen");

                            // tell the server we are done (10 sec)
                            countDownToGameStart = 10;
                            CountDownToGameStart();

                            setTimeout(function () {
                                $.ajax(
                                {
                                    url: 'game/randomEventDone',
                                    data: { room_id: gameID },
                                    dataType: 'json',
                                    cache: false,
                                    success: function (response) {
                                        GetNewGameState();
                                    }
                                });
                            }, 10000);
                        }
                    });

                    break;
                case 4:

                    console.log("GAME STATE 4: BOSS STORY");

                    $.ajax(
                    {
                        url: 'game/getHostBossStory',
                        data: { room_id: gameID },
                        dataType: 'json',
                        cache: false,
                        success: function (response)
                        {
                            // update UI
                            $("#bossTitle").html(response.Title);
                            $("#bossText").html(response.Text);

                            $.ajax({
                                url: 'game/generateBoss',
                                cache: false,
                                dataType: "json",
                                success: function (bossResponse) {
                                    bossImages = bossResponse;
                                    $('.leftarm').attr("src", bossImages['leftarm'])
                                    $('.legs').attr("src", bossImages['legs'])
                                    $('.rightarm').attr("src", bossImages['rightarm'])
                                    $('.weapon').attr("src", bossImages['weapon'])
                                    $('.head').attr("src", bossImages['head'])
                                    $('.torso').attr("src", bossImages['torso'])
                                }
                            });

                            // navigate to new screen
                            ShowPage("BossStoryScreen");

                            // tell the server we are done (10 sec)
                            countDownToGameStart = 10;
                            CountDownToGameStart();

                            setTimeout(function () {
                                $.ajax(
                                {
                                    url: 'game/bossStoryDone',
                                    data: { room_id: id },
                                    cache: false,
                                    success: function (response) {
                                        GetNewGameState();
                                    }
                                });
                            }, 10000);
                        }
                    });

                    break;
                case 5:

                    console.log("GAME STATE 5: ROUND");

                    $.ajax(
                    {
                        url: '/game/getHostRound',
                        data: { room_id: gameID },
                        dataType: 'json',
                        cache: false,
                        success: function(response) 
                        {
                            // update UI

                            // navigate to new screen
                            ShowPage("RoundScreen");

                            // fetch new status
                            GetNewGameState();
                        }
                    });                    

                    break;

                case 6:

                    console.log("GAME STATE 6: ROUND RESULT");

                    $.ajax(
                    {
                        url: '/game/getHostRoundResult',
                        data: { room_id: gameID },
                        dataType: 'json',
                        cache: false,
                        success: function (response)
                        {
                            
                            // tell the server we are done (10 sec)
                            countDownToGameStart = 10;
                            CountDownToGameStart();

                            // navigate to new screen
                            ShowPage("RoundResultScreen");

                            setTimeout(function () {
                                $.ajax(
                                {
                                    url: 'game/roundResultDone',
                                    data: { room_id: id },
                                    dataType: 'json'
                                });

                                // fetch new status
                                GetNewGameState();

                            }, 10000);
                        }
                    });                    

                    break;

                case 7:

                    console.log("GAME STATE 7: ROUND");

                    // navigate to new screen
                    ShowPage("VictoryScreen");

                    break;

                case 99:

                    console.log("GAME STATE 99: ROUND");

                    // navigate to new screen
                    ShowPage("DeathScreen");

                    break;
            }
        }
    });
}

function GetNewGameState()
{
    setTimeout(function () { GetGameState(gameID); }, 2000);
}

function CountDownToGameStart()
{
    if (countDownToGameStart > 0) {
        $("#countdownTimer").show();
        $("#countdownTimer span").fadeOut(function() {
            $(this).text(countDownToGameStart);
        }).fadeIn();
    }

    countDownToGameStart -= 1;
    if (countDownToGameStart == 3) {
        $('#countdownTimer span').css('position','fixed');
        $('#countdownTimer span').css('font-size','3500%');
        $('#countdownTimer span').css("left", ($(window).width()/2-$('#countdownTimer span').width()/2) + "px");
        $('#countdownTimer span').css("top", ($(window).height()/2-$('#countdownTimer span').height()/2) + "px");
        $('#countdownTimer span').css('color','red');

    }
    if (countDownToGameStart == 0) {
        countDownToGameStart = -1;
        $('#countdownTimer span').text("")
        $('#countdownTimer span').css('position','absolute');
        $('#countdownTimer span').css('left','');
        $('#countdownTimer span').css('top','');
        $('#countdownTimer span').css('right','0');
        $('#countdownTimer span').css('bottom','0');
        $('#countdownTimer span').css('font-size','1200%');
        $('#countdownTimer span').css('color','');
        $("#countdownTimer").hide();
        return;
    } else {
        setTimeout(CountDownToGameStart, 1000);
    }
}
function ShowPage(id)
{
    $("#content").children().hide();

    $("#" + id).show();
}

function CharacterAnim(elem, dist, speed) {
    $("."+elem).animate({ top: "+="+dist+"px" }, speed, 'linear', function () {
        $("."+elem).animate({ top: "-="+dist+"px" }, speed, 'linear', function() { CharacterAnim(elem, dist, speed); });
    });
}

function updatePlayers() {
    $.ajax({
        url: '/game/getHostStatus?room_id=' + gameID,
        dataType: 'json',
        cache: false,
        success: function (response)
        {
            // update UI
            // add the player in the right group onscreen
            $.each(response.Players, function (key, value) {
                if ($.inArray(value.Nick, players) == -1)
                {
                    console.log("Player " + value.Nick + " (role "+ value.Role +") joined the game.")

                    playerIndicator = '<div class="col-md-2">'
                    playerIndicator += '<img class="statusRoleImg" src="/static/images/icons/';

                    switch (value.Role)
                    {
                        case "1":       // DPS list
                            playerIndicator += 'ic_dps_clear.png" id="pImg' + value.Uid + '"';
//                            $("#dpslist").append("<div>" + player.Nick + "</div>");
                            break;
                        case "2":       // Tank list
                            playerIndicator += 'ic_tank_clear.png" id="pImg' + value.Uid + '"';
//                            $("#tanklist").append("<div>" + player.Nick + "</div>");
                            break;
                        case "3":       // Healer list
                            playerIndicator += 'ic_heal_clear.png" id="pImg' + value.Uid + '"';
//                            $("#healerlist").append("<div>" + player.Nick + "</div>");
                            break;
                    }

                    playerIndicator += ' />'
                    playerIndicator += ' <span class="playerName">' + value.Nick + '</span>';

                    $('#playerList').append(playerIndicator);
                    players.push(value.Nick);

                } else {
                    if (value.Ready === 1  && curState === 0) {
                        switch (value.Role)
                        {
                            case "1":       // DPS list
                                  $('#pImg' + value.Uid).attr('src', '/static/images/icons/ic_dps.png');
    //                            $("#dpslist").append("<div>" + player.Nick + "</div>");
                                break;
                            case "2":       // Tank list
                                $('#pImg' + value.Uid).attr('src', '/static/images/icons/ic_tank.png');
    //                            $("#tanklist").append("<div>" + player.Nick + "</div>");
                                break;
                            case "3":       // Healer list
                               $('#pImg' + value.Uid).attr('src', '/static/images/icons/ic_heal.png');
    //                            $("#healerlist").append("<div>" + player.Nick + "</div>");
                                break;
                        }
                    }
                }
            });
        }
    });
}
