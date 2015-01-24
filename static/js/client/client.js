var userNick  = "";
var gameID    = "";
var userClass = "";
var uid       = 0;
var userState = 0;
var counter   = 15;
var roomState = 0;
var selClass  = 0;



$(document).ready(function() {
    $('.countdown').toggle();
    $('#role_dps').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("DPS<span class=\"caret\"></span>");
        selClass = 1;
    });
    $('#role_tank').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Tank<span class=\"caret\"></span>");
        selClass = 2;
    });
    $('#role_support').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Healer<span class=\"caret\"></span>");
        selClass = 3;
    });
    $('#joinGame').click(function() {
        if ($('#chooseClass').hasClass("classSet")) {
            userNick  = $('.userNick').val();
            gameID    = $('.userID').val();
            $.ajax({
                url: '/game/join',
                data: { room: gameID, nick: userNick, role: selClass},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    if (response.result == true) {
                        $('.countdown').toggle();
                        $('.joinPage').toggle();
                        uid = response.uid;
                        console.log(uid);
                        
                    } else {
                        alert("Error on join, same nick different class?");
                        console.log(response.uid);
                    } 
                },
                error: function(error) {
                    console.log(error);
                }
            });
        } else {
            $('#chooseClass').html("Select a class!<span class=\"caret\"></span>");
        }
    });
    $('.readyButton').click(function() {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
           $.ajax({
                url: '/game/start',
                data: {uid: uid},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    console.log(response);
                    // State is 2
                    countdownPoll();
                },
                error: function(response) {
                    alert("Couldn't set player as ready");
                    console.log(response);
                }
            });
            // TODO: Make backend check how many players are ready before this
            // Run this until state is 3
            
        } else {
            // Make toggleable?
        }
    });
}); 


function countdownPoll() {
        setTimeout (function() {
            if (userState < 3) {
                $.ajax({
                    url: '/game/player_status',
                    data: {uid: uid},
                    dataType: 'json',
                    cache: false,
                    success: function(response) {
                        $('#theCountdown').text("Game starts in: " + counter);
                        counter--;
                        userState = response;
                        console.log("State: " + response);
                    },
                    error: function(response) {
                        alert("Failed to get player state!");
                        console.log("State: " + response);
                        return false;
                    },
                    complete: countdownPoll
                });
            } else {
                gameReadyPoll();
            }
            
        }, 1000);
}

function gameReadyPoll() {
    setTimeout(function() {
        if (userState < 4) {
            $.ajax({
                url: '/game/player_status',
                data: {uid: uid},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    userState = response;
                    console.log("state: " + response);
                },
                error: function(response) {
                    alert("Failed to get player state!");
                    console.log("State: " + response);
                    return false;
                    
                },
                complete: gameReadyPoll
            });
        } else {
            startGame();
        }
    }, 2000);
}
function startGame() {
    console.log("'Started' game");
}




