import matplotlib.pyplot as plt
from math import pi, cos

pi_4 = pi ** 4
gamma = 1


def d2qdt2_func(xi: float, dqdt: float, q: float, n: int, time_step: float) -> float:
    n_pi_4 = (n ** 4) * pi_4
    return - (xi*dqdt + n_pi_4 * (q + dqdt * time_step)) / (1 + xi * time_step + n_pi_4 * time_step * time_step / 2)


def dqdt_func(d2qdt2: float, dqdt: float, time_step: float) -> float:
    return d2qdt2 * time_step + dqdt


def q_func(d2qdt2: float, dqdt: float, q: float, time_step: float) -> float:
    return d2qdt2 * time_step * time_step / 2 + dqdt * time_step + q


def xi_func(xi: float, T: float, Ts: float, time_step: float) -> float:
    return xi + (T - Ts) * gamma * time_step


def T_func(dqdt_arr: list) -> float:
    rtrn = 0.0
    for dqdt in dqdt_arr:
        rtrn += dqdt * dqdt / 2
    return rtrn


def plot(x: list, y: list, name: str = '', color: str = 'red') -> None:
    plt.figure()
    plt.rcParams["figure.autolayout"] = True
    plt.title(name)
    plt.plot(x, y, color=color)


if __name__ == '__main__':
    step = 0.0001
    n = 300
    qn = [0] * n
    dqndt = [0] * n
    xi = 0
    d2qndt2 = [0] * n
    Ts_inf = 1/4
    xi_arr = []
    time = []
    temp = []
    T = 0
    for i in range(n - 1):
        dqndt[i + 1] = 2 * (1 - cos((i + 1) * pi)) / ((i + 1) * pi)
    for t in range(120000):
        for i in range(n):
            d2qndt2[i] = d2qdt2_func(xi, dqndt[i], qn[i], i, step)
            qn[i] = q_func(d2qndt2[i], dqndt[i], qn[i], step)
            dqndt[i] = dqdt_func(d2qndt2[i], dqndt[i], step)
        T  = T_func(dqndt)
        xi = xi_func(xi, T, Ts_inf, step)
        xi_arr.append(xi)
        temp.append(T)
        time.append(t * step)
    plot(time, xi_arr, r'$\xi  vs. t$' + "\n" + r'for  $\bar{T}_s(\infty) = $' + str(Ts_inf))
    plot(time, temp, r'$\bar{T}_s vs. t$' + "\n" + r'for  $\bar{T}_s(\infty) = $' + str(Ts_inf))
    plt.show()
