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
		mymsg = msg
		$('#player-hand').text(msg.data);
	});
    socket.on('status', function(msg){
		mymsg = msg
		$('#prompt').text(msg.msg);
	});
    socket.on('prompt', function(msg){
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
