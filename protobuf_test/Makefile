.PHONY: all clean

all: abeprototest_pb2.py

abeprototest_pb2.py:
	protoc --proto_path=. --python_out=. abeprototest.proto

clean:
	rm -f abeprototest_pb2.py
	rm -rf __pycache__
