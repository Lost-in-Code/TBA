$(document).ready(function() {
    $.ajax( {
        url: '/game/create',
        dataType: 'json',
        cache: false,
        success: function(response){
            var gameID = response.room_id;
            $('#gameID').text(gameID);
        },
        failure: function(response){
            alert("Error hosting game, could not retrieve game ID");
            console.log(response);
        }
    });
});