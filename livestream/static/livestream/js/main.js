
/*do not run yet*/

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
		session.connect(token, function(error){
			if(error){
				console.log("Error connecting: ", error.name, error.message);
			}else{
				console.log("Connected to the session.");
			}
		});

	}else{
		/* error message to display if user's browser does not support WebRTC*/
		alert("Your browser does not support WebRTC");
	}

}
