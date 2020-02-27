CC = /home/ajaha004/apps/cuda10/cuda/bin/nvcc -arch=sm_61
CFLAGS = -cudart shared -O0 -Xptxas -O0 -Xcompiler -O0

SRCS   := $(wildcard *.cu)
BINS   := $(patsubst %.cu,%,$(SRCS))
OBJS   := $(patsubst %,%.o,$(BINS))

.PHONY: all

%: %.cu 
	$(CC) $(CFLAGS) $< -o $@

all: $(BINS)

clean:
	$(RM) $(BINS) $(SRCS)

rebuild: clean all
