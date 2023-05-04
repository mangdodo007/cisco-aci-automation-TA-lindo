# Purpose of this program?
To provision ACI and MSO using ansible.



# How to use the program?


1. First time using this program, you need to install requirements.txt (pip install -r requirements.txt) (first time only if you already install requirement you can skip this step)
2. Input your parameter in the excel file ~/CISCO-ACI-AUTOMATION/helpers directory. E.g, Test.xlsx (extension excel should be .xlsx, you can use excel template, template.xlsx)
3. run the python script main.py and select menu 31 (Convert Excel to YAML) to convert the excel inputs to yaml variable files.
4. run the python script main.py to execute every task you want to execute.

Directory structure:

1. **~/CISCO-ACI-AUTOMATION/helpers**
contain the excel input file.


2. **~/CISCO-ACI-AUTOMATION/vars**
contain all the yaml variables files that was converted from excel.

3. **~/CISCO-ACI-AUTOMATION/methods**
This is the root project directory.
Contain the main playbooks

4. **~/CISCO-ACI-AUTOMATION/**
Contain the main program (main.py)
Contain any settings and information

# How to convert the excel inputs to yaml variable?

- in ~/CISCO-ACI-AUTOMATION/helpers directory make sure your excel file is exists in this directory.
e.g, **test.xlsx**


- in ~/CISCO-ACI-AUTOMATION/ directory, run python script main.py (python3 main.py), select menu 31 (Convert Excel to YAML) and input the excel name E.g, test.xlsx and then yaml variable files like the following will be generated on ~/CISCO-ACI-AUTOMATION/vars directory 
    - **system_setting_test.yml**


- note that the name of the yaml variable has some relation with the excel input file (test.xlsx) so that we can define
different variable files


- if you make any changes to the excel input file, you will need to re-run the convert exel to yaml script again to re-generate the
yaml variable files.

- if you want to clear ~/CISCO-ACI-AUTOMATION/vars directory you can use menu 32 (Clear Vars Folder) to delete all file contain .yml




# How to run the playbook to provision to aci?
python3 main.py, select menu to execute every task you want to execute

There is no need to specify inventory file. The program will prompt you for 
- APIC or MSO ip address
- Username
- Password
- excel file (without extension)
- Just key the parameters and it will run. Reason for doing this is to prevent errors when you have to provision ACI in Multisite environment.


if you want to run only particular section of a playbook, you can run every playbook at method/(name of function E.g fabric_policies)/executes/:
- ansible-playbook admin_create_task.yml --tag <tags-to-use>
- e.g, ansible-playbook admin_create_task.yml --tag input,export_policy       #input tag is required as it will prompt u for host. Else will have error 

You can also list the tags available in a playbook using:
- ansible-playbook admin_create_task.yml --list-tags

# Ansible and Python version
- Ansible 4.4.0 (required to support some modules)
- Python version 3.x
