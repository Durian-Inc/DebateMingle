document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
    document.getElementById("serious").addEventListener("click", function a() {
    document.getElementById("serious").removeEventListener('click', a);
    console.log("Connecting to Queue");
    document.getElementById("serious").innerHTML = "Connecting...";
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      socket.emit('mode', "serious");
      socket.on('okay', (data)=>{
        var options = {'dismissable': true}
        var elem = document.querySelector('.modal');
        var instance = M.Modal.init(elem, options);

        instance.open();
        console.log(data);

        document.getElementsByClassName("username")[0].textContent = data.name;
        document.querySelector('.modal-topic').textContent = data.topic;
        document.querySelector('.modal-emoji').textContent = data.opinion;

        instance.open()
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
          addMessage(message);
        });
        socket.on('disconnect', (reason)=>connectionDead(reason));
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

function connectionDead(reason) {
  var elem = document.querySelector('.modal');
  var instance = M.Modal.getInstance(elem);
  document.querySelector('.modal-header').textContent = "Your chat session has ended!";
  document.querySelector('.modal-text').textContent = "You will be sent away in 5 seconds.";
  document.querySelector('.modal-topic').textContent = reason;
  document.querySelector('.modal-emoji').textContent = "🙅";
  instance.open();
  setTimeout(()=>location.reload(), 5000);
}
