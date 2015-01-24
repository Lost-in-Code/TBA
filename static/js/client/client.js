var userNick  = "";
var gameID    = "";
var userClass = "";
var uid       = 0;
var userState = 0;
var oldState  = 0;
var counter   = 7;
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
                        questCountdown();
                        uid = response.uid;
                        console.log(uid);
                        userState = 1;
                        
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
                },
                error: function(response) {
                    alert("Couldn't set player as ready");
                    console.log(response);
                }
            });
            
        } else {
            // Make toggleable?
        }
    });
}); 

setInterval(function() {
    if (userState != oldState) {
        if (userState === 2) {
            questCountdown();
        } else if (userState === 4) {
            startRound();
        } else if (userState === 5) {
            roundResultPoll();
        }
    }
    $.ajax({
        url: '/game/getPlayerState',
        data: {uid: uid},
        dataType: 'json',
        cache: false,
        success: function(response) {
            if (userState == 2) {
                $('#theCountdown').text("Game starts in: " + counter);
                counter--;
                if (counter < 0) { counter = 0; }
            }
            oldState = userState;
            userState = response;
            console.log("State: " + response);
        }
        });
}, 2000);

function questCountdown() {
    $('.countdown').show();
    $('.joinPage').hide();
    $('.game').hide();
}


function startRound() {
    console.log("'Started' game");
}




