from ansible.errors import AnsibleFilterError

class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'allowed_encap_split': allowed_encap_split,
            'in_allowed_encap': in_allowed_encap
        }

def allowed_encap_split(string):

    numeric_list = []
    # print(string)

    # If it is a range of numbers x-y
    if "-" in string:
        r = string.split("-")
        if len(r) == 2:
            for x in range(int(r[0]),int(r[1])+1):
                numeric_list.append(x)
        else:
            raise AnsibleFilterError("Allowed Encapsulation looks to be a range but has more than 2 values!")
            numeric_list = False

    # If it is a list of numbers separated by a comma
    elif "," in string:
        x = string.split(",")
        for val in x:
            numeric_list.append(int(val))

    # If it is a list of numbers separated by a space
    elif " " in string:
        x = string.split()
        for val in x:
            numeric_list.append(int(val))

    # If it is a valid single number
    elif int(string):
        x = int(string)
        numeric_list.append(x)

    else:
        raise AnsibleFilterError("Unknown delimiter in allowed encapsulation string. Valid delimeters are ',', ' ', or '-' for a range of valid values!")
        numeric_list = False

    return(numeric_list)

def in_allowed_encap(allowed_encap, search):
    try:#print(search + ' in ' + allowed_encap + ' is:' + str(int(search) in allowed_encap_split(allowed_encap)))
      contained = int(search) in allowed_encap_split(allowed_encap)
    except:
      raise AnsibleFilterError("Invalid Search Value used in in_allowed_encap Filter: '%s'" % search)
    return contained
