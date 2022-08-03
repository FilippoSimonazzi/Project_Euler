"""
Problem 227 The Chase: https://projecteuler.net/problem=227

Description:

The Chase is a game played with two dice and an even number of players.

The players sit around a table and the game begins with two opposite players having one die each. On each turn, the two players with a die roll it.

If the player rolls 1, then the die passes to the neighbour on the left.
If the player rolls 6, then the die passes to the neighbour on the right.
Otherwise, the player keeps the die for the next turn.

The game ends when one player has both dice after they have been rolled and passed; that player has then lost.

In a game with 100 players, what is the expected number of turns the game lasts?

Give your answer rounded to ten significant digits.


Solution:


Time: 18.0 sec  
"""
import numpy as np

def build_matrix(N=100):
    """
    It generates the markov chain transition matrix
    that describes the problem for N players.

    It returns this matrix M and the vector v = [0, 0, .., 1]
    """

    # build matrix
    M = np.zeros((N//2+1, N//2+1))

    # First and last rows are fixed!
    M[0][0] = 1

    M[1][0] = 8
    M[1][1] = 19
    M[1][2] = 8
    M[1][3] = 1

    M[N//2-1][N//2] = 8
    M[N//2-1][N//2-1] = 19
    M[N//2-1][N//2-2] = 8
    M[N//2-1][N//2-3] = 1

    M[N//2][N//2] = 18
    M[N//2][N//2-1] = 16
    M[N//2][N//2-2] = 2

    for i in range(2, N//2-1):
        M[i][i-2] = 1
        M[i][i-1] = 8
        M[i][i] = 18
        M[i][i+1] = 8
        M[i][i+2] = 1

    M = np.transpose(M)
    M /= 36
    v = np.zeros(N//2+1)
    v[-1] = 1

    return M, v

def solution(N=100):
    """
    It returns the expected number of turns for the Chase Game
    up to ten decimal digits
    """

    M, v = build_matrix(N)
    stop = False
    prob_zero = 0
    mean = 0
    t = 1
    while not stop:
        v[0] = 0
        v = np.dot(M, v)

        v /= sum(v)

        new_prob = v[0]
        mean += new_prob * t
        prob_zero += (1 - prob_zero) * new_prob


    if prob_zero > 1 - 1/10**10:
        stop = True
    
    return np.round(mean, 10)

if __name__ == "__main__":
    print(f"{solution() = }")

# OSS: This code is theoretically correct but the 
# numpy implementation of np.dot() leads to numerical issues...

# the file sol2.py solves the issue

