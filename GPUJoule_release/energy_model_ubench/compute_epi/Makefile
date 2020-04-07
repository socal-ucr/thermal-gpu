CC = nvcc -arch=sm_61
CFLAGS = -O0 -Xcompiler -O0 -Xptxas -O0 -I. -I./power_monitor


SRCS := $(wildcard *.cu)
BINS := $(patsubst %.cu,%,$(SRCS))
OBJS := $(patsubst %,%.o,$(BINS))
DEPS := power_monitor/ip_connection.h power_monitor/bricklet_voltage_current_v2.h
 

.PHONY: all


all: dir $(BINS)

%.o: %.cu $(DEPS)  
	$(CC) $(CFLAGS) -c $< -o $@

%: %.o $(patsubst %.h,%.o,$(DEPS))
	$(CC) $(CFLAGS) -o bin/$@.out $^ 
dir:
	mkdir -p bin


clean:
	$(RM) -rf bin/

rebuild: clean all

