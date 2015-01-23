$(document).ready(function() {
    $('.countdown').toggle();
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
                        $('.countdown').toggle();
                        $('.joinPage').toggle();
                        
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
                
            // Send info to server, check game ID
            // Set HTML code to user logged in: Ready button/countdown
        } else {
            $('#chooseClass').html("Select a class! <span class=\"caret\"></span>");
        }
    });
    $('.readyButton').click(function() {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
        } else {
        }
    });
});