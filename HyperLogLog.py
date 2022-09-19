
from math import log2, log
from BitVector import BitVector
from hashlib import sha1

from random import randint #erase!!!

"""
Pay attention! num_of_buckets == 2 ** first_b_bits. 
In addition, the number of buckest should (probably) be a power of 2,
starting with 16.
"""
num_of_buckets = 1024
first_b_bits = int(log2(num_of_buckets))

"""
pay attention! if your hash returns an int that cannot be represented in 64 bits,
then an error will be thrown in hll_add_element function.
"""
bin_hash_size = 32
bucket_size = int(log2(bin_hash_size)) #in bits. this can cope with up to 2**(2**(bucket_size)) different cid's


# we start with initializing all the registers to 0
regs = []
for x in range(num_of_buckets): 
	regs.append(BitVector(intVal = 0, size = bucket_size))

def get_element_hashed(cid):
	global bin_hash_size
	hashed = sha1(str(cid).encode())
	digest = hashed.hexdigest()
	size = int(bin_hash_size/4)
	digest_int = int(digest[:size],16)
	return digest_int

def get_leftmost_bit(bv):
	pos = len(bv)
	while(bv.intValue() != 0):
		bv.shift_right(1)
		pos = pos - 1
	return pos

def get_alpha_constant():
	global num_of_buckets
	if num_of_buckets <= 16:
		return 0.673
	elif num_of_buckets == 32:
		return 0.697
	elif num_of_buckets == 64:
		return 0.709
	else:
		return 0.7213/(1+(1.079/num_of_buckets))	
		
def get_rho(w, max_width):
	rho = max_width - w.bit_length() + 1
	return rho

def hll_add_element(cid):
	global num_of_buckets, first_b_bits, bucket_size, regs, bin_hash_size, make_string
	
	#first step- hashing the cid
	hashed_cid = get_element_hashed(cid)
	
	#second step- finding the suitable bucket through the first b bits
	reg_index = hashed_cid & (num_of_buckets - 1)
	
	#third step- finding the leftmost bit in the rest of the hashed_cid_binary 
	w = hashed_cid >> first_b_bits
	leftmost_bit = get_rho(w, bin_hash_size - first_b_bits)
	
	#final step- save the pos of the biggest leftmost bit in the right bucket
	# PAY ATTENTION! If the size of the bucket is too small, an exception will be thrown! 
	regs[reg_index].setValue(intVal = max(regs[reg_index].intValue(), leftmost_bit), size = bucket_size)


def hll_count_cardinality():
	global regs, num_of_buckets
	alpha = get_alpha_constant()
	harmonic_mean = sum([pow(2,-x.intValue()) for x in regs])
	harmonic_mean = 1/harmonic_mean
	m_power2 = num_of_buckets ** 2
	cardinality = alpha * m_power2 * harmonic_mean
	count = 0
	#counting empty buckets
	for x in range(num_of_buckets):
		if regs[x].intValue() == 0:
			count = count + 1
	if cardinality <= 5 * num_of_buckets :
		if count != 0:
			cardinality = num_of_buckets * log(num_of_buckets/count)
	
	return cardinality
	
	
"""
next step- sniffing a quic connection id (cid) and adding to hll:
"""
# initialize an empty SET that will count the real cardinality
counter = {1}
counter.remove(1)

print("~~adding phase~~~")
for x in range(100000):
	cid = randint(1,100000)
	hll_add_element(cid)
	counter.add(cid)
print("~~finished adding~~~")
"""
for x in regs:
	print(x.intValue())
"""
print("~~counting phase~~~")
x = hll_count_cardinality()
print("~~finished counting~~~")
print("the estimated cardinality is:")
print(x)
print("the real cardinality is:")
print(len(counter))


print("byebye!")
input()

