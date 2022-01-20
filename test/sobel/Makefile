TARGET=sobel
include ../shared/Makefile.shared

$(TARGET): $(TARGET).o
	$(CC) $(TARGET).c -lstdc++ -lm $(SNIPER_LDFLAGS) -o $(TARGET)

run_$(TARGET):
	$(MAKE) -C ../../
	../../run-sniper -c base.cfg --cache-only -- ./$(TARGET) frames/00227.pgm frames/out.pgm

#CLEAN_EXTRA=output.bmp output*
