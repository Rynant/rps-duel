var mymsg = '';
$(document).ready(function() {
	var socket = io.connect('http://localhost:5000/play');

	socket.on('connected', function(msg) {
		$('#opponent-hand').text("Socket has been opened!");
        socket.emit('connect_ack', {data: 'ACK'});
	});
	socket.on('closed', function(){
		$('#opponent-hand').text("Socket has closed!");
	});
	socket.on('throw ack', function(msg){
		mymsg = msg
		$('#player-hand').text(msg.data);
	});
    socket.on('status', function(msg){
		mymsg = msg
		$('#prompt').text(msg.msg);
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
