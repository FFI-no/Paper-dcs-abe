#!/usr/bin/env python3
#
# An attempt to pack attributes relatively efficiently.

import random
from math import ceil
import zlib
from google.protobuf.message import Message

import abeprototest_pb2

# Proxy to G1 elements. We assume that G1 and G2 elements have the same size,
# which they do in OpenABE.
def get_group_elem() -> bytes:
	return random.randbytes(32)

def pack_ciphertext(attrs, ciph1=None, ciph2=None, IV=None, authtag=None, aesciph=None):
	message = abeprototest_pb2.oabe_ciphertext()

	if IV is not None: assert(len(IV) == 12)
	if authtag is not None: assert(len(authtag) == 16)
	if aesciph is not None: assert(len(aesciph) == 32)

	tmp = abeprototest_pb2.oabe_numattrs()

	for k, val in attrs.items():
		if type(val) is list:
			# the first (zeroth) item is the number itself also, it is an
			# unsigned 32-bit int turn 'num' into bytes (big endian) and put it
			# in position 0.
			num = val[0]
			num_bytes = num.to_bytes(ceil(num.bit_length() / 8), 'big')
			tmp = abeprototest_pb2.oabe_numattrs()
			tmp.attrmap[0] = num_bytes
			for j in range(len(val[1])):
				tmp.attrmap[j+1] = val[1][j]
			message.attrs[k].CopyFrom(tmp)
		else:
			tmp = abeprototest_pb2.oabe_numattrs()
			tmp.attrmap[0] = val
			message.attrs[k].CopyFrom(tmp)

	message.ciph1 = get_group_elem() if ciph1 is None else ciph1
	message.ciph2 = get_group_elem() if ciph2 is None else ciph2

	message.IV = random.randbytes(12) if IV is None else IV # 96 bits
	message.authtag = random.randbytes(16) if authtag is None else authtag # 128 bits
	message.aesciph = random.randbytes(32) if aesciph is None else aesciph # 256 bits

	out = message.SerializeToString()

	return out

def unpack_ciphertext(inp: Message):

	msg = abeprototest_pb2.oabe_ciphertext()
	msg.ParseFromString(inp)

	ciph1 = msg.ciph1
	ciph2 = msg.ciph2
	IV = msg.IV
	authtag = msg.authtag
	aesciph = msg.aesciph

	attrs = {}
	attrout = msg.attrs

	for k, val in attrout.items():
		# Handle numbers specially
		if 1 in val.attrmap:
			# the num is the zeroth item of the list, the rest are G1-elements.
			num = int.from_bytes(val.attrmap[0], 'big')
			tmp = [val.attrmap[k] for k in range(1, len(val.attrmap))]
			attrs[k] = [num, tmp]

		else:
			attrs[k] = val.attrmap[0]

	return {"attrs": attrs, "ciph1": ciph1, "ciph2": ciph2, "IV": IV,
	        "authtag": authtag, "aesciph": aesciph}


def simple_test():
	# Formatted relatively nicely for quality of life.
	# Has one g1-elem for each bit used to store the num
	# UUID-s are now no longer UUID-s proper, but random G1 elements
	attrs = {
		"country_code:NOR": get_group_elem(),
		"org_FFI": get_group_elem(),
		"CL":[3, [get_group_elem() for k in range(4) ]],
		"time":[1751615435, [get_group_elem() for k in range(32) ]],
		"uuid":get_group_elem(),
	}

	IV = random.randbytes(12)
	authtag = random.randbytes(16)
	aesciph = random.randbytes(32)

	ciph1 = get_group_elem()
	ciph2 = get_group_elem()

	out_str = pack_ciphertext(attrs, ciph1=ciph1, ciph2=ciph2, IV=IV,
	                          authtag=authtag, aesciph=aesciph)

	print(f"Protobuf: {len(out_str)}")
	print(f"Protobuf (compressed): {len(zlib.compress(out_str, wbits=-15, level=9))}")

	recovered = unpack_ciphertext(out_str)

	assert(recovered["attrs"] == attrs)
	print(recovered["attrs"] == attrs)
	assert(recovered["ciph1"] == ciph1)
	assert(recovered["ciph2"] == ciph2)
	assert(recovered["IV"] == IV)
	assert(recovered["authtag"] == authtag)
	assert(recovered["aesciph"] == aesciph)

if __name__ == '__main__':
	simple_test()
