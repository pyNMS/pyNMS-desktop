# NetDim (contact@netdim.fr)

import re
import tkinter as tk
from tkinter import ttk, messagebox
from objects.objects import *
from pythonic_tkinter.preconfigured_widgets import *
from miscellaneous.decorators import update_paths

class ObjectManagementWindow(FocusTopLevel):
    
    read_only = (
                 'source', 
                 'destination',
                 'path',
                 'flowSD',
                 'flowDS', 
                 'bgp_AS',
                 'AS'
                )
                
    property_list = {
    'interface': ('FE', 'GE', '10GE', '40GE', '100GE'),
    'site_type': ('Physical', 'Logical'),
    'controller_type': ('DefaultController', 'RemoteController'),
    'default_route': (None,),
    'nh_tk': (None,),
    'nh_ip': (None,),
    'ipS': (None,),
    'ipD': (None,),
    'dst_sntw': (None,)
    }
                
    @update_paths
    def __init__(self, obj, controller):
        super().__init__()

        self.title('Properties')
        # current node which properties are displayed
        self.current_obj = obj
        
        # current path of the object: computing a path is not saving it
        self.current_path = None
        
        # dictionnary containing all global properties entries / combobox
        self.dict_global_properties = {}
        
        # dictionnary containing all per-AS properties
        self.dict_perAS_properties = {}

        # create the property window
        
        # labelframe for global properties
        lf_global = Labelframe(self)
        lf_global.text = 'Global properties'
        lf_global.grid(1, 0, 1, 2)
        
        for index, property in enumerate(object_properties[obj.subtype]):
            
            # too much trouble handling interfaces here
            if property in ('interfaceS', 'interfaceD'):
                continue
            
            # creation of the label associated to the property
            text = prop_to_name[property]
            label = Label(self)
            label.text = text
            
            # value of the property: drop-down list or entry
            if property in self.property_list:
                pvalue = Combobox(self, width=12)
                pvalue['values'] = self.property_list[property]
            else:
                s = 'readonly' if property in self.read_only else 'normal'
                pvalue = Entry(self, width=15, state=s)
                
            self.dict_global_properties[property] = pvalue
                
            label.grid(index+1, 0, pady=1, in_=lf_global)
            pvalue.grid(index+1, 1, pady=1, in_=lf_global)
            
        if obj.subtype in perAS_properties:
            # labelframe for per-AS interface properties
            lf_perAS = Labelframe(self)
            lf_perAS.text = 'Per-AS properties'
            lf_perAS.grid(2, 0, 1, 2)
            self.dict_perAS_properties = {}
            
            # AS combobox
            self.AS_combobox = Combobox(self, width=30)
            self.AS_combobox.bind('<<ComboboxSelected>>', self.update_AS_properties)
            self.AS_combobox.grid(0, 0, 1, 2, in_=lf_perAS)
        
            for index, property in enumerate(perAS_properties[obj.subtype]):
                
                # creation of the label associated to the property
                text = prop_to_name[property]
                label = Label(self)
                label.text = text
                
                # value of the property
                pvalue = Entry(self, width=15)
                
                self.dict_perAS_properties[property] = pvalue
                    
                label.grid(index+1, 0, pady=1, in_=lf_perAS)
                pvalue.grid(index+1, 1, pady=1, in_=lf_perAS)
                                                                            
        button_save_obj = Button(self) 
        button_save_obj.text = 'Save'
        button_save_obj.command = self.save_obj
        button_save_obj.grid(0, 1)
        
        # update all properties with the selected object properties
        self.update()
        
        # when the window is closed, save all parameters (in case the user
        # made a change), then withdraw the window.
        self.protocol('WM_DELETE_WINDOW', lambda: self.save_and_destroy())
        
    def update_AS_properties(self, _):
        AS = self.AS_combobox.text
        for property, entry in self.dict_perAS_properties.items():
            entry.text = str(self.current_obj.AS_properties[AS][property])
        
    # this function converts the user-defined constraints to python objects.
    # it is used both when reading the user inputs, and when saving the 
    # route properties.
    def conv(self, property):
        value = self.dict_var[property].get().replace(' ','').split(',')
        if property == 'excluded_plinks':
            return {self.network.lf(name=t) for t in filter(None, value)}
        elif property == 'excluded_nodes':
            return {self.network.nf(name=n) for n in filter(None, value)}
        else:
            return [self.network.nf(name=n) for n in filter(None, value)]
    
    def get_user_input(self):
        name = self.dict_var['name'].get()
        source = self.network.nf(name=self.dict_var['source'].get())
        destination = self.network.nf(name=self.dict_var['destination'].get())
        return (
                name, 
                source, 
                destination, 
                self.conv('excluded_plinks'), 
                self.conv('excluded_nodes'), 
                self.conv('path_constraints')
                )
        
    def find_path(self):
        name, *parameters = self.get_user_input()
        nodes, plinks = self.network.A_star(*parameters)
        
        if plinks:
            self.view.unhighlight_all()
            self.current_path = plinks
            self.dict_var['path'].set(plinks)
            self.view.highlight_objects(*(nodes + plinks))
        else:
            self.view.unhighlight_all()
            # activate focus to prevent the messagebox from removing the window
            self.var_focus.set(1)
            self.change_focus()
            messagebox.showinfo('Warning', 'No path found')
        
    def save_obj(self):
        for property, property_widget in self.dict_global_properties.items():
            value = property_widget.text
            # convert 'None' to None if necessary
            value = None if value == 'None' else value              
            if property == 'path':
                setattr(self.current_obj, property, self.current_path)
            if property == 'sites':
                value = filter(None, set(re.sub(r'\s+', '', value).split(',')))
                value = set(map(self.site_network.convert_node, value))
                setattr(self.current_obj, property, value)
            elif property in self.property_list:
                if property in ('ipS', 'ipD', 'default_route'):
                    # convert the IP to a Object IP, if it isn't None
                    if value:
                        value = self.network.ip_to_oip[value]
                setattr(self.current_obj, property, value)
            else:
                if property not in self.read_only and 'interface' not in property:
                    if property in (
                                    'path_constraints', 
                                    'excluded_nodes', 
                                    'excluded_plinks'
                                    ): 
                        value = self.conv(property)
                    else:
                        value = self.network.prop_to_type[property](value)
                        if property == 'name':
                            name = getattr(self.current_obj, property)
                            id = self.network.name_to_id.pop(name)
                            self.network.name_to_id[value] = id
                    setattr(self.current_obj, property, value)
            # refresh the label if it was changed
            self.view.refresh_label(self.current_obj)
            # move the node on the canvas in case it's coordinates were updated
            if self.current_obj.class_type == 'node':
                self.view.move_node(self.current_obj)
             
        if hasattr(self.current_obj, 'AS_properties'):
            if self.current_obj.AS_properties:
                AS = self.AS_combobox.text
                for property, entry in self.dict_perAS_properties.items():
                    value = self.network.prop_to_type[property](entry.text)
                    self.current_obj(AS, property, value)
                
    def save_and_destroy(self):
        self.save_obj()
        #TODO send script no longer works when this window is simply destroyed...
        self.withdraw()
            
    def update(self):
        for property, property_widget in self.dict_global_properties.items():
            obj_prop = getattr(self.current_obj, property)
            if property == 'default_route':
                # in practice, the default route can also be set as an outgoing
                # interface, but the router has to do an ARP request for each
                # unknown destination IP address to fill the destination 
                # MAC field of the Ethernet frame, which may result in 
                # ARP table being overloaded: to be avoided in real-life and
                # forbidden here.
                attached_ints = (None,) + tuple(filter(None, 
                                    self.network.nh_ips(self.current_obj)))
                property_widget['values'] = attached_ints
                property_widget.text = obj_prop
            elif property == 'nh_tk':
                src_route = self.current_obj.source
                attached_ints = tuple(filter(None, (plink for _, plink 
                                in self.network.graph[src_route]['plink'])))
                property_widget['values'] = attached_ints
                property_widget.text = obj_prop
            elif property == 'dst_sntw':
                dest_node = self.current_obj.destination
                attached_ips = (None,) + tuple(filter(None, 
                            (plink.sntw for _, plink
                            in self.network.graph[dest_node]['plink']
                            ))) 
                property_widget['values'] = attached_ips
                property_widget.text = obj_prop
            elif property == 'ipS':
                src = self.current_obj.source
                attached_ips = (None,) + tuple(filter(None, 
                                    self.network.attached_ips(src)))
                property_widget['values'] = attached_ips
                property_widget.text = obj_prop
            elif property == 'nh_ip':
                nh_ips = (None,) + tuple(filter(None, 
                                    self.network.nh_ips(self.current_obj)))
                property_widget['values'] = nh_ips
                property_widget.text = obj_prop
            elif property == 'ipD':
                dest = self.current_obj.destination
                attached_ips = (None,) + tuple(filter(None, 
                                    self.network.attached_ips(dest)))
                property_widget['values'] = attached_ips
                property_widget.text = obj_prop
            elif property == 'AS':
                property_widget.text = ','.join(map(str, obj_prop.keys()))
            elif type(obj_prop) in (list, set):
                property_widget.text = ','.join(map(str, obj_prop))
            else:
                property_widget.text = str(obj_prop)
            # if there is a path, we set current_path in case the object is saved
            # without computing a new path
            if property == 'path':
                self.current_path = self.current_obj.path
                
        if self.current_obj.subtype in perAS_properties:
            self.AS_combobox['values'] = tuple(self.current_obj.AS_properties)
            has_AS = bool(self.current_obj.AS_properties)
            first_AS = next(iter(self.current_obj.AS_properties)) if has_AS else ''
            self.AS_combobox.text = first_AS
            for property, property_widget in self.dict_perAS_properties.items():
                if has_AS:
                    value = str(self.current_obj.AS_properties[first_AS][property])
                else:
                    value = ''
                property_widget.text = value
                
class PropertyChanger(FocusTopLevel):
                                 
    @update_paths
    def __init__(self, objects, type, controller):
        super().__init__()
        
        # list of properties
        self.property_list = Combobox(self, width=15)
        self.property_list['values'] = object_properties[type]
        self.property_list.current(0)        
                            
        self.entry_prop = Entry(self, width=15)
        button_OK = Button(self)
        button_OK.text = 'OK'
        button_OK.command = lambda: self.confirm(objects)
                                        
        self.property_list.grid(0, 0)
        self.entry_prop.grid(1, 0)
        button_OK.grid(2, 0)
        
    def confirm(self, objects):
        selected_property = self.property_list.text
        value = self.network.prop_to_type[selected_property](self.entry_prop.text)
        for object in objects:
            setattr(object, selected_property, value)
        self.destroy()
        