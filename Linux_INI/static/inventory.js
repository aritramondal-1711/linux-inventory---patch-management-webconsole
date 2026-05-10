function formshow() {
    window.location.href="/add";
}

function hideform() {
    window.location.href="/";
}

function closemsg(elid) {
    document.getElementById(elid).id="msg";
}

const checkboxes=document.querySelectorAll('.checkboxes')
const removebth=document.getElementById('Remove')
const patchbth=document.getElementById('Patch')


checkboxes.forEach((cb) => {
    cb.addEventListener("change",()=>{
        const anychecked=Array.from(checkboxes).some((c) => {return c.checked});
        removebth.disabled=!anychecked;
        patchbth.disabled=!anychecked;
    })  
})

function checkConfirmation(server){
    let hosts = [];
    for(let i=0; i<server.length; i++){
        hosts[i]=server[i]+"\n";
    }
    return confirm("Are you sure you want to proceed with deletion of below servers from the Inventory ?\n"+hosts)
}

function deletesrv() {
    const checkedboxes=document.querySelectorAll('.checkboxes:checked');
    const allchecked=Array.from(checkedboxes).map((c) => {return c.value});
    const confirmation=checkConfirmation(allchecked);
    if(confirmation){
        fetch("/delete",{
            method:"POST",
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body:JSON.stringify({servers:allchecked})
        }).
        then(res => res.json()).
        then(data => {
            if(data.status=="Success"){
                let hosts = [];
                for(let i=0; i<data.servers.length; i++){
                    hosts[i]=data.servers[i]+"\n";
                }
                alert("Suceessfuly deleted below servers from inventory - \n"+hosts)
                window.location.href="/";
            }
            else{
                alert(data.msg)
            }
        }).
        catch( err => {
            alert("Error Occurred: "+err)
        })
    }
}

function patchsrv(){
    const checkedboxes=document.querySelectorAll('.checkboxes:checked');
    const allchecked=Array.from(checkedboxes).map((c) => {return c.value});
    
    let hosts=[]
    for(let i=0; i<allchecked.length;i++){
        hosts[i]=allchecked[i]+"\n";
    }

    const getconfirm=confirm("Are you sure to initiate patching for below servers ?\n"+hosts);
    if(getconfirm){
        let querystring=allchecked.join("&servers=");
        window.location.href="/patch?servers="+querystring;
    }

}

function patchinitiate(){
    document.getElementById("patchhead").style.display="block";
    document.getElementById("patchheading").style.display="none";
    document.getElementById("warning").style.display="none";
    document.getElementById("patchform").style.display="none";
}

function searchtable(){
    const searched=document.getElementById("searchid").value.toUpperCase();
    const table=document.getElementById("table");
    const row=table.getElementsByTagName("tr");
    for(let i=1;i<row.length;i++){
        let data=row[i].getElementsByTagName("td")[0].textContent.toUpperCase();
        let env=row[i].getElementsByTagName("td")[1].textContent.toUpperCase();
        let os=row[i].getElementsByTagName("td")[2].textContent.toUpperCase();
        let uptime=row[i].getElementsByTagName("td")[3].textContent.toUpperCase();
        if(data.indexOf(searched) > -1 || env.indexOf(searched) > -1 || os.indexOf(searched) > -1 || uptime.indexOf(searched) > -1 || searched == ""){
            row[i].style.display="";
        }
        else{
            row[i].style.display="none";
        }
    }

}