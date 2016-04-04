.PHONY: all clean

all: clean1 copy

copy:./src/lexer.py
	@cp -r ./src/ ./bin/
	@chmod +x ./bin/irspit
	@echo "Everything is cool. Unlike the weather"

clean1:
	@rm -rf bin

clean:
	@rm -rf bin
	@echo "Ho gaya saaf"
