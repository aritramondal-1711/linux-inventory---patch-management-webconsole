from django.shortcuts import render, redirect
from .models import linux_inventory
import subprocess
import json
from django.http import JsonResponse
import os

# Create your views here.
def inventory(req):
    Linux_Inventory=linux_inventory.objects.all()
    print(Linux_Inventory)
    for hosts in Linux_Inventory:
        os_v=subprocess.run(["ssh",hosts.servername,"cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f 2"],text=True,capture_output=True)
        upt=subprocess.run(["ssh",hosts.servername,"uptime | cut -d ',' -f 1 | awk -F 'up' '{print $NF}'"],text=True,capture_output=True)
        if os_v.returncode != 0:
            os_version="SSH Failed"
        else:
            os_version=os_v.stdout

        if upt.returncode != 0:
            uptime="SSH Failed"
        else:
            uptime=upt.stdout

        linux_inventory.objects.filter(servername=hosts.servername).update(os_version=os_version,uptime=uptime)
    
    Linux_Inventory=linux_inventory.objects.all()

    return render(req,'inventory.html',{'Linux_Inventory':Linux_Inventory})

def addserver(req):
    msg=dict({})
    if req.method == "POST":
        servername=req.POST.get("servername")

        # Checking if the new server to be added is already in the inventory or not
        allserers=linux_inventory.objects.all()
        flag=0
        for host in allserers:
            if host.servername == servername:
                flag=1
                break
        
        # If the new server is not a exising one, proceed to add
        if flag == 0:
            servergroup=req.POST.get("servergroup")
            os_v=subprocess.run(["ssh",servername,"cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f 2"],text=True,capture_output=True)
            upt=subprocess.run(["ssh",servername,"uptime | cut -d ',' -f 1 | awk -F 'up' '{print $NF}'"],text=True,capture_output=True)

            print(os_v)
            print(upt)
            if os_v.returncode != 0:
                os_version="SSH Failed"
            else:
                os_version=os_v.stdout

            if upt.returncode != 0:
                uptime="SSH Failed"
            else:
                uptime=upt.stdout

            linux_inventory.objects.create(servername=servername,servergroup=servergroup,os_version=os_version,uptime=uptime)
            msg["message"]=f"The server {servername} is added to the inventory"
            msg["style"]="green"


        # IF it's a existing one throw error
        else:
            msg["message"]=f"{servername} already exists in the inventory"
            msg["style"]="red"
    else:
        msg["style"]="msg"
        msg["message"]=""
    return render(req,'addserver.html',{'msg':msg})

def delserver(req):
    if req.method == "POST":
        try:
            data=json.loads(req.body)
            servers=data.get("servers",[])
            for servername in servers:
                linux_inventory.objects.filter(servername=servername).delete()
            return JsonResponse({"status":"Success","servers":servers})
        except Exception as err:
            return JsonResponse({"status":"Failed","msg":"Deletion failed with error "+err})

    return redirect("/")


def patchjob(req):
    if req.method == "GET":
        servers=req.GET.getlist("servers")
        return render(req,'patch.html',{"servers":servers})
    else:
        return redirect("/")
    
def patchinitiate(req):
    if req.method == "POST":
        servers=req.POST.getlist("servers")
        curdir=os.getcwd()

        with open(os.path.join(curdir,"hosts"),"w") as f:
            for server in servers:
                f.write(server+"\n")
        
        # Get Timestamp
        time=subprocess.run("date +%d%m%Y-%H%M%S",shell=True,text=True,capture_output=True)

        # Create directories
        logdir = os.path.join(curdir, "patchlogs")
        os.makedirs(logdir, exist_ok=True)

        precheck_dir = os.path.join(logdir,"prechecks")
        os.makedirs(precheck_dir, exist_ok=True)

        postcheck_dir = os.path.join(logdir,"postchecks")
        os.makedirs(postcheck_dir, exist_ok=True)
        

        # Create log files
        logfile=os.path.join(curdir,f"patchlogs/logs-{time.stdout.strip()}.txt")
        precheck_file=os.path.join(precheck_dir,f"precheck-{time.stdout.strip()}.txt")
        postcheck_file=os.path.join(postcheck_dir,f"postcheck-{time.stdout.strip()}.txt")

        with open(precheck_file,"w") as f:
            f.write("***********************************************")

        with open(postcheck_file,"w") as f:
            f.write("***********************************************")

        subprocess.run(["sudo","chmod","-R","744",f"{logdir}"])

        # Run Ansible for Patching
        result=subprocess.Popen(["ansible-playbook","-i","hosts","patch.yml","-e",f"precheck_file={precheck_file}","-e",f"postcheck_file={postcheck_file}"],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        # Saving & Retriving the files
        log=[]
        with open(logfile,"w") as f:
            for line in result.stdout:
                f.write(line)
                log.append(line)

        pre=[]
        with open(precheck_file,"r") as f:
            for line in f:
                pre.append(line.strip)

        post=[]
        with open(postcheck_file,"r") as f:
            for line in f:
                post.append(line.strip)


        message="The the logs for this operation is stored in file -"
        filename=logfile

        return render(req,"patchresult.html",{"log":log,"message":message,"filename":filename,"prechecklog":pre,"precheck_file":precheck_file,"postchecklog":post,"postcheck_file":postcheck_file})
    else:
        return redirect("/")
        
