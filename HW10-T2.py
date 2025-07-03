#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

def f(x):
    return x ** 2

def monte_carlo_integral(f, a, b, n):
    x = np.random.uniform(a, b, n)
    y = f(x)
    return (b - a) * np.mean(y)

def generate_plot(a, b, plot_file):
    x = np.linspace(a - 0.5, b + 0.5, 400)
    y = f(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', linewidth=2)
    ix = np.linspace(a, b, 100)
    iy = f(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.axvline(x=a, color='gray', linestyle='--')
    ax.axvline(x=b, color='gray', linestyle='--')
    ax.set_title(f'Графік інтегрування f(x)=x^2 від {a} до {b}')
    plt.grid()
    plt.tight_layout()
    fig.savefig(plot_file)
    plt.close(fig)

def generate_readme(mc, quadv, qerr, rel_err, plot_file, path='README.md', n_samples=None):
    lines = []
    lines.append('# Завдання 2. Обчислення визначеного інтеграла методом Монте-Карло\n')
    if n_samples:
        lines.append(f'- Кількість випадкових точок (n): **{n_samples}**\n')
    lines.append(f'- Результат Monte Carlo: **{mc:.6f}**\n')
    lines.append(f'- Результат quad (SciPy): **{quadv:.6f}**, похибка оцінки **{qerr:.2e}**\n')
    lines.append(f'- Відносна похибка Monte Carlo: **{rel_err:.4%}**\n')
    lines.append('\n## Графік функції та області інтегрування\n')
    lines.append(f'![]({plot_file})\n')
    lines.append('## Висновки\n')
    lines.append('- Метод Монте-Карло дає наближений результат; точність зростає з кількістю вибірок.\n')
    lines.append('- SciPy quad видає дуже точний аналітичний результат як еталон.\n')
    lines.append('- Для n ≳ 10^5 відносна похибка падає до кількох відсотків, але поступається детермінованим методам.\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(
        description="Обчислення інтегралу f(x)=x^2 від a до b методом Monte Carlo та quad"
    )
    parser.add_argument('--samples', '-n', type=int, default=100000,
                        help='Кількість точок Monte Carlo (за замовчуванням: 100000)')
    parser.add_argument('--readme', '-r', default='README.md',
                        help='Шлях до файлу README (за замовчуванням: README.md)')
    parser.add_argument('--plot', '-p', default='integral_plot.png',
                        help='Шлях до файлу з графіком (за замовчуванням: integral_plot.png)')
    parser.add_argument('--a', type=float, default=0.0, help='Нижня межа інтегрування')
    parser.add_argument('--b', type=float, default=2.0, help='Верхня межа інтегрування')
    args = parser.parse_args()

    # Monte Carlo
    mc = monte_carlo_integral(f, args.a, args.b, args.samples)
    # SciPy quad
    quadv, qerr = spi.quad(f, args.a, args.b)
    rel_err = abs(mc - quadv) / abs(quadv)

    # Графік та README
    generate_plot(args.a, args.b, args.plot)
    generate_readme(mc, quadv, qerr, rel_err, args.plot,
                    path=args.readme, n_samples=args.samples)

    # Вивід на екран
    print(f'Monte Carlo: {mc:.6f}')
    print(f'Quad:        {quadv:.6f} ± {qerr:.2e}')
    print(f'Rel. error:  {rel_err:.4%}')
    print(f'Plot saved:  {args.plot}')
    print(f'README saved: {args.readme}')

if __name__ == '__main__':
    main()
