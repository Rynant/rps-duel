var mymsg = '';
$(document).ready(function() {
	var socket = io.connect('http://localhost:5000/echo');

	socket.on('connected', function(msg) {
		$('#opponent-hand').text("Socket has been opened!");
	});
	socket.on('closed', function(){
		$('#opponent-hand').text("Socket has closed!");
	});
	socket.on('throw ack', function(msg){
		mymsg = msg
		$('#player-hand').text(msg.data);
	});
    $('#rock').click(function() {
        socket.emit('throw', {data: 'Rock'});
    });
    $('#paper').click(function() {
        socket.emit('throw', {data: 'Paper'});
    });
    $('#scissors').click(function() {
        socket.emit('throw', {data: 'Scissors'});
    });
});
