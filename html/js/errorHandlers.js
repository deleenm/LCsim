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

$(document).ready(function(){
$("#obsfile").hide();
$("#ra").hide();
$("#dec").hide();
$("#filter").hide();
$("#raLabel").hide();
$("#decLabel").hide();
$("#filterLabel").hide();
$("#tempfile").hide();

    $('input:radio[name="Obsformat"]').change(function(){
		$("#test").append($('input[name ="Obsformat"]:checked').val());
		
		if ($('input[name ="Obsformat"]:checked').val() == 'uploadObs'){
		 $("#ra").hide();
		 $("#dec").hide();
		 $("#filter").hide();
		 $("#raLabel").hide();
		 $("#decLabel").hide();
		 $("#filterLabel").hide();
		 $("#obsfile").show();
		 
		 }
		else if ($('input[name ="Obsformat"]:checked').val() == 'generateObs'){
			$("#obsfile").hide();
			$("#ra").show();
			$("#dec").show();
			$("#filter").show();
			$("#raLabel").show();
			$("#decLabel").show();
			$("#filterLabel").show();
			} 
		
    });
	
$('input:radio[name="Tmpformat"]').change(function(){
		$("#test").append($('input[name ="Tmpformat"]:checked').val());
		
		if ($('input[name ="Tmpformat"]:checked').val() == 'uploadTmp'){
		 $("#tempfile").show();
		 $(".listTest").empty();
		 
		 }
		else if ($('input[name ="Tmpformat"]:checked').val() == 'useTmp'){
			$("#tempfile").hide();
			
			var json = {"definitions": [
  {
    "name": "Template One",
	"id": "tempfile",
    "tooltip" : "Template files are two column files that describe the shape of your variable star. They can be normalized or not. The first column is Phase (from 0 to 1) or some type of Julian date (JD, MJD, HJD, BJD) and the second column should be magnitude",
	
  },
  {
    "name": "Template Two",
    "tooltip" : "Two Definiton",
  },
  {
    "name": "Template Three",
    "tooltip" : "Three Definition",
  }
]};

			var list = document.getElementsByClassName("listTest")[0];
			var items = json.definitions;
			for(var i = 0; i < items.length; i++) {
			    var h5 = document.createElement("h5");
				h5.innerHTML = items[i].name;
				list.appendChild(h5);
				p = document.createElement("p");
			list.appendChild(p);}
    
}

			 
		
    });
	
	

	
});


$(function() {
    $('#nav').on('click','.nav', function ( e ) {
        e.preventDefault();
        $(this).parents('#nav').find('.active').removeClass('active').end().end().addClass('active');
        $(activeTab).show();
    });
});