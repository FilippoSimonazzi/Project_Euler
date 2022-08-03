import sys


def solution():
    v = [[0] for _ in range(51)]
    v[50] = [1]
    M = build_trans_matrix()
    expected_value = 0.0
    for i in range(1, 150001):
        v[0][0] = 0
        v = m_v_multiply(M, v)
        expected_value += v[0][0] * i
        if i % 1000 == 0:
            print(i, expected_value)
    return expected_value

def build_trans_matrix():
    transition_matrix = [[0 for _ in range(51)] for _ in range(51)]
    transition_matrix[0][0] = 1
    transition_matrix[0][1] = 2 / 9
    transition_matrix[1][1] = 1 / 2 + 1 / 36
    transition_matrix[2][1] = 2 / 9
    transition_matrix[3][1] = 1 / 36
    for i in range(2, 49):
        transition_matrix[i - 2][i] = 1 / 36
        transition_matrix[i - 1][i] = 2 / 9
        transition_matrix[i][i] = 1 / 2
        transition_matrix[i + 1][i] = 2 / 9
        transition_matrix[i + 2][i] = 1 / 36
    transition_matrix[47][49] = 1 / 36
    transition_matrix[48][49] = 2 / 9
    transition_matrix[49][49] = 1 / 2 + 1 / 36
    transition_matrix[50][49] = 2 / 9
    transition_matrix[48][50] = 1 / 36 + 1 / 36
    transition_matrix[49][50] = 2 / 9 + 2 / 9
    transition_matrix[50][50] = 1 / 2
    return transition_matrix

def m_v_multiply(x, y):
    rv = [[0 for _ in range(len(y[0]))] for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                rv[i][j] += x[i][k] * y[k][j]
    return rv

if __name__ == "__main__":
    print(f"{solution() = }")
