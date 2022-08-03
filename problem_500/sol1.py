"""
Problem 500 Problem 500!!!: https://projecteuler.net/problem=500

Description:

The number of divisors of 120 is 16.
In fact 120 is the smallest number having 16 divisors.
Find the smallest number with 2^(500500) divisors.
Give your answer modulo 500500507.

Solution:

The number of total divisors of a number n is given by the product
of the exponents of its prime factor decomposition, provided that we
increase each exponent by 1. 
(See https://math.stackexchange.com/questions/2877738/why-multiplying-powers-of-prime-factors-of-a-number-yields-number-of-total-divis)

We build two lists 'num_seq' and 'compare_seq'.
The former is needed to speed up computation time, while the latter
is used to determine whether we should increase the exponent of a given
prime factor or include the next unused prime to determine the smallest 
number having N divisors (where N is a power of 2).

On one hand, 'num_seq' stores the amount of time we increased the exponent of a given prime.
In particular, given the formula to map an element of 'num_seq' to its corresponding 
integer is as follows:

x = p ** (2 ** (exp) - 1)

where x is the integer, p is the prime and exp is the number stored in 'num_seq'

On the other hand, 'compare_seq' is used to determine whether we should increase the 
exponent of a prime p or if we should add the next prime.
In particular, we check if compare_seq[i] < next_prime and if that is the case
we increase the exponent. Infact, adding the next prime or increasing the exponent
always doubles the number of total divisors, but we want to obtain the minumum integer 
with N divisors, thus we need to always multiply the smallest possible number.
[It is important to observe that this method only works if N is a power of 2]
If we increase the exponent, the formula to update compare_seq is as follows:

new_exp = 2 * log_p(compare_seq[i]) [log is in base_p]
compare_seq[i] = p ** new_exp

Time: 18.0 sec  
"""
import math
import numpy 

def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    # Code from: https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n

    sieve = numpy.ones(n//3 + (n%6==2), dtype=bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]

def next_el(compare_seq, num_seq, next_prime, list_primes):
    for i in range(len(compare_seq)):
        # if the number is smaller than the next prime, 
        # increase the exponent!
        if compare_seq[i] < next_prime:
            exponent = 2 * math.log(compare_seq[i], list_primes[i])
            compare_seq[i] = list_primes[i] ** exponent
            num_seq[i] += 1
            return compare_seq, num_seq, False
        
        # otherwise, keep checking!
        # Computation trick: we need to check only for the smallest 
        # prime that has exponent 1 
        # (None of the followings could work if this did not work)
        if num_seq[i] == 1:
            compare_seq.append(next_prime ** 2)
            num_seq.append(1)
            return compare_seq, num_seq, True

def convert_seq(seq, list_primes, M=500500507):
    """
    Given 'num_seq', it returns the corresponding integer
    It performs each operation mod M
    """
    ans = 1
    for i in range(len(seq)):
        temp = convert_el(el=list_primes[i], exponent=seq[i], M=M)
        ans = ans * temp % M
    return ans

def convert_el(el, exponent, M=500500507):
    """
    It return: el ** (2 ** (exponent) - 1) mod M
    """
    ans = 1
    for _ in range(2**(exponent)-1):
        ans = ans * el % M
    return ans
    

def solution(N=500500, M=500500507) -> int:
    """
    It return the smallest integer n with a total number of divisors 2**N
    modulo M = 500500507
    >>> solution(2)
    8
    >>> solution(4)
    120
    >>> solution(5)
    840
    """
    # initialization
    list_primes = primesfrom2to(n=10**7)
    compare_seq = [4]
    num_seq = [1]
    prime_pos = 1

    for _ in range(N - 1):
        compare_seq, num_seq, next_prime = next_el(compare_seq, num_seq, list_primes[prime_pos], list_primes)
        if next_prime:
            prime_pos += 1
    
    return int(convert_seq(num_seq, list_primes, M=M))

if __name__ == "__main__":
    print(f"{solution() = }")



