
''' cyperus.py
This file is a part of 'cyperus'
This program is free software: you can redistribute it and/or modify
hit under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'cyperus' is a realtime music system

Copyright 2024 murray foster '''

import argparse
import os
import signal
import subprocess

CONFIG_DIRECTORY = "~/.local/share/cyperus"


class Cyperus:
    def __init__(self, config_directory):
        self.config_directory = config_directory
        self.config_directory_presets = f"{self.config_directory}/presets"
        self.config_directory_preset_active = f"{self.config_directory}/preset_active"
        self._setup_directories()

    _child_processes = {
        'cyperus-server': {
            'pid': None
        },
        'websocket-relay': {
            'pid': None
        },
        'presets-loader': {
            'pid': None
        }
    }

    def _setup_directories(self):
        os.makedirs(os.path.expanduser(self.config_directory), exist_ok=True)
        os.makedirs(os.path.expanduser(self.config_directory_presets), exist_ok=True)
        os.makedirs(os.path.expanduser(self.config_directory_preset_active), exist_ok=True)
    
    def _setup_cyperus_server(self,
                             server_input_channels=4,
                             server_output_channels=4,
                             server_bitdepth=24,
                             server_recv_port=7500,
                             server_send_port=7400,
                             server_period=256):
        
        proc = subprocess.Popen(
            [
                'cyperus-server/build/cyperus-server',
                '-i', str(server_input_channels),
                '-o', str(server_output_channels),
                '-bd', str(server_bitdepth),
                '-rp', str(server_recv_port),
                '-sp', str(server_send_port),
                '-p', str(server_period)
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.child_processes['cyperus-server']['pid'] = proc.pid
        (output, error) = proc.communicate()
        if error:
            print('error:', error)
            print('output:', output)
            
    def _setup_websocket_relay(self):
        pass

    def _setup_presets_loader(self):
        pass
    
    def run(self,
            server_input_channels=4,
            server_output_channels=4,
            server_bitdepth=24,
            server_recv_port=7500,
            server_send_port=7400,
            server_period=256,
            relay_recv_port=7400,
            relay_send_port=7500,
            presets_recv_port=7600,
            presets_send_port=7500):
        self._setup_directories()
        self._setup_cyperus_server(server_input_channels,
                                   server_output_channels,
                                   server_bitdepth,
                                   server_recv_port,
                                   server_send_port,
                                   server_period)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='cyperus')

    cyperus_server_group = parser.add_argument_group('server', 'cyperus-server arguments')
    cyperus_server_group.add_argument('-i', '--input-channels', type=int, help='input audio channels, default: 4', default=4)
    cyperus_server_group.add_argument('-o', '--output-channels', type=int, help='output audio channels, default: 4', default=4)
    cyperus_server_group.add_argument('-b', '--bitdepth', type=int, help='audio bitdepth. default: 24', default=24)
    cyperus_server_group.add_argument('-r', '--recv-port', type=int, help='osc receiving port. default: 7500', default=7500)
    cyperus_server_group.add_argument('-s', '--send-port', type=int, help='osc sending port. default: 7400', default=7400)
    cyperus_server_group.add_argument('-p', '--period', type=int, help='frames per period. default: 256', default=256)
    
    websocket_relay_group = parser.add_argument_group('relay', 'websocket relay arguments')
    websocket_relay_group.add_argument('-rr', '--relay-recv-port', type=int, help='osc receiving port. default: 7400', default=7400)
    websocket_relay_group.add_argument('-rs', '--relay-send-port', type=int, help='osc sending port. default: 7500', default=7500)

    preset_loader_group = parser.add_argument_group('presets', 'presets loader arguments')
    preset_loader_group.add_argument('-pr', '--presets-recv-port', type=int, help='osc receiving port. default: 7600', default=7600)
    preset_loader_group.add_argument('-ps', '--presets-send-port', type=int, help='osc sending port. default 7500', default=7500)
    
    args = parser.parse_args()

    cyperus = Cyperus(CONFIG_DIRECTORY)
    cyperus.run(server_input_channels=args.input_channels,
                server_output_channels=args.output_channels,
                server_bitdepth=args.bitdepth,
                server_recv_port=args.recv_port,
                server_send_port=args.send_port,
                server_period=args.period,
                relay_recv_port=args.relay_recv_port,
                relay_send_port=args.relay_send_port,
                presets_recv_port=args.presets_recv_port,
                presets_send_port=args.presets_send_port)