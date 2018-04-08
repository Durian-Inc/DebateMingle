document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
  document.getElementById("zany").addEventListener("click", ()=>{
    console.log("Connecting to Queue");
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      socket.emit('okay', "griffin");
      socket.on('okay', (data)=>{
        console.log(data);
        document.getElementsByClassName("username")[0].textContent = data.name;
        addMessage("You will be talking about "+data.topic+". You feel very "+data.opinion+" about this topic!");
        chatBegin();
        socket.on('msg', (datum)=>{
          console.log(datum);
          addMessage(datum, 1)
        });

        document.getElementById("submitbtn")
          .addEventListener("click", function(event) {
          event.preventDefault();
          var message = document.getElementById("chat__field").value;
          console.log(message);
          socket.emit('msg', message);
            document.getElementById("chat__field").value = "";
        });

      });
    });
  });
});

function chatBegin() {
  var waiting = document.getElementById("waiting");
  var chat = document.getElementById("chat");
  waiting.remove();
  chat.classList.remove("hidden");
}

function tag(name, attrs) {
  var el = document.createElement(name.toString());

  !!attrs && Object.keys(attrs).forEach(function(key) {
    el.setAttribute(key, attrs[key]);
  });

  return el;
}

function addMessage(message, received=0) {
  var theirs = " theirs".repeat(Boolean(received));

  var line = tag('li', {'class':'chat__line'});
  var bubble = tag('div', {'class': 'bubble'+theirs});

  bubble.textContent = message.toString();
  line.appendChild(bubble);

  document.getElementsByClassName("chat__window")[0].appendChild(line);
}
