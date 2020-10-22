TARGET=motion
include ../shared/Makefile.shared

$(TARGET): $(TARGET).o
	$(CC) $(TARGET).cpp -lstdc++ -lm $(SNIPER_LDFLAGS) -o $(TARGET)

run_$(TARGET):
	$(MAKE) -C ../../
	../../run-sniper -c base.cfg --cache-only -- ./motion frames/00227.bmp frames/00228.bmp outputs/output.bmp

CLEAN_EXTRA=output.bmp
