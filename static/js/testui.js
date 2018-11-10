
// var obutton = document.getElementById("tb_subject").getElementsByTagName("button");


// for (var i = obutton.length - 1; i >= 0; i--) {
//     obutton[i].onclick = function(){
//        var subjectname = $(this).parents("tr").find("#subjectname").text(); 
//        alert(subjectname);
//     }
// }


function myFunction(elem) {
    var subjectname = $(elem).parents("tr").find("#subjectname").text(); 
    alert(subjectname);
    document.cookie="subjectname="+subjectname;
    //window.location.href="/starttest";
    // $.post("/setsubjectcookie",  
    //         {  
    //         subjectname:subjectname, 
    //         },
    //         function(data)
    //             { 
    //             // var dialog=document.getElementById("modal-add")
    //             // dialog.close();
    //             alert(data);
    //             window.location.href="/starttest";
    //             }
    //         )
    PostSubmit("/starttest/", subjectname, subjectname)
}

function PostSubmit(url, data, msg) {  
    var postUrl = url;//提交地址  
    var postData = data;//第一个数据  
    var msgData = msg;//第二个数据  
    var ExportForm = document.createElement("FORM");  
    document.body.appendChild(ExportForm);  
    ExportForm.method = "POST";  
    var newElement = document.createElement("input");  
    newElement.setAttribute("name", "subjectname");  
    newElement.setAttribute("type", "hidden");  
    var newElement2 = document.createElement("input");  
    newElement2.setAttribute("name", "no");  
    newElement2.setAttribute("type", "hidden");  
    ExportForm.appendChild(newElement);  
    ExportForm.appendChild(newElement2);  
    newElement.value = postData;  
    newElement2.value = msgData;  
    ExportForm.action = postUrl;  
    ExportForm.submit();  
};  

       

// $("#testin").click(function () {
//     //alert("wwww");
//     var subjectname = $(this).parents("tr").find("#subjectname").text(); 
//     alert(subjectname);
    
//     // $.post("/starttest/",  
//     //         {  
//     //         subjectname:subjectname, 
//     //         },
//     //         function(data)
//     //             { 
//     //             // var dialog=document.getElementById("modal-add")
//     //             // dialog.close();
//     //             //$("#modal-add").hide();
//     //             }
//     //         )

// });





// $("#testin",this).click(function(){
//     alert("wwww");
//     // var subjectname = $(this).parents("tr").find("#subjectname").text(); 
    
//     // alert(subjectname);

// });  