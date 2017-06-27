# NetDim (contact@netdim.fr)

from pythonic_tkinter.preconfigured_widgets import *
from collections import OrderedDict
from miscellaneous.decorators import update_paths

class GraphAlgorithmWindow(FocusTopLevel):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title('Advanced graph options')

        ## Shortest path section
        
        # shortest path algorithms include:
        #   - shortest path with A* (Dijkstra)
        #   - shortest path with Bellman-Ford
        #   - shortest path with Floyd-Warshall
        #   - shortest path with Linear programming

        # label frame for shortest path algorithms
        lf_sp = Labelframe(self)
        lf_sp.text = 'Shortest path algorithms'

        # List of shortest path algorithms
        self.sp_list = Combobox(self, width=30)
        self.sp_list['values'] = (
                                  'Constrained A*',
                                  'Bellman-Ford algorithm', 
                                  'Floyd-Warshall algorithm',
                                  'Linear programming'
                                  )
        self.sp_list.current(0)
                                
        sp_src_label = Label(self)
        sp_src_label.text = 'Source :'
        self.sp_src_entry = Entry(self)
        
        sp_dest_label = Label(self)
        sp_dest_label.text = 'Destination :'
        self.sp_dest_entry = Entry(self)
        
        bt_sp = Button(self)
        bt_sp.text = 'Compute path'
        bt_sp.command = self.compute_sp
        
        lf_sp.grid(1, 0, 1, 2)
        self.sp_list.grid(0, 0, 1, 2, in_=lf_sp)
        sp_src_label.grid(1, 0, in_=lf_sp)
        self.sp_src_entry.grid(1, 1, in_=lf_sp)
        sp_dest_label.grid(2, 0, in_=lf_sp)
        self.sp_dest_entry.grid(2, 1, in_=lf_sp)
        bt_sp.grid(3, 0, 1, 2, in_=lf_sp)
        
        ## Maximum flow section
        
        # maximum flow algorithms include:
        #   - maximum flow with Ford-Fulkerson
        #   - maximum flow with Edmond-Karps
        #   - maximum flow with Dinic
        #   - maximum flow with Linear programming
        
        # label frame for maximum flow algorithms
        lf_mflow = Labelframe(self)
        lf_mflow.text = 'Maximum flow algorithms'
        
        # List of flow path algorithms
        self.mflow_list = Combobox(self, width=30)
        self.mflow_list['values'] = (
                                    'Ford-Fulkerson',
                                    'Edmond-Karps', 
                                    'Dinic', 
                                    'Linear programming'
                                    )
        self.mflow_list.current(0)
        self.mflow_list.bind('<<ComboboxSelected>>', self.readonly)
                                        
        mflow_src_label = Label(self)
        mflow_src_label.text = 'Source :'
        self.mflow_src_entry = Entry(self)
        
        mflow_dest_label = Label(self)
        mflow_dest_label.text = 'Destination :'
        self.mflow_dest_entry = Entry(self)
        
        bt_mflow = Button(self)
        bt_mflow.text = 'Compute flow'
        bt_mflow.command = self.compute_mflow
        
        lf_mflow.grid(1, 2, 1, 2)
        self.mflow_list.grid(0, 0, 1, 2, in_=lf_mflow)
        mflow_src_label.grid(1, 0, in_=lf_mflow)
        self.mflow_src_entry.grid(1, 1, in_=lf_mflow)
        mflow_dest_label.grid(2, 0, in_=lf_mflow)
        self.mflow_dest_entry.grid(2, 1, in_=lf_mflow)
        bt_mflow.grid(4, 0, 1, 2, in_=lf_mflow)
        
        ## K link-disjoint shortest paths section
        
        # K link-disjoint shortest paths algorithms include:
        #   - constrained A*
        #   - Bhandari algorithm
        #   - Suurbale algorithm
        #   - Linear programming

        # label frame for shortest pair algorithms
        lf_spair = Labelframe(self) 
        lf_spair.text = 'K link-disjoint shortest paths algorithms'

        # List of shortest path algorithms
        self.spair_list = Combobox(self, width=30)
        self.spair_list['values'] = (
                                    'Constrained A*', 
                                    'Bhandari algorithm', 
                                    'Suurbale algorithm', 
                                    'Linear programming'
                                    )

        self.spair_list.current(0)
                                
        spair_src_label = Label(self)
        spair_src_label.text = 'Source :'
        self.spair_src_entry = Entry(self)
        
        spair_dest_label = Label(self)
        spair_dest_label.text = 'Destination :'
        self.spair_dest_entry = Entry(self)

        nb_paths_label = Label(self)
        nb_paths_label.text = 'Number of paths :'
        self.nb_paths_entry = Entry(self)

        bt_spair = Button(self)
        bt_spair.text = 'Compute paths'
        bt_spair.command = self.compute_spair
        
        lf_spair.grid(2, 0, 1, 2)
        self.spair_list.grid(0, 0, 1, 2, in_=lf_spair)
        spair_src_label.grid(1, 0, in_=lf_spair)
        self.spair_src_entry.grid(1, 1, in_=lf_spair)
        spair_dest_label.grid(2, 0, in_=lf_spair)
        self.spair_dest_entry.grid(2, 1, in_=lf_spair)
        nb_paths_label.grid(3, 0, in_=lf_spair)
        self.nb_paths_entry.grid(3, 1, in_=lf_spair)
        bt_spair.grid(4, 0, 1, 2, in_=lf_spair)
        
        ## Minimum-cost flow section
        
        # minimum-cost flow algorithms include:
        #   - minimum-cost flow with Linear programming
        #   - minimum-cost flow with Klein (cycle-cancelling algorithm)
        
        # label frame for maximum flow algorithms
        lf_mcflow = Labelframe(self)
        lf_mcflow.text = 'Minimum-cost flow algorithms'
        
        # List of flow path algorithms
        self.mcflow_list = Combobox(self, width=30)
        self.mcflow_list['values'] = ('Linear programming', 'Klein')

        self.mcflow_list.current(0)
        self.mcflow_list.bind('<<ComboboxSelected>>', self.readonly)
                                        
        mcflow_src_label = Label(self)
        mcflow_src_label.text = 'Source :'
        self.mcflow_src_entry = Entry(self)
        
        mcflow_dest_label = Label(self)
        mcflow_dest_label.text = 'Destination :'
        self.mcflow_dest_entry = Entry(self)

        bt_mcflow = Button(self)
        bt_mcflow.text = 'Compute cost'
        bt_mcflow.command = self.compute_mcflow

        flow_label = Label(self)
        flow_label.text = 'Flow :'
        self.flow_entry = Entry(self)

        lf_mcflow.grid(2, 2, 1, 2)
        self.mcflow_list.grid(0, 0, 1, 2, in_=lf_mcflow)
        mcflow_src_label.grid(1, 0, in_=lf_mcflow)
        self.mcflow_src_entry.grid(1, 1, in_=lf_mcflow)
        mcflow_dest_label.grid(2, 0, in_=lf_mcflow)
        self.mcflow_dest_entry.grid(2, 1, in_=lf_mcflow)
        bt_mcflow.grid(4, 0, 1, 2, in_=lf_mcflow)
        flow_label.grid(3, 0, in_=lf_mcflow)
        self.flow_entry.grid(3, 1, in_=lf_mcflow)

        # hide the window when closed
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
        self.withdraw()
        
    def readonly(self, event):
        if self.flow_list.text[-4:-1] == 'MCF':
            self.max_flow_entry.config(state=tk.NORMAL)
        else:
            self.max_flow_entry.config(state='readonly')
                 
    @update_paths
    def compute_sp(self):
        source = self.network.nf(name=self.sp_src_entry.text)
        destination = self.network.nf(name=self.sp_dest_entry.text)
        algorithm = {
                    'Constrained A*': self.network.A_star,
                    'Bellman-Ford algorithm': self.network.bellman_ford,
                    'Floyd-Warshall algorithm': self.network.floyd_warshall,
                    'Linear programming': self.network.LP_SP_formulation
                    }[self.sp_list.text]
        nodes, plinks = algorithm(source, destination)
        self.view.highlight_objects(*(nodes + plinks))
        
    @update_paths
    def compute_mflow(self):
        source = self.network.nf(name=self.mflow_src_entry.text)
        destination = self.network.nf(name=self.mflow_dest_entry.text)
        algorithm = {
                    'Ford-Fulkerson': self.network.ford_fulkerson,
                    'Edmond-Karps': self.network.edmonds_karp,
                    'Dinic': self.network.dinic,
                    'Linear programming': self.network.LP_MF_formulation
                    }[self.mflow_list.text]
        flow = algorithm(source, destination)   
        print(flow)
        
    @update_paths
    def compute_spair(self):
        source = self.network.nf(name=self.spair_src_entry.text)
        destination = self.network.nf(name=self.spair_dest_entry.text)
        algorithm = {
                    'Constrained A*': self.network.A_star_shortest_pair,
                    'Bhandari algorithm': self.network.bhandari,
                    'Suurbale algorithm': self.network.suurbale,
                    'Linear programming': lambda: 'to repair'
                    }[self.spair_list.text]
        nodes, plinks = algorithm(source, destination)
        self.view.highlight_objects(*(nodes + plinks))
        
    @update_paths
    def compute_mcflow(self):
        source = self.network.nf(name=self.mcflow_src_entry.text)
        destination = self.network.nf(name=self.mcflow_dest_entry.text)
        flow = self.flow_entry.text
        algorithm = {
                    'Linear programming': self.network.LP_MCF_formulation,
                    'Klein': lambda: 'to be implemented'
                    }[self.mcflow_list.text]
        cost = algorithm(source, destination, flow)   
        print(cost)