# SlidingHyperLogLog
Python implementation of the HyperLogLog algorithm - estimating the cardinality of a given multiset’s distinct elements, with the added feature to count only the cardinality of the last _"window of time"_ seconds.  
If you are not familiar with the algorithm, i highly recommend to read the full explanation in **_Sliding_HyperLogLog_full_explanation.pdf_**, which include what is this algorithm, why it is so important and a top down description of the code.


## Installation:
- Make sure you have a Python version of at least 3.0 version.
- Install BitVector library:
`pip install BitVector`

## The 3 files:
### 1. sliding_hll.py:
Implementation of the Sliding HyperLogLog algorithm, with the main purpose of counting the cardinality of all the [QUIC](https://en.wikipedia.org/wiki/QUIC)   connections that are up in the last _"window of time"_ seconds.  
The elements in this file are QUIC's dcid (destination connection id) parameters.  

#### Running the script:
You can either run the script without changing the parameters:  
Window’s cmd: `python sliding_hll.py`.  
  Or with Linux’s terminal: `python3 sliding_hll.py`.  
  If you want to change the parameters too, then:  
  `python sliding_hll.py <size_of_hash_outcome> <number_of_buckets> <size_of_window> <testing_mode>`  
  Or with linux:  
  `python3 sliding_hll.py <size_of_hash_outcome> <number_of_buckets> <size_of_window> <testing_mode>`  
 
 The parameters as seen above are the same as in the Sliding HyperLogLog algorithm:  
 
 - The number of bits the hash function return, from it we derive the bucket size.
 - The number of buckets- to know how many buckets and what is the size of the variable ‘b’. This value also must be a power of 2.
 - The size of the time window in seconds.
 - The testing mode means if we want to count the real number of active flows simultaneously. This value can either be empty, which means that we are not counting the real cardinality, or ‘y’ which means we do count it.  

 If instead of the original NIC you are using a different NIC/interface, you need to explicitly add it here (line 233):  
 ```python
 live_cap = pyshark.LiveCapture(interface=<name_of_interface>, display_filter="quic", include_raw=True, use_json=True)
  ```  
### 2. sliding_testing:
Another implementation of the Sliding HyperLogLog algorithm, but mainly for debugging purposes.  
Thus, the multiset's size and the distinct elements are generated through the `randint()` function and the size of the "for" loop.  
The rest of the explanations - how to run the code and what are the parameters - are as written in the previous section.

### 3. HyperLogLog.py:  
Implementaion of the HyperLogLog algorithm, without the Sliding feature.  
This file was created while implementing the full Sliding algorithm, and I decided to keep it.  
It's main purpose is debugging only the HyperLogLog part of the algorithm: In the end of the file you can decide how many elemenets would be (with repititions), and then, randomly chosen, how many distinct elements would be generated.  
This file does not have an easy way to change its parameters, but to manualy change them after copying the file.  
In order to run the file, after choosing the parameters, simply type: `python HyperLogLog.py` or `python3 HyperLogLog.py`.
   
   

  

  
