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

$("#ra").hide();
$("#dec").hide();
$("#filter").hide();
$("#raLabel").hide();
$("#decLabel").hide();
$("#filterLabel").hide();
 $(".listTest").hide();


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
		 $(".listTest").hide();
		 
		 }
		else if ($('input[name ="Tmpformat"]:checked').val() == 'useTmp'){
			$("#tempfile").hide();
			$("#dropDownDest").empty();
			 $(".listTest").show();
			
			var json = {"definitions": [
  {
    "name": "Template One",
    "tooltip" : "Template files are two column files that describe the shape of your variable star. They can be normalized or not. The first column is Phase (from 0 to 1) or some type of Julian date (JD, MJD, HJD, BJD) and the second column should be magnitude",
	"fileName" : "algo1.templ"
	
  },
  {
    "name": "Template Two",
    "tooltip" : "Two Definiton",
	"fileName" : "RRa2.templ"
  },
  {
    "name": "Template Three",
    "tooltip" : "Three Definition",
	"fileName" : "RRa1.templ"
  }
]};

	$.each(json.definitions, function (key, value) 
	{
    $("#dropDownDest").append($('<option></option>').val(value.fileName).html(value.fileName));
});

    
}});});


$(function() {
    $('#nav').on('click','.nav', function ( e ) {
        e.preventDefault();
        $(this).parents('#nav').find('.active').removeClass('active').end().end().addClass('active');
        $(activeTab).show();
    });
});