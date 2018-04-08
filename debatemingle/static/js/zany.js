console.log("hello");
document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
  document.getElementById("zany").addEventListener("click", ()=>{
    console.log("hello");
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      socket.emit('okay', "griffin");
      socket.on('okay', (data)=>{
        console.log(data);
      });
    });
    chatBegin();
  });
});

function chatBegin() {
  var waiting = document.getElementById("waiting");
  var chat = document.getElementById("chat");
  waiting.remove();
  chat.classList.remove("hidden");
}
