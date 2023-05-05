import os
import sys
import yaml
import getpass
import re
from methods.excel_parse_method import xl2yaml_new

# make sure the item for every data menu is 18 items
data1 = (
   "SYSTEM SETTING:",              
   "    1. System Setting",        
   "ADMIN:",                       
   "    2. Admin",                	
   "FABRIC DISCOVERY:",           
   "    3. POD Fabric Setup",    
   "    4. Fabric Membership",     		
   "    5. Node Management Address",
           
)

data2 = (
  "FABRIC POLICIES:",            
   "    6. Policies",              
   "    7. Switch Policy Group",    
   "    8. Switch Profile",         
   "    9. POD Policy Group",     
   "    10. POD Profile",
   "",
   "",
   
)

data3 = (
   "FABRIC ACCESS POLICIES 1:",             
   "    11. Access Policies",                
   "    12. Pools",                         
   "    13. Domains",    
   "TOOLS:",
   "    31. Convert Excel to YAML",
   "    32. Clear Vars Folder",
   "     0. Quit",
)


# BASE DIR
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)



class Menu():

	def __init__(self):

		self.choices = {
		"1" : self.sysSetting,
		"2" : self.admin,
		"3"	: self.podSetup,
		"4" : self.fabMembership,
		"5" : self.nodeMgmt,
		"6" : self.fabPolicies,
		"7" : self.swPG,
		"8" : self.swProf,
		"9" : self.podPG,
		"10" : self.podProf,
		"11" : self.accPolicies,
		"12" : self.pools,
		"13" : self.domains,
		"31" : self.xltoyml,
        "32" : self.clear_var,
		"0" : self.quit
		}

	def openPrompt(self):

		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			Requirement:
			• Make sure You already fill the Excel file on helpers directory.
			• Make sure You have IP, user, pass, excel name of APIC.
			""")

	def display_menu(self):

		len_data1 = []
		len_data2 = []
		len_data3 = []
		print("\nCisco ACI Configuration Task :\n")
		for i, v, c in zip(data1, data2, data3):
			len_data1.append(len(i))
			len_data2.append(len(v))
			len_data3.append(len(c))

		for i, v, c in zip(data1, data2, data3):
			space_req_data1 = max(len_data1) - len(i)
			space_req_data2 = max(len_data2) - len(v)
			print(" " * 4, i, " " * space_req_data1, v, " " * space_req_data2, c)
		print()

	def run(self):
		# Menu
		list1 = []
		list2 = []
		temp_list = []
		cmd_list = []
		while True:
			self.clear()
			self.openPrompt()
			self.display_menu()
			choice = input("Enter your choices (number followed by , or -): ")
			choice_ = re.search("[^0-9,-]", choice)
			# handling input user
			choice_nospace = choice.replace(" ", "")
			choice_list = choice_nospace.split(",")
			try:
				for _choice in choice_list:
					if "-" not in _choice:
						list1.append(int(_choice))
					else:
						temp_list.append(_choice)
				# choice range
				for i in temp_list:
					_temp_list = i.split("-")
					range_list = range(int(_temp_list[0]), int(_temp_list[1]) + 1)
					for c in range_list:
						list2.append(int(c))
				total_list = list1 + list2
				total_list.sort()
				cmd_list = [str(i) for i in total_list]	
			except Exception as ex:
				print(f"WARNING: Invalid menu choice / structure. Please try again.")
				print(f"Example: 1,2,3,4,5 or 1-5")
			# Run Ansible Playbook one by one
			if choice_ or choice == "":
				print(f"WARNING: Wrong Input.. Press Enter key to Continue...")
				input()
			else:
				if "32" in cmd_list or "31" in cmd_list or "0" in cmd_list:
					action = self.choices.get(choice)
					if action:
						action()
					else:
						print("\n{0} is not a valid choice!.. Press Enter key to Continue...\n".format(choice))
						input()				
					self.reset_input()
					self.run()
				else:
					self.get_input()
					for cmd in cmd_list:
						action = self.choices.get(cmd)
						if action:
							action()
						else:
							print("\n{0} is not a valid choice!.. Press Enter key to Continue...\n".format(choice))
							input()
					self.reset_input()
					self.run()

	def sysSetting(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tSystem Setting will be configure:
			\t\t• MP BGP            • IP Aging
			\t\t• Banner and Alias  • Remote EP Learning
			\t\t• Timezone          • AES Encryption
			\t\t• OOB Preference
			""")

		#Configuring System Setting
		cmd = 'ansible-playbook methods/system_setting/executes/system_setting_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def admin(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tAdmin will be configure:
			\t\t• Export Policy • Security Domain
			\t\t• Local User    
			""")
		cmd = 'ansible-playbook methods/admin/executes/admin_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def podSetup(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tPOD Fabric Setup will be configure:
			\t\t• POD
			\t\t• POD TEP Pool
			""")

        #Configuring POD Setup
		cmd = 'ansible-playbook methods/fabric_discovery/executes/fabric_discovery_pod_setup_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def fabMembership(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tFabric Membership will be configure:
			\t\t• Fabric Discovery
			""")

        #Configuring POD Setup
		cmd = 'ansible-playbook methods/fabric_discovery/executes/fabric_discovery_membership_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def nodeMgmt(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tNode Management Address will be configure:
			\t\t• OOB Management
			\t\t• In-Band Management
			\t\t• Site Building
			""")

        #Configuring POD Setup
		cmd = 'ansible-playbook methods/fabric_discovery/executes/fabric_discovery_node_mgmt_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def fabPolicies(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tFabric Policies will be configure:
			\t\t• NTP Policy           • SNMP Policy
			\t\t• ISIS Policy          • Fabric Node Controls
			\t\t• Power Supply Policy
			""")
		cmd = 'ansible-playbook methods/fabric_policies/executes/fabric_policies_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def swPG(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tFabric Switch Policy Group will be configure:
			\t\t• Fabric Leaf Policy Group
			\t\t• Fabric Spine Policy Group
			""")
		cmd = 'ansible-playbook methods/fabric_policies/executes/fabric_policies_switch_group_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def swProf(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tFabric Switch Profile will be configure:
			\t\t• Fabric Leaf Profile
			\t\t• Fabric Spine Profile
			""")

		cmd = 'ansible-playbook methods/fabric_policies/executes/fabric_policies_switch_profile_create_task.yml'

	
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def podPG(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tPOD Policy Group will be configure:
			\t\t• POD Policy Group
			""")

		cmd = 'ansible-playbook methods/fabric_policies/executes/fabric_policies_pod_group_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def podProf(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tPOD Profile will be configure:
			\t\t• POD Profile
			""")

		cmd = 'ansible-playbook methods/fabric_policies/executes/fabric_policies_pod_profile_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def accPolicies(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tAccess Policies will be configure:
			\t\t• Interface Policies
			\t\t• AAEP
			\t\t• MCP Global
			""")

		cmd = 'ansible-playbook methods/fabric_access_policies_1/executes/fabric_access_1_policy_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def pools(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tPools will be configure:
			\t\t• VLAN Pools
			""")

		cmd = 'ansible-playbook methods/fabric_access_policies_1/executes/fabric_access_1_pools_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm

	def domains(self):

		self.clear()
		print("""
			\t\t\tCISCO ACI AUTOMATION\n
			\t\tDomains will be configure:
			\t\t• Physical Domains
			\t\t• L3 Routed Domains
			""")

		cmd = 'ansible-playbook methods/fabric_access_policies_1/executes/fabric_access_1_domain_create_task.yml'

		
		confirm = input('Are you sure to push this configuration? [y/n]: ')
		if confirm == 'y' or confirm == 'Y':
			os.system(cmd)
			print()
			input("Press Enter to continue...")
			# self.run()
		elif confirm == 'n' or confirm == 'N':
			self.reset_input()
			self.run()
		else:
			confirm


	def xltoyml(self):

		self.clear()

		#Converting Excel to YAML				
		xlName = input('\nInput Excel File Name (.xlsx or .xls): ')

		xlPath = os.path.join(application_path, "input_data", xlName)
		varDir = os.path.join(application_path, "methods", "vars")
		print('\n######## Converting Excel File to YAML ########\n')
		xl2yaml_new.main(xlPath, varDir)
		print('\n######## Converting Complete ########\n')
		print()
		input("Press Enter to continue...")

	def clear_var(self):
		self.clear()
		base_folder = os.path.dirname(__file__)
		print(base_folder)
		var_dir = os.path.join(base_folder, "methods/vars")
		for f in os.listdir(var_dir):
			if ".yml" in f:
				print("Deleted File: " + f)
				os.remove(os.path.join(var_dir, f))
		print()
		input("Press Enter to continue...")
	
	def get_input(self):
		base_folder = os.path.dirname(__file__)
		get_input_file = os.path.join(base_folder, "methods/user_input/get_input.yml")
		try:
			apic_ip = str(input("Enter APIC or MSO IP address: ")).strip()
			apic_username_input = str(input("Enter APIC or MSO username: ")).strip()
			apic_password_input = str(getpass.getpass("Enter APIC or MSO password: ")).strip()
			# apic_password_input = str(input("Enter APIC or MSO password: ")).strip()
			xls_filename_input = str(input("Enter Input Excel file (without file extension): ")).strip()
			with open(get_input_file) as fp:
				data = yaml.safe_load(fp)
				# print(type(data))
				for elem in data:
					if elem["tasks"][0]["add_host"]:
						elem["tasks"][0]["add_host"]["name"] = apic_ip
						elem["tasks"][0]["add_host"]["apic_hostname"] = apic_ip
						elem["tasks"][0]["add_host"]["apic_password"] = apic_password_input
						elem["tasks"][0]["add_host"]["apic_username"] = apic_username_input
						elem["tasks"][0]["add_host"]["xls_filename"] = xls_filename_input
			with open(get_input_file, "w") as f:
				yaml.dump(data, f)
		except Exception as e:
			print(e)

	def reset_input(self):
		base_folder = os.path.dirname(__file__)
		get_input_file = os.path.join(base_folder, "methods/user_input/get_input.yml")
		try:
			with open(get_input_file) as fp:
				data = yaml.safe_load(fp)
				# print(type(data))
				for elem in data:
					if elem["tasks"][0]["add_host"]:
						elem["tasks"][0]["add_host"]["name"] = "apic_ip"
						elem["tasks"][0]["add_host"]["apic_hostname"] = "apic_ip"
						elem["tasks"][0]["add_host"]["apic_password"] = "apic_password_input"
						elem["tasks"][0]["add_host"]["apic_username"] = "apic_username_input"
						elem["tasks"][0]["add_host"]["xls_filename"] = "xls_filename_input"
			with open(get_input_file, "w") as f:
				yaml.dump(data, f)
		except Exception as e:
			print(e)

	def quit(self):
	
		while True:
			confirm = input('Are you sure to close this program? [y/n]: ')
			if confirm == 'y' or confirm == 'Y':
				print('\nProgram closed!\n')
				sys.exit(0)
				self.run()
			elif confirm == 'n' or confirm == 'N':
				self.run()
			else:
				confirm
	def clear(self):

		cmd = 'clear'
		os.system(cmd)

if __name__ == '__main__':
    try:
        Menu().run()
    except KeyboardInterrupt:
	    print('\nProgram closed!\n')