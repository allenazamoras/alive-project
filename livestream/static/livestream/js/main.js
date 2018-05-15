
/*do not run yet*/
console.log('API Key: ' + API_KEY)
console.log('Session ID: ' + SESSION_ID);
console.log('Token: ' + TOKEN);

var session;	

/* buttons */
var start_button = document.getElementById("start_button");
var stop_button = document.getElementById("stop_button");

function connect(){
	/* Check if user browser supports WebRTC*/
	if (OT.checkSystemRequirements() == 1){
		/* initialize JS Session object 
		   this DOES NOT create an OpenTok session*/
		session = OT.initSession(API_KEY,SESSION_ID);
		/* Check for success using a completion handler function */
		session.connect(TOKEN, function(error){
			if(error){
				if(error.name === "OT_NOT_CONNECTED"){
					showMessage('Failed to connect. Please check your connection and try connecting again.');
				}else{
					console.log("Error connecting: ", error.name, error.message);
				}
			}else{
				console.log("Connected to the session.");
				// WE CAN FRICKEN STREAM NA WITCHEEEEZZZZZ
				publish();
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

function publish(){
	var publisher;
	var targetElement = 'publisherContainer';
	/* Check if client has publish capabilities */
	if(session.capabilities.publish == 1){
		/**/
		publisher = OT.initPublisher(targetElement, null, function(error){
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
				// publisher.on({
				// 	accessAllowed: function(event){
				// 		/* User has granted acess to camera and mic */
				// 	}
				// 	accessDenied: function accessDeniedHandler(event){
				// 		/* User has denied access to camera and mic */
				// 	}
				// });
			}
		});
	}else{
		alert("You cannot publish right now.");
	}

	var audioInputDevices;
	var videoInputDevices;
	OT.getDevices(function(error, devices) {
		audioInputDevices = devices.filter(function(element) {
			return element.kind == "audioInput";
		});
		videoInputDevices = devices.filter(function(element) {
			return element.kind == "videoInput";
		});
		for (var i = 0; i < audioInputDevices.length; i++) {
			console.log("audio input device: ", audioInputDevices[i].deviceId);
		}
		for (i = 0; i < videoInputDevices.length; i++) {
			console.log("video input device: ", videoInputDevices[i].deviceId);
		}
	});

	var pubOptions =
	{
		audioSource: audioInputDevices[0].deviceId,
		videoSource: videoInputDevices[0].deviceId
	};
	var publisher = OT.initPublisher(null, pubOptions, function(error) {
		console.log("OT.initPublisher error: ", error);
	});
}

connect();