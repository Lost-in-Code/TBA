var userNick  = "";
var gameID    = "";
var userClass = "";
var uid       = 0;
var userState = 0;
var counter   = 15;

$(document).ready(function() {
    $('.countdown').toggle();
    $('#role_dps').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("DPS<span class=\"caret\"></span>");
    });
    $('#role_tank').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Tank<span class=\"caret\"></span>");
    });
    $('#role_support').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Support<span class=\"caret\"></span>");
    });
    $('#joinGame').click(function() {
        if ($('#chooseClass').hasClass("classSet")) {
            userNick  = $('.userNick').val();
            gameID    = $('.userID').val();
            userClass = $('#chooseClass').text();
            $.ajax({
                url: '/game/join',
                data: { room: gameID, nick: userNick, role: userClass},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    if (response.result == true) {
                        $('.countdown').toggle();
                        $('.joinPage').toggle();
                        uid = response.uid;
                        console.log(response.uid)
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
                },
                error: function(response) {
                    alert("Couldn't set player as ready");
                    console.log(response);
                }
            });
            // TODO: Make backend check how many players are ready before this
            countdownPoll();
        } else {
            // Make toggleable?
        }
    });
});

function countdownPoll() {
    setTimeout(function() {
        if (userState != 3) {
            $.ajax({
                url: '/game/player_status',
                data: {uid: uid},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    userState = response;  
                    console.log(response);
                    $('#theCountdown').text("Game starts in: " + counter);
                    counter--;
                },
                complete: countdownPoll
                
            });
        }
    }, 1000);

}

function startGame() {
    
}