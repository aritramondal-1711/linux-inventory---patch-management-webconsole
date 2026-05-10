### Agentless Linux Inventory & Patch Management Web Console using Django & Ansible

## Topic: Linux Inventory & Patch management WebUI Console

# Prerequisites:
    • The remote servers should be accessible in network
    • The remote servers should have passwordless ssh configuration
    • The central or control server should have python, ansible, django installaed and configured
    • If the added server is not accessible using SSH, it will show SSH Failed, otherwise, it will have OS and uptime field

# Setup:
    • The project is running on localhost:8000
    • I have NGINX configured for reverse proxy to localhost:8000
<img width="1515" height="661" alt="image" src="https://github.com/user-attachments/assets/00cac967-629e-434c-9290-7fef0ee4a732" />
      
    • I don not have a proper DNS entry but I had done hosts file entry for this 
<img width="665" height="150" alt="image" src="https://github.com/user-attachments/assets/360de53d-6f78-4744-be07-576a8a8780c9" />


# WebGUI Go THrough:

    • The first look to the inventory (home page)
<img width="1861" height="535" alt="image" src="https://github.com/user-attachments/assets/d5c3ffa1-679e-4e48-afbe-fdc4cdc8e48a" />

    • The Delete and Patch buttons are by default disabled
    • These two will get enabled once at least one of the checkboxes against servers will be selected
<img width="1861" height="535" alt="image" src="https://github.com/user-attachments/assets/c9a7e0ab-f0c4-499c-b7f0-1a5769dbed61" />

    • One can also search by any keyward. The table will reflect if the keyward matches to any of the field
<img width="1861" height="535" alt="image" src="https://github.com/user-attachments/assets/c389fa36-b1da-4263-a9f5-7e35175e3a18" />

    • The above were pure HTML, CSS, Java Script in play
    • The table fields are from django showing data from db. Before showing the uptime & os fields will be once again fetched and saved in db and then will be provided to frontend.


    • Now, click on Add server button to add new servers
    • This will redirect to a form for server addition
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/dea5b5db-d99b-44f1-9e72-253bb21e490c" />
  
    • Once submitted, it will add the server in db and show a message that the server is added
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/39f3a934-df50-45c9-9456-cec34270c581" />

    • It is not possible to add same server twice. It will throw a error
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/bf8bbfb3-191c-434b-a100-7e217656a72b" />

    • Go back to inventory, and the new servers will be visible with uptime and OS field
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/625ae3f6-ab0a-4a79-8964-39b6c7874d2d" />
  

    • Select the servers to be deleted and click on Remove Servers
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/70339301-8900-46d7-8b0f-0e1575e1c51f" />
    
    • It will ask for confirmation
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/99511b1b-4e27-4d41-9e9a-026457db3a33" />

    • Once confirmed it will delete the servers from db and redirect to inventory and the removed servers will be gone
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/349b9382-1519-4bee-8e6a-e0fc3f5141c3" />


    • Now Let’s move to highlight which is agentless remote patching
    • Select servers and click on Patch
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/374dc3b5-64a1-422c-83ef-5bd7f2d4d0bd" />
  
    • This will ask for confirmation and once confirmed, it will redirect to a page where the selected servers will be shown and will give options to initiate patching or cancel patching
    • Click on initiate patching to proceed with patching
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/a4ee8a9a-074a-48ef-a0a3-0b7b2943a393" />

    • This is totally agent less.
    • The backend will use Ansible to perform this patching
    • The Ansible will take prechecks → save in precheck file → initiate patching → store ansible output in a file → take postchecks → stote the postcheck in a file
    • During the patch process, the webui will show  a loading like “Patching in progress …”
<img width="1847" height="784" alt="image" src="https://github.com/user-attachments/assets/25f2cd8d-06ae-414f-b97d-9d7c5c51eb6b" />

    • Once Patching is done, it will redirect to a page where the ansible output, pre/post checks and stored file patchs will be shown
<img width="1811" height="930" alt="image" src="https://github.com/user-attachments/assets/464a4014-d84b-4b01-8056-24b8d82f146b" />























