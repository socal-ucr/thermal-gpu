/***************************************************************************\
  |*                                                                           *|
  |*      Copyright 2010-2016 NVIDIA Corporation.  All rights reserved.        *|
  |*                                                                           *|
  |*   NOTICE TO USER:                                                         *|
  |*                                                                           *|
  |*   This source code is subject to NVIDIA ownership rights under U.S.       *|
  |*   and international Copyright laws.  Users and possessors of this         *|
  |*   source code are hereby granted a nonexclusive, royalty-free             *|
  |*   license to use this code in individual and commercial software.         *|
  |*                                                                           *|
  |*   NVIDIA MAKES NO REPRESENTATION ABOUT THE SUITABILITY OF THIS SOURCE     *|
  |*   CODE FOR ANY PURPOSE. IT IS PROVIDED "AS IS" WITHOUT EXPRESS OR         *|
  |*   IMPLIED WARRANTY OF ANY KIND. NVIDIA DISCLAIMS ALL WARRANTIES WITH      *|
  |*   REGARD TO THIS SOURCE CODE, INCLUDING ALL IMPLIED WARRANTIES OF         *|
  |*   MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR          *|
  |*   PURPOSE. IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY SPECIAL,            *|
  |*   INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES          *|
  |*   WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN      *|
  |*   AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING     *|
  |*   OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOURCE      *|
  |*   CODE.                                                                   *|
  |*                                                                           *|
  |*   U.S. Government End Users. This source code is a "commercial item"      *|
  |*   as that term is defined at 48 C.F.R. 2.101 (OCT 1995), consisting       *|
  |*   of "commercial computer  software" and "commercial computer software    *|
  |*   documentation" as such terms are used in 48 C.F.R. 12.212 (SEPT 1995)   *|
  |*   and is provided to the U.S. Government only as a commercial end item.   *|
  |*   Consistent with 48 C.F.R.12.212 and 48 C.F.R. 227.7202-1 through        *|
  |*   227.7202-4 (JUNE 1995), all U.S. Government End Users acquire the       *|
  |*   source code with only those rights set forth herein.                    *|
  |*                                                                           *|
  |*   Any use of this source code in individual and commercial software must  *| 
  |*   include, in the user documentation and internal comments to the code,   *|
  |*   the above Disclaimer and U.S. Government End Users Notice.              *|
  |*                                                                           *|
  |*                                                                           *|
  \***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <nvml.h>
#include <signal.h>
#include <pthread.h>
#include "ip_connection.h"
#include "bricklet_voltage_current_v2.h"

#define HOST "localhost"
#define PORT 4223
#define UID12VPS "HKZ" // Change XYZ to the UID of your Voltage/Current Bricklet 2.0
#define UID12VMB "HM3" // Change XYZ to the UID of your Voltage/Current Bricklet 2.0
#define UID3VMB "HL3" // Change XYZ to the UID of your Voltage/Current Bricklet 2.0
VoltageCurrentV2 vc[3];
IPConnection ipcon;
volatile sig_atomic_t stopFlag = 0;
pthread_t powerMonitor_t;
int32_t avgPower= 0;
void* monitor_power(void*)
{
    int32_t numSamples = 0;
    while(!stopFlag) { 
        int32_t sample_power = 0;
        for(int i = 0; i < 3; i++)
        {
            int32_t sensor_power;
            voltage_current_v2_get_power(&vc[i], &sensor_power);
            sample_power += sensor_power;
        }
        avgPower = avgPower + ((sample_power - avgPower) / (numSamples + 1));
        numSamples++;
    }
    return NULL; 
}

void start_power_monitor(int ms) 
{
    // Create IP connection
    ipcon_create(&ipcon);

    // Create device object
    voltage_current_v2_create(&vc[0], UID12VPS, &ipcon);
    voltage_current_v2_create(&vc[1], UID12VMB, &ipcon);
    voltage_current_v2_create(&vc[2], UID3VMB, &ipcon);
    // Connect to brickd
    if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
        fprintf(stderr, "Could not connect\n");
        return;
    }

    pthread_create(&powerMonitor_t,NULL,monitor_power,NULL);

}

void end_power_monitor()
{
    stopFlag = 1;
    pthread_join(powerMonitor_t,NULL);
    voltage_current_v2_destroy(&vc[0]);
    voltage_current_v2_destroy(&vc[1]);
    voltage_current_v2_destroy(&vc[2]);
    ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally

    printf("%d\n",avgPower);
}

