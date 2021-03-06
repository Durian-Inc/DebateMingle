document.addEventListener("DOMContentLoaded", ()=>{
  // The page is fully loaded
  var url = 'http://'+document.domain+':'+location.port;
  var element = document.getElementById("swipy");
  var hammertime = new Hammer(element);
  
var cards;
var request = new XMLHttpRequest();
request.open('GET', url+'/topics', true);

request.onload = function() {
  if (request.status >= 200 && request.status < 400) {
    // Success!
    var topics = JSON.parse(request.responseText);
    console.log(topics)
    cards = topics.map((topic)=>{
      var output = false;
      var req = new XMLHttpRequest();
      req.open('GET', url+'/check_topic/'+topic, false);
      req.onload = function() {
        if (req.status >= 200 && req.status < 400) {
          // Success!
          if (req.responseText == "False") {
            output = topic;
          }
        } else {
          // We reached our target server, but it returned an error
          console.log("also rip");
        }
      };

      req.onerror = function() {
        // There was a connection error of some sort
      };

      req.send();
      return output;
      
  });

  } else {
    // We reached our target server, but it returned an error
    console.log('rip')
  }
  console.log(cards);



  document.querySelector(".card-title").textContent = cards.pop(0);

  hammertime.on('pan', function(ev) {
    console.log(ev);
  });
  hammertime.get('pan').set({ direction: Hammer.DIRECTION_ALL });
  // listen to events...
  hammertime.on("panleft panright pandown", function(ev) {
    if (ev.type == "panleft") {
      // no
      var request = new XMLHttpRequest();
      request.open('GET', url+"/add_response/"+document.querySelector(".card-title").textContent+"/0", false);

      request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
          // Success!
          console.log("no");
          var data = JSON.parse(request.responseText);
        } else {
          // We reached our target server, but it returned an error
          
        }
      };

      request.onerror = function() {
        // There was a connection error of some sort
      };

      request.send();
    } else if (ev.type == "panright") {
      // yes
      var request = new XMLHttpRequest();
      request.open('GET', url+"/add_response/"+document.querySelector(".card-title").textContent+"/1", false);

      request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
          // Success!
          console.log("yes");
          var data = JSON.parse(request.responseText);
        } else {
          // We reached our target server, but it returned an error

        }
      };

      request.onerror = function() {
        // There was a connection error of some sort
        
      };

      request.send();
    } else if (ev.type == "pandown") {
      // SUper no
      var request = new XMLHttpRequest();
      request.open('GET', url+"/add_response/"+document.querySelector(".card-title").textContent+"/2", false);

      request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
          // Success!
          console.log("super no");
          var data = JSON.parse(request.responseText);
        } else {
          // We reached our target server, but it returned an error

        }
      };

      request.onerror = function() {
        // There was a connection error of some sort
        
      };

      request.send();
    }
    newthing = cards.pop(0);
    document.querySelector(".card-title").textContent = newthing;
  });








};

request.onerror = function() {
  // There was a connection error of some sort
};

request.send();














  //
    document.getElementById("serious").addEventListener("click", function a() {
    document.getElementById("serious").removeEventListener('click', a);
    console.log("Connecting to Queue");
    document.getElementById("serious").innerHTML = "Connecting...";
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      socket.emit('mode', "serious");
      socket.on('okay', (data)=>{
        console.log("RECEIEVED");
        var options = {'dismissable': true}
        var elem = document.querySelector('.modal');
        var instance = M.Modal.init(elem, options);

        instance.open();
        console.log(data);

        document.getElementsByClassName("username")[0].textContent = data.name;
        document.querySelector('.modal-topic').textContent = data.topic;
        document.querySelector('.modal-emoji').textContent = data.opinion;
        document.querySelector('.header-topic').textContent = data.topic;
        document.querySelector('.header-emoji').textContent = data.opinion;


        instance.open()
        chatBegin();
        socket.on('msg', (datum)=>{
          console.log(datum);
          addMessage(datum, 1);
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
