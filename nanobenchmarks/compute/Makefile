CC = /home/ajaha004/apps/cuda10/cuda/bin/nvcc 
CFLAGS = -cudart shared -O0 -Xptxas #-O0 -Xcompiler -O0 -Xptxas -O0

SRCS   := $(wildcard *.cu)
BINS   := $(patsubst %.cu,%,$(SRCS))
OBJS   := $(patsubst %,%.o,$(BINS))

.PHONY: all

%: %.cu 
	$(CC) $(CFLAGS) -c $< -o $@

all: $(BINS)

clean:
	$(RM) $(BINS) $(SRCS)

rebuild: clean all
