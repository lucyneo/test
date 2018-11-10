

function onload(){
    
    document.getElementById("input2").style.display="none";
}

function edit2(){
    var currenttext=document.getElementById("colh2").innerText;
    $("#colh2").hide();
    $("#input2").show();  
    document.getElementById("input22").value=currenttext;
}
function save2(){
    var newtext=document.getElementById("input22").value;
    $("#colh2").show();
    $("#input2").hide();
    document.getElementById("colh2text").innerHTML=newtext;
}

