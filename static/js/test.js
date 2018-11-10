


function myFunction(elem) {
    // var subjectname = $(elem).parents("div").find(".hiden").val(); 
    var questionid = $(elem).next(".hidden").text(); 
    // var answerchoice= $("#answerchoice").val(); 
    // var answer=$("#answer").val(); 
    var paperid=$("#paperidlabel").text(); 
    var ischoice=$(elem).next(".hidden").next(".hidden").text();
    
    if (ischoice==0)
        {
            var answer=$(elem).parents('.input-group').find(".form-control").val();
           
        }
    else
        {
            var answerchoice= $(elem).parents("div").prev("div").find(".form-control").val();
            var answerlist= document.getElementsByName("choice");
            if (answerchoice=='A')
                {
                    var answer=answerlist[0].innerHTML;
                }
            if (answerchoice=='B')
                {
                    var answer=answerlist[1].innerHTML;             
                }
            if (answerchoice=='C')
                {
                    var answer=answerlist[2].innerHTML;         
                }
            if (answerchoice=='D')
                {
                    var answer=answerlist[3].innerHTML;
                }
            
           
        }
    // alert(answer)
    //window.location.href="/starttest";
    
    $.post("/submitanswer/",  
            {  
            paperid:paperid,
            answer:answer,
            questionid:questionid,
            ischoice:ischoice,
            },
            function(data)
                { 
                // var dialog=document.getElementById("modal-add")
                // dialog.close();
                alert(data);
                }
            )
}