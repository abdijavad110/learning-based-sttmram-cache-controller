FILE = sobel.c

CC_ARM = arm-linux-gnueabi-gcc
CC_FLAGS_ARM = -static -DAMHM_APPROXIMATION -O0
ISA_FILE_ARM = ../../shared_lib/m5op_arm.S
LDFLAGS_ARM =

CC = gcc
CC_FLAGS = -static
LDFLAGS =

BINDIR = ../../bin

all: arm x86

arm:
	$(CC_ARM)  $(CC_FLAGS_ARM) $(FILE) -o $(BINDIR)/arm/sobel $(ISA_FILE_ARM) $(LDFLAGS_ARM)

x86:
	$(CC)  $(CC_FLAGS) $(FILE) -o $(BINDIR)/x86/sobel $(LDFLAGS)

clean:
	rm -rf $(BINDIR)/arm/sobel output*
	rm -rf $(BINDIR)/x86/sobel output*