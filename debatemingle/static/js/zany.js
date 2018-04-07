console.log("hello");
document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
  document.getElementById("zany").addEventListener("click", ()=>{
    console.log("hello");
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      socket.emit('okay', "griffin");
    });
  });
});

