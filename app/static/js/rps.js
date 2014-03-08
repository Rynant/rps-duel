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
    // Start new bout
    socket.on('bout', function(){
        resetButtons();
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
   $('.throw-button').css({'border-width': '1px'}); 
}
