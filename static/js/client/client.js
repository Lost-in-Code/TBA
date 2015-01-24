var userNick  = "";
var gameID    = "";
var userClass = "";
var uid       = 0;
var userState = 0;
var oldState  = 0;
var selClass  = 0;
var hp        = 100;
var mana      = 100;


$(document).ready(function() {
    $('.readyPage').hide();
    $('.game').hide();
    $('.waiting').hide();
    $('.joinPage').show();
    
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
                        readyPage();
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
        $('.readyPage').find('button').attr('disabled', true);
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
    });
}); 

setInterval(function() {
   if (userState != oldState) {
        if (userState === 1) {
            oldState = userState;
            readyPage();
        } else if (userState === 2){
            oldState = userState;
            goWaiting();
        } else if (userState === 3) {
            oldState = userState;
            goWaiting();
        } else if (userState === 4) {
            oldState = userState;
            startRound();
        } else if (userState === 5) {
            oldState = userState;
            goWaiting();
        } else if(!userState) {
            joinPage();
        }
    }
    $.ajax({
        url: '/game/getPlayerState',
        data: {uid: uid},
        dataType: 'json',
        cache: false,
        success: function(response) {
            oldState = userState;
            userState = response;
            console.log("State: " + response);
        },
    });
    $.ajax({
        url: '/game/getPlayerStatus',
        data: {uid: uid},
        dataType: 'json',
        cache: false,
        success: function(response) {
            if (response.hp < 0) { hp = 0;} else {hp = response.HP;}
            $('.hp_bar').text(hp + "%");
            $('.hp_bar').css("width", hp+"%");
            mana = response.Mana;
            $('.mana_bar').text(mana + "%");
            $('.mana_bar').css("width", mana+"%");
        }
    });
}, 2000);



function joinPage() {
    $('.readyPage').hide();
    $('.joinPage').show();
    $('.game').hide();
    $('.waiting').hide();
}
function readyPage() {
    document.title = "Are you ready?";
    $('.readyPage').find('button').attr('disabled', false);
    $('.readyPage').show();
    $('.joinPage').hide();
    $('.waiting').hide();
    $('.game').hide();
}


function startRound() {
    $('.readyPage').hide();
    $('.joinPage').hide();
    $('.game').show();
    $('.waiting').hide();
    $('.mana').hide();
    $('.attack_buttons').find('button').attr('disabled', false);
    document.title = 'Battle!';
    
    if (selClass === 1) {
        $('.action1').text("Melee Attack");
        $('.action2').text("Ranged Attack");
        $('.action3').text("Boost Attack");
    } else if (selClass === 2) {
        $('.action1').text("Taunt");
        $('.action2').text("Guard");
        $('.action3').text("Boost Defense");
    } else if (selClass === 3) {
        $('.action1').text("Tank Heal");
        $('.action2').text("Group Heal");
        $('.action3').text("Recover Mana");
        $('.mana').show();
    }  
    $('.action1').unbind().bind('click', function() {
        $.ajax({
            url: '/game/doClientAction',
            data: {uid:uid, action: 1},
            dataType: 'json',
            cache: false,
            success: function() {
                console.log("sent attack");
                $('.attack_buttons').find('button').attr('disabled', true);
            },
            error: function(response) {
                alert("Could not send your action!");
                console.log(response);
            }
        });
    });
    $('.action2').unbind().bind('click', function() {
        $.ajax({
            url: '/game/doClientAction',
            data: {uid:uid, action: 2},
            dataType: 'json',
            cache: false,
            success: function() {
                console.log("sent attack");
                $('.attack_buttons').find('button').attr('disabled', true);
            },
            error: function(response) {
                alert("Could not send your action!");
                console.log(response);
            }
        });
    });
    $('.action3').unbind().bind('click', function() {

        $.ajax({
            url: '/game/doClientAction',
            data: {uid:uid, action: 3},
            dataType: 'json',
            cache: false,
            success: function() {
                console.log("sent attack");
                $('.attack_buttons').find('button').attr('disabled', true);
            },
            error: function(response) {
                alert("Could not send your action!");
                console.log(response);
            }
        });
    });
}

function goWaiting() {
    document.title = 'Waiting...';
    $('.readyPage').hide();
    $('.joinPage').hide();
    $('.game').hide();
    $('.waiting').show();
}


