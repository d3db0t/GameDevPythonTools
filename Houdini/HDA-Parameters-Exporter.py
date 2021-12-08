'''
**DESCRIPTION**
Export all parameters in a houdini digital asset and save it to a text file.
'''

'''
**SETUP**
HDA->Type Properties->Parameters->CallbackScript->
Add "hou.pwd().hm().export_params(kwargs)"

HDA->Type Properties->Scripts->Add this code
'''

# Add types of parameters to exclude from the export
parameter_types_to_exclude = ["Button"]

def export_params(kwargs):
    ''' iterate on the HDA parameters and writes the output
    to a file'''
    parent_node       = kwargs['node']
    parent_node_parms = parent_node.parms()
    output            = []
    
    for parm in parent_node_parms:
        parm_data = get_parm_data(parm)
        if check_type(parm_data):
            output.append(parm_data)
    print(output)
    write_to_file(output)
    
        
def get_parm_data(parm):
    '''returns the [Name, Value, Type] of a parameter'''
    parm_name  = str(parm).split(' ')[1]
    parm_value = parm.eval()
    parm_type  = str(parm.parmTemplate().type()).split('.')[1]
    return [parm_name, parm_value, parm_type]
    
    
def check_type(t):
    '''checks for parameter types to output'''
    return t[2] not in parameter_types_to_exclude
    
    
def write_to_file(output):
    '''exports the output to a file'''
    filename = "hda_parameters.txt"
    path     = "C:/Users/Shady/Desktop/" + filename
    f        = open(path, 'w')
    f.write(str(output))
    f.close
    
    