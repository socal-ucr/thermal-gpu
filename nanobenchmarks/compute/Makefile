CC = /home/ajaha004/apps/cuda40/cuda/bin/nvcc -arch=sm_20
CFLAGS = -O0 -Xcompiler -O0 -Xptxas -O0

SRCS   := $(wildcard *.cu)
BINS   := $(patsubst %.cu,%,$(SRCS))
OBJS   := $(patsubst %,%.o,$(BINS))

.PHONY: all

%.o: %.cu 
	$(CC) $(CFLAGS) -c $< -o $@
%: %.o 
	$(CC) $(CFLAGS) -o $@ $^ 
all: $(BINS)

clean:
	$(RM) $(BINS) $(SRCS)

rebuild: clean all
