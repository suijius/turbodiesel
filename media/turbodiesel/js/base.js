$(document).ready(function() {
	$(".select").kendoDropDownList();
	$(".datetime").kendoDateTimePicker({
    	format: "dd.MM.yyyy hh:mm:ss",
    	culture: "ru-RU"
	});
	$('.tags_input').tagsInput();
		$(".date").kendoDatePicker({
    	format: "dd.MM.yyyy",
    	culture: "ru-RU"
	});
	$(".textarea").kendoEditor({tools:[
         "bold",
         "italic",
         "underline",
         "strikethrough",
         "foreColor",
         "backColor",
         "justifyLeft",
         "justifyCenter",
         "justifyRight",
         "justifyFull",
        "insertUnorderedList",
         "insertOrderedList",
         "indent",
         "outdent",
          "fontName",
         "fontSize",
         "formatBlock",
	 "viewHtml",
	"insertImage",	
"createLink",
                "unlink"]

         });

})
