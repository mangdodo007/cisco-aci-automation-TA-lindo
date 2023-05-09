from __future__ import absolute_import, division, print_function
from collections import OrderedDict

import xlrd,time,os,yaml,re,sys,argparse



if sys.version_info[0] >= 3:
    unicode = str
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

# Representer for OrderedDict
def dict_representer(dumper, data):
    return dumper.represent_mapping( u'tag:yaml.org,2002:map', data.items(), flow_style=False )

#Representer for Unicode Values (Excel data is in unicode)
def unicode_representer(dumper, uni):
    node = yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)
    return node

def short_name(full_tab_name):

    ftn = full_tab_name.lower()
    # 04/11/19 - refactor function to work better
    # Set the short name or prefix of the output YAML file
    # Set the proper script name so that the actual execution command can be printed out
    if "fabric_discovery" in ftn:
        short_name = "fabric_discovery"
    elif "system_setting" in ftn:
        short_name = "system_setting"
    elif "admin" in ftn:
        short_name = "admin"          
    elif "fabric_policies" in ftn:
        short_name = "fabric_policies"
    elif "fabric_access_policies" in ftn:
        short_name = "fabric_access_policies" 
    elif "tenant_1" in ftn:
        short_name = "tenant_1"    
    elif "tenant_2" in ftn:
        short_name = "tenant_2"   
    elif "tenant_3" in ftn:
        short_name = "tenant_3"           
    elif "virtual_networking" in ftn:
        short_name = "virtual_networking" 
    elif "service_graph" in ftn:
        short_name = "service_graph" 
    elif "fabric_extension_1" in ftn:
        short_name = "fabric_extension_1" 
    elif "fabric_extension_2" in ftn:
        short_name = "fabric_extension_2" 
    else:
        short_name = ftn

    return short_name

def yaml_from_excel(excel_file, outpath):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    msg = "Excel to YAML {}\n".format(time.ctime())
    print(msg)

    for worksheet_name in all_worksheets:
        if "sec" in worksheet_name.lower(): 
            worksheet = workbook.sheet_by_name(worksheet_name)
            if worksheet.nrows == 0:
                continue
            
            top_level_list = []
            top_level_dict = OrderedDict()  #Keep original order also in yaml, therefore use OrderedDict
            temp_dict = OrderedDict()
            interim_dict = OrderedDict() #Keep original order also in yaml, therefore use OrderedDict
            temp_list = []
            after_start = False
            keys = []

            #for row in worksheet.row_s
            for rownum in range(worksheet.nrows):
                row=worksheet.row_values(rownum)
                for idx,value in enumerate(row):
                    if (type(value) == float or type(value) == int):
                        row[idx] = str(int(value))
                    elif (type(value) == str or type(value) == unicode):
                        row[idx] = value.strip()
                # If not an empty row
                if worksheet.row(rownum):
                    if row[0] and not re.search('^#', row[0].strip()):
                        if row[0] == "key_start":

                            top_level_key = row[1].strip()
                            top_level_dict[top_level_key] = {}

                            row.remove(top_level_key)
                            row.remove('key_start')
                            keys = [x for x in row if x]
                            after_start = True
                            continue
                        if after_start:
                            after_start = False
                            continue
                        if row[0] == "key_end":

                            interim_dict[top_level_key] = temp_list

                            top_level_list.append(interim_dict.copy())

                            # Reset variables
                            keys = ""
                            temp_dict = OrderedDict() #Keep original order also in yaml, therefore use OrderedDict
                            temp_list = []
                            interim_dict = OrderedDict() #Keep original order also in yaml, therefore use OrderedDict
                            continue
                        for i in range(0, len(keys)):
                            if type(row[i]) == float:
                                temp_dict[keys[i].strip()] = int(row[i])
                            elif (type(row[i]) == str or type(row[i]) == unicode):
                                temp_dict[keys[i].strip()] = row[i].strip()
                            else:
                                temp_dict[keys[i].strip()] = row[i]
                        temp_list.append(temp_dict.copy())

            # print json.dumps(top_level_list, indent = 4)
            print("Total number of policy sections generated in file: " + str(len(top_level_list)))
            for line in top_level_list:
                line.keys()

            shortname = short_name(worksheet_name)
            _suffix = os.path.basename(excel_file)
            filename, extension = os.path.splitext(_suffix)
            yaml_filename = os.path.join(outpath,'{}_{}.yml'.format(shortname, filename))
            with open(yaml_filename, 'w') as yamlfile:
                #Use regular dump with custom representers for unicode and OrderedDict
                for item in top_level_list:
                    yaml.dump(item, yamlfile, encoding='utf-8', allow_unicode=True, default_flow_style=False)
            print("YAML Output has been saved to the file: " + yaml_filename)


def main(excel_file, output_path):
    #setup representers for OrderedDict and unicode values.
    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_representer(unicode, unicode_representer)

    yaml_from_excel(excel_file, output_path)
    
    
if __name__ == '__main__':
    main()
