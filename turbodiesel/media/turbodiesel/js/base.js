$(document).ready(function () {
    $(".select").chosen();
    $(".datetime").datepicker({
        inline: true
    });
    $('.tags_input').tagsInput();
    $(".date").datepicker({
        inline: true
    });

    $('.table').dataTable({
        "sScrollX": "100%",
        "sScrollXInner": "145%",
        "bScrollCollapse": true
    });
    var editor = $( '.wysiwyg' ).ckeditor();
    editor.height = 559;
    /*	$(".textarea").kendoEditor({tools:[
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

     });*/

})
