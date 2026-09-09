<!--
Shared Week 2 prerequisites.

This duplication is intentional: the same implementations remain visible in
the teaching material, while this hidden setup cell makes every section usable
directly after a page reload. Running a visible implementation simply replaces
the identical definition in the shared Python session.
-->

```{pyodide-python}
#| context: setup

import math

import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x**3 + x - 1


def g1(x):
    return 1 - x**3


def g2(x):
    # Reell kubikkrot, også for negative argumenter
    return np.cbrt(1 - x)


def g3(x):
    return (2*x**3 + 1)/(3*x**2 + 1)


def iterate(g, x0, number_of_steps):
    """Returner x_0, x_1, ..., x_n."""
    values = [float(x0)]
    for _ in range(number_of_steps):
        values.append(g(values[-1]))
    return np.array(values)


solution = 0.6823278038280193
r_reference = solution


def cobweb_plot(g, x0, number_of_steps=20,
                x_min=0, x_max=1, title="Spindelvevplott"):
    x_grid = np.linspace(x_min, x_max, 800)
    y_grid = np.array([g(x) for x in x_grid])
    values = iterate(g, x0, number_of_steps)

    plt.close("all")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(x_grid, y_grid, label="$y=g(x)$")
    ax.plot(x_grid, x_grid, "k--", label="$y=x$")

    current = values[0]
    for next_value in values[1:]:
        ax.plot([current, current], [current, next_value], color="tab:red")
        ax.plot([current, next_value], [next_value, next_value], color="tab:red")
        current = next_value

    ax.set(xlim=(x_min, x_max), ylim=(x_min, x_max),
           xlabel="$x$", ylabel="$y$", title=title)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.legend()
    plt.show()
    return values


def fixed_point(g, x0, f=None, atol=1e-10, rtol=1e-10, maxiter=100):
    """Fikspunktiterasjon x_(n+1)=g(x_n), med diagnostikk."""
    x = float(x0)
    history = [x]
    steps = []
    residual = lambda value: abs(f(value)) if f is not None else abs(g(value)-value)
    residuals = [residual(x)]

    def result(value, converged, reason, iterations):
        return {"x": value, "converged": converged, "reason": reason,
                "iterations": iterations, "history": np.array(history),
                "steps": np.array(steps), "residuals": np.array(residuals)}

    for iteration in range(1, maxiter + 1):
        x_new = g(x)

        if not math.isfinite(x_new):
            return result(x_new, False, "ikke-endelig verdi", iteration)

        step = abs(x_new - x)
        history.append(x_new)
        steps.append(step)
        residuals.append(residual(x_new))

        tolerance = atol + rtol*abs(x_new)
        if step <= tolerance:
            return result(x_new, True, "lite skritt", iteration)
        x = x_new

    return result(x, False, "maksimalt antall iterasjoner", maxiter)


def make_sqrt_iteration(a):
    def g(x):
        return 0.5*(x + a/x)
    return g


def make_sqrt_equation(a):
    def f(x):
        return x*x - a
    return f
```
