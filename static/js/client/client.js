$(document).ready(function() {
    $('#role_dps').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("DPS <span class=\"caret\"></span>");
    });
    $('#role_tank').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Tank <span class=\"caret\"></span>");
    });
    $('#role_support').click(function() {
        $('#chooseClass').addClass("classSet");
        $('#chooseClass').html("Support <span class=\"caret\"></span>");
    });
    $('#joinGame').click(function() {
        if ($('#chooseClass').hasClass("classSet")) {
            var userNick = $('.userNick').val();
            var gameID   = $('.userID').val();
            var userClass= $('#chooseClass').text();
            $.ajax({
                url: '/game/join',
                data: { room: gameID, nick: userNick, role: userClass},
                dataType: 'json',
                cache: false,
                success: function(response) {
                    if (response.result == true) {
                        $('body').load($('#urlForCountdownHTML').text());
                    } else {
                        alert("error! same nick different class?");
                        console.log(response.uid);
                    }
                    // Set HTML to logged in user
                    
                },
                error: function(error) {
                    console.log(error);
                }
            });
                
            // Send info to server, check game ID
            // Set HTML code to user logged in: Ready button/countdown
        } else {
            $('#chooseClass').html("Select a class! <span class=\"caret\"></span>");
        }
    });
});