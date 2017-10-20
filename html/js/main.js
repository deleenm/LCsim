var btn = document.getElementById("btn");
var animalContainer = document.getElementById("info");
var counter = 1;

btn.addEventListener('click', function()
{
	$.getJSON("definitions.json", function(json) {
    console.log(json); // this will show the info it in firebug console
	});
});	


function render(data){
	var string= "";
	for (i = 0 ; i < data.length ; i++)
	{
		string += "<p>" + data[i].name;
		
		
		string += ".</p>";
	}
	animalContainer.insertAdjacentHTML('beforeend',string);
}