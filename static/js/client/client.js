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
            uid       = 0;
            $.ajax({
                url: '/game/join',
                data: { room: gameID, nick: userNick, role: userClass},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    if (response.result == true) {
                        $('.countdown').toggle();
                        $('.joinPage').toggle();
                        // Tell the server our uid and that we are ready to join
                        countdownCheck();
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
            // Somehow check with the server when to start the countdown, when countdown ends:
            // Hide .countdown, toggle .game
            // 
        } else {
            $('#chooseClass').html("Select a class!<span class=\"caret\"></span>");
        }
    });
    $('.readyButton').click(function() {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
           /* .ajax({
                url: 'game/playerIsReady', // Not a real URL, expect how many are ready?
                data: {room: gameID, uid: uid, player_ready: true},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    startCountdown();   */
        } else {
            // Make toggleable?
        }
    });
});


// Check the number of ready players and start countdown if more than half

function countdownCheck() {
    
}

function startCountdown() {
    
}