"""
Solution to Euler Problem 467 : https://projecteuler.net/problem=467

"""

from math import ceil, log 

import shelve 
import os 

indexed_primes = {} 
not_primes     = set() 
primes         = set() 
prime_hint     = 10000 * log(10000)
dp_cache_path  = ".problem467_dp_cache.db"

"""
Returns true if the argument is a prime. Uses caches to speed up computation
"""
def is_prime(n):

    # First check the caches 
    if n in not_primes:
        return False
    
    if n in primes:
        return True 

    # Brute force check for primality caching the result
    for div in range(2,ceil(n/2)+1):
        if n % div == 0:            
            not_primes.add(n)
            return False

    primes.add(n)

    # If we have found a prime then any multiples of it are not primes so we 
    # can add those to the cache.
    if n > 1:
        n_composite = n   
        while n_composite < prime_hint:
            n_composite += n         
            not_primes.add(n_composite)

    return True 

"""
Returns the Nth prime number. Checks the cache or does a brute force search
"""
def prime(n):
    if n in indexed_primes:
        return indexed_primes[n]
    else:
        p = 1
        for i in range(0,n):
            p += 1
            while(not is_prime(p)):
                p += 1
            
        indexed_primes[n] = p 
        return p

"""
Returns the Nth composite number.
"""
def composite(n):
    c = 0
    for i in range(0,n):
        c += 1
        while(is_prime(c)):
            c += 1
            
         
    return c

"""
Returns digits of an integer as a list
"""
def digits(n):
     return [int(i) for i in str(n)]

"""
Returns the digital root of an integer as defined in the exercise.
"""
def digital_root(n):
    root = n
    while(root > 9):
        root = sum(digits(root))
    
    return root 
"""
Given a list of integers returns a new integer where each digit is the digital
root of an integer in the input list
"""
def root_signeture(n):
    roots  = list(map(digital_root, n))
    result = 0
    for digit in range(0, len(roots)):
        result += roots[len(roots) - digit -1] * 10**digit 

    return result

"""
As defined in the exercise
"""
def C(n):
    composites = map(composite, range(1,n + 1))
    return root_signeture(composites)

"""
As defined in the exercise
"""
def P(n):
    primes = map(prime, range(1,n + 1))
    return root_signeture(primes)

"""
Check if the first argument is a sub-integer of the second. Not actually used 
in this implementation but I figured I would keep around anyway.
"""
def is_superinteger(sub, super):
    sub_iter = iter(str(sub))
    super_iter = iter(str(super))

    sub_next = next(sub_iter)
    try:
        while(True):
            
            super_next = next(super_iter)
            if sub_next == super_next:
                try:
                    sub_next = next(sub_iter)
                except StopIteration:
                    return True 
    except StopIteration:
        return False 

"""
Cost of appending the digits in seq to the solution. LSB first.
"""
def remaider_cost(seq):
        result = 0 
        n      = 1 
        for c in seq: 
            result += int(c) * 10**n
            n      +=1 
        return result

def subseq(seq, n):
    return seq[len(seq) - n:]

"""
Precomputes the solutions to all the superinteger subproblems and returns the 
result as a dict indexed by the length of the remaining integer from the 
least significant bit.

"""
def precompute_costs(seq1, seq2):

    if os.path.exists(dp_cache_path):
        print("DP cache file " + dp_cache_path + "already exists!!!")
        exit()

    # Use shelve to reduce memory usage 
    result = shelve.open(dp_cache_path) 
    result.clear()

    def set_result(i1, i2, c):
        result[str((i1,i2))] = c 

    def get_result(i1, i2):
        return result[str((i1,i2))]

    seq1   = seq1[::-1]
    seq2   = seq2[::-1]
    
    for (i1,i2) in [(i1,i2) 
                        for i1 in range(len(seq1) + 1) 
                        for i2 in range(len(seq2) + 1)]:
        
        # If we reached the end of both integers then the cost is 0
        if i1 == 0 and i2 == 0:
            set_result(i1, i2, 0)
            continue 

        remainder1 = subseq(seq1, i1)
        remainder2 = subseq(seq2, i2)

        # If we reached the end of one of the integers then the cost is 
        # the value of the other integer 
        if i1 == 0:
            set_result(i1, i2, remaider_cost(remainder2))
            continue            
        
        elif i2 == 0:
            set_result(i1, i2, remaider_cost(remainder1))
            continue

        # If the heads of both sequences are the same there is no choice to make 
        # and we just compute the cost and store it 
        if remainder1[0] == remainder2[0]:
            set_result(i1,i2, int(remainder1[0]) + 10 * get_result(i1 - 1, i2 - 1))
            continue

        # If the heads are different we compute the cost of appending either one 
        s1_cost = int(remainder1[0]) + 10 * get_result(i1 - 1, i2    )
        s2_cost = int(remainder2[0]) + 10 * get_result(i1    , i2 - 1)
        
        # Then we pick the least costly one as the result.
        if s1_cost > s2_cost:
            set_result(i1, i2, s2_cost)
            
        else:
            set_result(i1, i2, s1_cost)
    
    return result 

"""
This function uses dynamic programming to compute the smallest super integer 
of two integers. It expects the two integers to be passed as strings.
"""           
def smallest_supersequence(seq1, seq2):

    costs = precompute_costs(seq1, seq2)

    """
    Return minimum cost of a super integer of integer s1 and s2 starting at 
    digit 'n' in the solution from the cache.
    """
    def cost(s1, s2):
        return costs[str((len(s1), len(s2)))]        
               

    # We build up the super-integer from the least significant end by
    # picking the least costly subsequence to take the next integer from.
    result = ""

    seq1 = seq1[::-1]
    seq2 = seq2[::-1]

    while True:
        if len(seq1) == 0:
            result += seq2
            break
        
        elif len(seq2) == 0:
            result += seq1
            break


        if seq1[0] == seq2[0]:
            result += seq1[0]
            seq1 = seq1[1:]
            seq2 = seq2[1:]

        elif cost(seq1[1:], seq2) > cost(seq1, seq2[1:]):
            result += seq2[0]
            seq2 = seq2[1:]

        else:
            result += seq1[0]
            seq1 = seq1[1:]

    # Clean up
    costs.close()
    os.remove(dp_cache_path)
    return result[::-1]

"""
As defined in the exercise
"""
def f(n):
    return int(smallest_supersequence(str(P(n)), str(C(n))))


# Evaluate the function - note that evaluating f(10 000) will take a very long time and 
# and require 100s of gigabytes of space. 
for N in  [10,100,1000]:
    print("Computing f(" + str(N) + ")")
    result = f(N)
    if N == 10:
        print("f(" + str(N) + ") = " + str(result))
    else:
        print("f(" + str(N) + ") mod 1 000 000 007 = " + str(result % 1000000007))



