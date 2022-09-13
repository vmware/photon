CC := gcc
RM := /bin/rm
CFLAGS := -O2 -std=gnu99 -Wall -Wextra

SRC_DIR := .
SRCS := $(wildcard $(SRC_DIR)/*.c)
HDRS := $(wildcard $(SRC_DIR)/*.h)
TARGET_EXEC := contain_unpriv

.PHONY: clean

all: $(TARGET_EXEC)

$(TARGET_EXEC): $(SRCS) $(HDRS)
	@$(CC) $(CFLAGS) -o $@ $(SRCS)

install: all
ifneq ($(shell id -u), 0)
	@echo "You must be root to perform this action."
else
	@cp ./$(TARGET_EXEC) ../../bin/
	@install -o root -g root -m 4755 ../../bin/$(TARGET_EXEC) ../../bin/contain
endif

clean:
	@$(RM) -f ../../bin/$(TARGET_EXEC) ./$(TARGET_EXEC)
