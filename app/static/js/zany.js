document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
    document.getElementById("zany").addEventListener("click", function a() {
    document.getElementById("zany").removeEventListener('click', a);
    console.log("Connecting to Queue");
    document.getElementById("zany").innerHTML = "Connecting...";
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      console.log("Connected to socket");
      socket.emit('mode', "zany");
      console.log("Sent mode")
      socket.on('okay', (data)=>{
        var options = {'dismissable': true}
        var elem = document.querySelector('.modal');
        var instance = M.Modal.init(elem, options);

        instance.open();
        console.log(data);
        opinion = (data.opinion == 'yes' ? "👍" : "👎");

        document.getElementsByClassName("username")[0].textContent = data.name;
        document.querySelector('.modal-topic').textContent = data.topic;
        document.querySelector('.modal-emoji').textContent = opinion;
        document.querySelector('.header-topic').textContent = data.topic;
        document.querySelector('.header-emoji').textContent = opinion;

        instance.open()
        chatBegin();
        socket.on('msg', (datum)=>{
          console.log(datum);
          addMessage(datum, 1)
          var objDiv = document.querySelector(".chat__window");
          objDiv.scrollTop = objDiv.scrollHeight;
        });

        document.getElementById("submitbtn")
          .addEventListener("click", function(event) {
          event.preventDefault();
          var message = document.getElementById("chat__field").value;
          console.log(message);
          socket.emit('msg', message);
          document.getElementById("chat__field").value = "";
          addMessage(message);
          var objDiv = document.querySelector(".chat__window");
          objDiv.scrollTop = objDiv.scrollHeight;
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
