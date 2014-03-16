var mymsg = '';
var my_id = '';

$(document).ready(function() {
	var socket = io.connect('http://192.168.1.20:5000/play');

	socket.on('connected', function(msg) {
        my_id = msg.id;
		$('#opponent-hand').text("Socket: " + my_id);
        socket.emit('connect_ack', {data: 'ACK'});
	});
	socket.on('closed', function(){
		$('#opponent-hand').text("Socket has closed!");
	});
	socket.on('throw_ack', function(msg){
		mymsg = msg;
        resetButtons();
        $('#'+msg.toLowerCase()).css({'border-width': '5px',
                                      'border-color': '#EEE'});
	});
    socket.on('prompt', function(msg){
		mymsg = msg;
		$('#prompt').text(msg);
	});
    socket.on('bout', function(){
        resetButtons();
	});
    socket.on('scores', function(msg){
        console.log('On scores');
        $('#prompt').text(msg['prompt']);
        delete msg['prompt'];
        Object.keys(msg).forEach(function (key) {
            var score = msg[key];
            var element = '';
            if(key === my_id) { var player = 'player'; } 
            else { var player = 'opponent'; }
            $('#'+player+'-hand').text(score['hand']);
            for(var i = 1; i <= 3; i++) {
                element = '#'+player+'-m'+i;
                if(score['match'] >= i ) {
                    $(element).text(2);
                }
                else if (score['match'] === i-1) {
                    $(element).text(score['bout']);
                }
                else {
                    $(element).text(0);
                }
            }
        });
    });
    socket.on('end_game', function(msg){
        if(msg['winner'] === my_id) {
            $('#prompt').text('You Win!');
        }
        else {
            $('#prompt').text('You Lose.');
        }
    });
    $('#rock').click(function() {
        socket.emit('throw', 'Rock');
    });
    $('#paper').click(function() {
        socket.emit('throw', 'Paper');
    });
    $('#scissors').click(function() {
        socket.emit('throw', 'Scissors');
    });
});

function resetButtons() {
    $('.throw-button').css({'border': 'solid 1px black'}); 
}
function resetDisplay() {
    for(var i = 1; i <= 3; i++) {
        for(player in ['player', 'opponent']) {
            element = '#'+player+'-m'+i;
            $(element).text(0);
        }
    }
}
