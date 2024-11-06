#! /usr/bin/python3

import argparse
import json

from pycyperus import pycyperus

class LiteGraphSerialized:
    def __init__(self, path, cyperus_api):
        self.path = path
        self.graph = None
        self.cyperus_api = cyperus_api

    def load_graph(self):
        with open(self.path, 'r') as fp:
            self.graph = json.loads(fp.read())

    def write_indented_graph(self):
        serialized_graph_path_indented = '/home/mfoster/Dev/cyperus/presets/four_sines_indented.json'
        with open(serialized_graph_path_indented, 'w') as fp:
            fp.write(json.dumps(self.graph, indent=4))

    def update_mains(self):
        mains_dict = self.cyperus_api.list_main()
        for idx, node in enumerate(self.graph['nodes']):
            match node['type']:
                case 'cyperus/main/inputs':
                    for idx_id, id in enumerate(
                            self.graph['nodes'][idx]['properties']['ids']
                    ):
                        self.graph['nodes'][idx]['properties']['ids'][idx_id] = mains_dict['in'][idx_id]
                case 'cyperus/main/outputs':
                    for idx_id, id in enumerate(
                            self.graph['nodes'][idx]['properties']['ids']
                    ):
                        self.graph['nodes'][idx]['properties']['ids'][idx_id] = mains_dict['out'][idx_id]

    def _peek_subgraph_busports(self, subgraph):
        ins = []
        outs = []
        for node in subgraph['nodes']:
            match node['type']:
                case 'cyperus/bus/input':
                    ins.append(node)
                case 'cyperus/bus/output':
                    outs.append(node)
        return {
            'ins': ins,
            'outs': outs
        }

    def _update_module_parameter_ids(self, node, new_module_ports):
        for port_type in ('in', 'out'):
            for module_port in new_module_ports[port_type]:
                for node_port in node[f'{port_type}puts']:
                    if module_port['name'] == node_port['name']:
                        node_port['id'] = module_port['id']
    
    def _recursively_update_subgraph(self, subgraph, subgraph_bus_id=''):
        for idx_node, node in enumerate(subgraph['nodes']):
            match node['type']:
                case 'cyperus/main/inputs':
                    pass
                case 'cyperus/main/outputs':
                    pass
                case 'cyperus/bus/add':
                    busports = self._peek_subgraph_busports(node['subgraph'])

                    busport_ins = []
                    busport_outs = []
                    for busport in busports['ins']:
                        busport_ins.append(busport['properties']['name'])
                    for busport in busports['outs']:
                        busport_outs.append(busport['properties']['name'])
                        
                    busport_in_names = ','.join(busport_ins)
                    busport_out_names = ','.join(busport_outs)
                    
                    new_bus_id = self.cyperus_api.add_bus(subgraph_bus_id,
                                                          node['title'],
                                                          busport_in_names,
                                                          busport_out_names)

                    new_bus_ports = self.cyperus_api.list_bus_port(new_bus_id)

                    node['properties']['id'] = new_bus_id
                    node['subgraph']['bus_id'] = new_bus_id
                    node['properties']['bus_input_ids'] = [bus_port['id'] for bus_port in new_bus_ports['in']]
                    node['properties']['bus_output_ids'] = [bus_port['id'] for bus_port in new_bus_ports['out']]
                    for idx, busport in enumerate(busports['ins']):
                        busport['properties']['id'] = new_bus_ports['in'][idx]['id']                        
                    for idx, busport in enumerate(busports['outs']):
                        busport['properties']['id'] = new_bus_ports['out'][idx]['id']

                    subgraph['nodes'][idx_node] = node
                    
                    self._recursively_update_subgraph(node['subgraph'],
                                                      node['properties']['id'])
                case 'cyperus/bus/input':
                    pass
                case 'cyperus/bus/output':
                    pass
                case _:
                    #
                    # add current cyperus module
                    #
                    match node['type']:
                        case 'oscillator/sine':
                            frequency = float(node['properties']['frequency'])
                            amplitude = float(node['properties']['amplitude'])
                            phase = float(node['properties']['phase'])
                            new_module_id = self.cyperus_api.add_modules_oscillator_sine(
                                subgraph_bus_id,
                                frequency,
                                amplitude,
                                phase
                            )
                        case 'envelope/follower':
                            attack = float(node['properties']['attack'])
                            decay = float(node['properties']['decay'])
                            scale = float(node['properties']['scale'])
                            new_module_id = self.cyperus_api.add_modules_envelope_follower(
                                subgraph_bus_id,
                                attack,
                                decay,
                                scale
                            )
                        case _:
                            print('UNSUPPORTED MODULE:')
                            print('node', node['type'])
                            continue
                    new_module_ports = self.cyperus_api.list_module_port(
                        new_module_id
                    )
                    node['properties']['id'] = new_module_id
                    self._update_module_parameter_ids(node, new_module_ports)

        for link in subgraph['links']:
            link_dict = {
                'id': link[0],
                'origin_id': link[1],
                'origin_slot': link[2],
                'target_id': link[3],
                'target_slot': link[4],
                'type': link[5],
                'cyperus_id': link[6]
            }
            
            origin_node = None
            target_node = None
            origin_slot = link_dict['origin_slot']
            target_slot = link_dict['target_slot']
            origin_port_id = None
            target_port_id = None
            for node in subgraph['nodes']:
                if node['id'] == link_dict['origin_id']:
                    origin_node = node
                    match node['type']:
                        case 'cyperus/main/inputs':
                            origin_port_id = node['properties']['ids'][origin_slot]
                        case 'cyperus/bus/add':
                            origin_port_id = node['properties']['bus_output_ids'][origin_slot]
                        case 'cyperus/bus/input':
                            origin_port_id = node['properties']['id']
                        case _:
                            origin_port_id = node['outputs'][origin_slot]['id']
                if node['id'] == link_dict['target_id']:
                    target_node = node
                    match node['type']:
                        case 'cyperus/main/outputs':
                            target_port_id = node['properties']['ids'][target_slot]
                        case 'cyperus/bus/add':
                            target_port_id = node['properties']['bus_input_ids'][target_slot]
                        case 'cyperus/bus/output':
                            target_port_id = node['properties']['id']
                        case _:
                            target_port_id = node['inputs'][target_slot]['id']

            new_connection_id = self.cyperus_api.add_connection(origin_port_id,
                                                                target_port_id)
            link[6] = new_connection_id
            
    def update_graph(self):
        self._recursively_update_subgraph(self.graph)
        
def main():
    serialized_graph_path = '/home/mfoster/Dev/cyperus/presets/four_sines.json'

    # for node in serialized_graph['nodes']:
    #     if node['type'] == 'cyperus/bus/add':
    #         subgraph = node['subgraph']
    #         subgraph_links = subgraph['links']

    cyperus_api = pycyperus.Api(7800, 7500)
    lg = LiteGraphSerialized(serialized_graph_path, cyperus_api)
    lg.load_graph()
    lg.update_mains()
    lg.update_graph()    
    lg.write_indented_graph()
    cyperus_api.close()

if __name__ == '__main__':
    main()
