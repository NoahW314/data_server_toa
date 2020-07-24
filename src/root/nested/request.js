var sendData = function(dataToSend){
	console.log("Sending")
	$.ajax({
		error:function(xhr, status, error){
			console.log("Status: "+status)
			console.log(xhr.responseText)
			console.log(xhr.responseXML)
			console.log(error)
			$("#submit").attr("disabled", false).attr("enabled", true)
		},
		success:function(data, status, xhr){
			console.log("Data: "+data)
			console.log("Status: "+status)
			console.log("Request: "+xhr)
			$("#result").empty()
			$("#result").append(data)
			$("#submit").attr("disabled", false).attr("enabled", true)
			console.log("Finished!")
		},
		contentType:"application/json; charset=utf-8",
		data:JSON.stringify(dataToSend),
		type:"POST",
		url:"http://localhost:8000/"
	})
}

var idStrings = {
	"Team":"team",
	"Match":"match",
	"Event":"event",
	"Region":"region",
	"Season":"season",
	"":""
}

var onPrimaryChanged = function(selector, info_type){
	var selection = idStrings[selector.val()]
	var infoType = info_type.val()
	var secondaryID = "#select_"+selection
	console.log("Secondary Element ID: "+secondaryID)
	
	
	/**hide all secondary span elements and input divs*/
	$(".secondary_span").attr("hidden", true)
	$(".input_div").attr("hidden", true)
	
	
	/**show new secondary*/
	
	//check that we have a secondary has been selected
	if(selection !== ""){
	
		//if new secondary doesn't exist (first choice is season, region or info type is info, compare)
		if(selection === "region" || selection === "season" || (selection !== "team" && (infoType === "info" || infoType === "compare"))){
			//show input div
			var inputDivID = "#select_"+selection+"_div"
			$(inputDivID).attr("hidden", false)
			
			if(infoType === "compare"){
				$("#select_"+selection+"_compare_div").attr("hidden", false)
			}
			
			$("#submit").attr("disabled", false).attr("enabled", true)
		}
		else {
			//show secondary selector span
			$(secondaryID+"_span").attr("hidden", false)
			
			//if new secondary already has selection, call onSecondaryChanged
			onSecondaryChanged($(secondaryID))
		}
	}
}
var onSecondaryChanged = function(selector){
	var idOfSelector = selector.attr("id")
	if(selector.val() === ""){return}
	var idOfInputDiv = "#"+idOfSelector+"_"+idStrings[selector.val()]+"_div"
	console.log("Input Div ID: "+idOfInputDiv)
	
	/**hide all input divs*/
	$(".input_div").attr("hidden", true)
	
	/**show new input div*/
	$(idOfInputDiv).attr("hidden", false)
	
	$("#submit").attr("disabled", false).attr("enabled", true)
}


var getInputData = function(data){
	switch(data["AnalysisType"]){
		case "team":
			switch(data["InfoType"]){
				case "info":
				case "compare":
				case "rank":
			}
		case "match":
			switch(data["InfoType"]){
				case "info":
				case "compare":
				case "rank":
			}
		case "event":
			switch(data["InfoType"]){
				case "info":
				case "compare":
				case "rank":
			}
		case "region":
			switch(data["InfoType"]){
				case "info":
				case "compare":
				case "rank":
			}
		case "season":
			var seasonNumInput = $($("#select_season_div").children()[0])
			switch(data["InfoType"]){
				case "info":
				case "rank":
					var name = seasonNumInput.attr("name")
					return {
						name:seasonNumInput.val()
					}
				case "compare":
					var season2NumInput = $($("#select_season_compare_div").children()[0])
					var name = seasonNumInput.attr("name")
					var name2 = season2NumInput.attr("name")
					console.log(name+" "+name2)
					var inputData = {}
					inputData[name] = seasonNumInput.val()
					inputData[name2] = season2NumInput.val()
					return inputData
			}
		default:
			return ""
	}
}
var getSecondaryAnalysisType = function(data){
	switch(data["AnalysisType"]){
		case "region":
		case "season":
		case "":
			return ""
		case "team":
			return idStrings[$("#select_team").val()]
		default:
			if(data["InfoType"] === "rank"){return $("#select_"+idStrings[data["AnalysisType"]]).val()}
			else{return ""}
	}
}