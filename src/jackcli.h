/* jackcli.h
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

'cyperus' is a JACK client for learning about software synthesis

Copyright 2015 murray foster */

#ifndef JACKCLI_H
#define JACKCLI_H


#include <stdio.h> //printf
#include <string.h> //memset
#include <stdlib.h> //exit(0);

#include <jack/jack.h>
#include "dsp.h"

/* ==== BEGIN to-be-defined cyperus params ==== */
extern int jackcli_channels_in;
extern int jackcli_channels_out;
/* ====  END  to-be-defined cyperus params ==== */

extern int jackcli_samplerate;
extern unsigned int jackcli_samplerate_pos;
extern int jackcli_buffer_size;

int jackcli_setup(char *jackcli_client_name, int bit_depth, int channels_in, int channels_out);
int jackcli_teardown();

#endif
