//Page Created: December 1, 2017
//handles all the user interactive features in HTML pages

$(document).ready(function(){
$("#ra").hide();
$("#dec").hide();
$("#filter").hide();
$("#raLabel").hide();
$("#decLabel").hide();
$("#filterLabel").hide();
 $(".templateTable").hide();


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
		 $(".templateTable").hide();
		 $('table#tbl TBODY').empty();

		 }
		else if ($('input[name ="Tmpformat"]:checked').val() == 'useTmp'){
			$("#tempfile").hide();
			$("#dropDownDest").empty();
			 $(".templateTable").show();

			var json = {"definitions": [
  {
	"fileName" : "layden98_algol.templ",
    "description" : "Algol Eclipsing Binary",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_RRa1.templ",
    "description" : "RRab RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
    {
	"fileName" : "layden98_RRa2.templ",
    "description" : "RRab RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_RRa3.templ",
    "description" : "RRab RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_RRb1.templ",
    "description" : "RRab RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
    {
	"fileName" : "layden98_RRb2.templ",
    "description" : "RRab RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_RRc.templ",
    "description" : "RRc RR Lyrae",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_sin.templ",
    "description" : "Pure Sine Wave",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  },
  {
	"fileName" : "layden98_w_uma.templ",
    "description" : "W Ursae Majoris Eclipsing Binary",
	"ref_short": "Layden (1998)",
	"reference": "Layden, A.C. 1998, AJ, 115, 193",
  }
]};

	$.each(json.definitions, function (key, value)
	{
    $('table#tbl TBODY').append('<tr><td><label><input type="radio" id="RadioGroup4_0" value= "'+value.fileName+'" name="optradio">'+' '+value.fileName+'</label></td><td>' +value.description +' </td><td> ' +value.ref_short +'</td><td> '+value.reference +'</td></tr>');
    });
};


}

);});


$(function() {
    $('#nav').on('click','.nav', function ( e ) {
        e.preventDefault();
        $(this).parents('#nav').find('.active').removeClass('active').end().end().addClass('active');
        $(activeTab).show();
    });
});
