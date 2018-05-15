
/*You can run this thing na. it works but it's super messy 
  I'd cry a thousand tears over it*/
console.log('API Key: ' + API_KEY)
console.log('Session ID: ' + SESSION_ID);
console.log('Token: ' + TOKEN);

var session;	

/* buttons */
var start_button = document.getElementById("start_button");
var stop_button = document.getElementById("stop_button");


function publishErrorHandler(error){
	if(error){
		/* The client cannot publish :( */
		alert("Error: ", error.name, error.message);
	}else{
		console.log('Publisher Initialized.');
		session.publish(publisher, function(error){
			if(error){
				alert(error);
			}else{
				console.log('Publishing a stream');
			}
		});
	}
}

function subscribeErrorHandler(error){
	if(error){
		alert("Error: ", error.name, error.message);
	}else{
		console.log('Subscriber Initialized.');
	}
}

var defaultProperty = {
	insertMode: 'append',
	width: '100%',
	height: '100%'
}

function connect(){
	/* Check if user browser supports WebRTC*/
	if (OT.checkSystemRequirements() == 1){
		/* initialize JS Session object 
		   this DOES NOT create an OpenTok session*/
		session = OT.initSession(API_KEY,SESSION_ID);
		
		// Subscribe to newly created stream
		session.on('streamCreated', function(event){
			session.subscribe(event.stream, 'subscriber', defaultProperty, subscribeErrorHandler);
		});

		/* 	Connect to the session
			Check for success using a completion handler function */
		session.connect(TOKEN, function(error){
			if(error){
				if(error.name === "OT_NOT_CONNECTED"){
					showMessage('Failed to connect. Please check your connection and try connecting again.');
				}else{
					console.log("Error connecting: ", error.name, error.message);
				}
			}else{
				console.log("Connected to the session.");
				if(session.capabilities.publish == 1){
						/*  initializes publisher
							publishErrorHandler checks for possible errors
							if no errors are found, session starts publishing
							bad design? ugh. i know. I wanna redo the whole thing
							but nothing makes sense rn*/
						publisher = OT.initPublisher('publisher', defaultProperty, publishErrorHandler);
					}else{
						alert("You cannot publish right now.");
					}
				}
		});

	}else{
		/* error message to display if user's browser does not support WebRTC*/
		alert("Your browser does not support WebRTC");
	}

}

function disconnect(){
	session.disconnect();
}


connect();