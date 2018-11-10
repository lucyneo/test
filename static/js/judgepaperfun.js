

function myFunction(elem) {

    var questionid = $(elem).next(".hidden").text(); 
    var paperid=$(elem).next(".hidden").next(".hidden").text();
    var score=$(elem).parents('.input-group').find(".form-control").val();


    //alert(questionid+paperid+score);
    
    $.post("/submitscore/",  
            {  
            paperid:paperid,
            score:score,
            questionid:questionid,
            },
            function(data)
                { 
                // var dialog=document.getElementById("modal-add")
                // dialog.close();
                alert(data);
                }
            )
}

