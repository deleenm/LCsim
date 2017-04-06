var errorBoolean = false;

function errorHandlerFlux(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x <= -3e26)    throw "too low";
        if(x >= 3e26 )   throw "too high";
		else
		{
			errorBoolean= false;
		}
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }	
}


function errorHandlerRightAscension(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x <= 0)    throw "too low";
        if(x >= 360 )   throw "too high";
		else{errorBoolean= false;}
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }	
}


function errorHandlerRightDeclination(inputID,outputID) {
    var error, x;
    error = document.getElementById(outputID);
    error.innerHTML = "";
    x = document.getElementById(inputID).value;
    try { 
        if(x == "")  throw "empty";
        if(isNaN(x)) throw "not a number";
        x = Number(x);
        if(x <= -90)    throw "too low";
        if(x >= 90 )   throw "too high";
		else{errorBoolean= false;}
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }	
}




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
		else{errorBoolean= false;}
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
        if(x < 0)    throw "too low";
		else{
			errorBoolean= false;
			}
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
		else{errorBoolean= false;}
    }
    catch(err) {
        error.innerHTML = "Input is " + err;
		errorBoolean = true;
    }
	}
	
	 
	function validator()
	{
		if(errorBoolean) {
			alert("Please correct the errors");
			return false;}
		else{
			return true;
		}
	}
	
	
	function clearErrors()
	{
		location.reload();
		
	}
