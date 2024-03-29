/*
 * cyperus_lowpass_module.h
 *
 * Code generation for model "cyperus_lowpass_module".
 *
 * Model version              : 1.2
 * Simulink Coder version : 9.1 (R2019a) 23-Nov-2018
 * C source code generated on : Mon Apr 13 12:16:16 2020
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objective: Execution efficiency
 * Validation result: Not run
 */

#ifndef OPS_MODULES_OSCILLATOR_CLOCK_H
#define OPS_MODULES_OSCILLATOR_CLOCK_H

#include <stdio.h> //printf
#include <string.h> //memset
#include <stdlib.h> //exit(0)

#include "../../../dsp.h"
#include "../../../dsp_ops.h"
#include "../../../dsp_types.h"
#include "../../../dsp_math.h"
#include "../../../osc.h"
#include "../../../osc_handlers.h"

#include "../../../jackcli.h"

int
dsp_create_oscillator_clock(struct dsp_bus *target_bus,
                           float frequency,
                           float amplitude);
void
dsp_oscillator_clock(struct dsp_operation *oscillator_clock,
			    int jack_samplerate);
void
dsp_edit_oscillator_clock(struct dsp_module *oscillator_clock,
                         float frequency,
                         float amplitude);

void
dsp_osc_listener_oscillator_clock(struct dsp_operation *oscillator_clock,
                                 int jack_samplerate);
#endif
