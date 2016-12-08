	
	var errorBoolean = false;
	
	
	function errorHandlerPhase(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x < 0)    throw "too low";
        if(x >= 1)   throw "too high";
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }
}
	function errorHandler(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x <= 0)    throw "too low";
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }
	
	

}
	function errorHandlerLightObs(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x < 0)    throw "too low";
        if(x >= 1000)   throw "too high";
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }
	}
	
	
	function validator()
	{
		if(errorBoolean) window.alert("Please correct the errors");
	}