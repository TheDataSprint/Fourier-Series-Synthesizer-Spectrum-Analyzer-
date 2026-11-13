"""
Fourier Series Synthesizer & Spectrum Analyzer
==============================================
Signals and Systems - Course Project

A menu-driven Python program that
  * synthesizes standard periodic waveforms from their Fourier series,
  * shows how the approximation improves as harmonics are added
    (including the Gibbs phenomenon),
  * analyzes the frequency content of a signal with the FFT and checks it
    against the theoretical Fourier coefficients,
  * studies approximation error and verifies Parseval's theorem, and
  * lets the user build a custom signal from hand-picked harmonics.

Run the interactive menu :  python fourier_synthesizer.py
Generate output_graph.png:  python fourier_synthesizer.py --demo

Only NumPy and Matplotlib are required.
"""

import argparse

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Waveform catalogue
# ---------------------------------------------------------------------------
WAVEFORMS = {
    "square": "Square wave",
    "sawtooth": "Sawtooth wave",
    "triangle": "Triangle wave",
    "full_rectified": "Full-wave rectified sine",
    "half_rectified": "Half-wave rectified sine",
}

# Plot colours (kept in one place so every figure looks consistent)
C_IDEAL = "#222222"
C_SYNTH = "#1f77b4"
C_FFT = "#2a9d8f"
C_THEORY = "#d62828"
KIND_COLORS = {
    "square": "#1f77b4",
    "sawtooth": "#e76f51",
    "triangle": "#2a9d8f",
    "full_rectified": "#8e6bbf",
    "half_rectified": "#e9a820",
}


# ---------------------------------------------------------------------------
# 2. Core mathematics
# ---------------------------------------------------------------------------
def fourier_coefficients(kind, amp, n_harm):
    """
    Trigonometric Fourier series coefficients of a periodic waveform:

        x(t) = a0 + sum_{k=1..N} [ a_k cos(k w0 t) + b_k sin(k w0 t) ]

    Returns (a0, a, b) where a and b are arrays of length N + 1
    (index k = harmonic number; index 0 is unused and left at zero).
    """
    k = np.arange(n_harm + 1)
    a0 = 0.0
    a = np.zeros(n_harm + 1)
    b = np.zeros(n_harm + 1)
    odd = (k % 2 == 1)
    even = (k % 2 == 0) & (k >= 2)

    if kind == "square":                       # odd, +/-A
        b[odd] = 4 * amp / (np.pi * k[odd])
    elif kind == "sawtooth":                   # odd, ramps -A -> +A
        pos = k >= 1
        b[pos] = (2 * amp / np.pi) * (-1.0) ** (k[pos] + 1) / k[pos]
    elif kind == "triangle":                   # odd, peak value A
        b[odd] = (8 * amp / np.pi ** 2) * (-1.0) ** ((k[odd] - 1) // 2) / k[odd] ** 2
    elif kind == "full_rectified":             # A |sin(w0 t)|
        a0 = 2 * amp / np.pi
        a[even] = -4 * amp / (np.pi * (k[even] ** 2 - 1))
    elif kind == "half_rectified":             # A max(sin(w0 t), 0)
        a0 = amp / np.pi
        if n_harm >= 1:
            b[1] = amp / 2
        a[even] = -2 * amp / (np.pi * (k[even] ** 2 - 1))
    else:
        raise ValueError(f"Unknown waveform: {kind}")
    return a0, a, b


def ideal_waveform(kind, t, f0, amp):
    """The exact (infinite-bandwidth) waveform, used as the reference."""
    theta = 2 * np.pi * f0 * t
    if kind == "square":
        return np.where(np.sin(theta) >= 0, amp, -amp)
    if kind == "sawtooth":
        return amp * (2 * ((f0 * t + 0.5) % 1.0) - 1)
    if kind == "triangle":
        return amp * (2 / np.pi) * np.arcsin(np.sin(theta))
    if kind == "full_rectified":
        return amp * np.abs(np.sin(theta))
    if kind == "half_rectified":
        return amp * np.maximum(np.sin(theta), 0.0)
    raise ValueError(f"Unknown waveform: {kind}")


def synthesize(t, f0, a0, a, b):
    """Sum the Fourier series terms to build the signal on the time axis t."""
    w0 = 2 * np.pi * f0
    x = np.full(t.shape, float(a0))
    for k in range(1, len(a)):
        if a[k] != 0.0:
            x += a[k] * np.cos(k * w0 * t)
        if b[k] != 0.0:
            x += b[k] * np.sin(k * w0 * t)
    return x


def make_time_axis(f0, n_harm, n_periods):
    """
    Time axis covering an exact whole number of periods, sampled well above
    the Nyquist rate of the highest harmonic.  Using whole periods means the
    FFT has no spectral leakage, so harmonics fall exactly on FFT bins.
    """
    samples_per_period = max(512, 16 * n_harm)
    fs = samples_per_period * f0
    t = np.arange(samples_per_period * n_periods) / fs
    return t, fs


def amplitude_spectrum(x, fs):
    """Single-sided amplitude spectrum of x using the FFT."""
    n = len(x)
    spec = np.abs(np.fft.rfft(x)) / n
    spec[1:] *= 2.0                      # fold negative frequencies in
    if n % 2 == 0:
        spec[-1] /= 2.0                  # Nyquist bin is not doubled
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    return freqs, spec


def harmonic_amplitudes(a0, a, b):
    """Theoretical amplitude c_k = sqrt(a_k^2 + b_k^2); c_0 = |a0|."""
    c = np.hypot(a, b)
    c[0] = abs(a0)
    return c


def power_time(x):
    """Average power computed in the time domain."""
    return float(np.mean(x ** 2))


def power_freq(a0, a, b):
    """Average power computed from the coefficients (Parseval's theorem)."""
    return float(a0 ** 2 + 0.5 * np.sum(a[1:] ** 2 + b[1:] ** 2))


# --- error / convergence studies -------------------------------------------
ERROR_N_VALUES = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200]
OVERSHOOT_N_VALUES = [1, 3, 5, 9, 15, 25, 51, 101, 201]
GIBBS_LIMIT_PERCENT = 8.949          # (Si(pi)/pi - 1/2) * 100


def rms_error_curve(kind, amp, n_values, points=4000):
    """RMS difference between the ideal waveform and its N-term series."""
    t = (np.arange(points) + 0.5) / points        # one period, f0 = 1 Hz
    ideal = ideal_waveform(kind, t, 1.0, amp)
    errors = []
    for n in n_values:
        a0, a, b = fourier_coefficients(kind, amp, n)
        x = synthesize(t, 1.0, a0, a, b)
        errors.append(np.sqrt(np.mean((x - ideal) ** 2)))
    return np.array(errors)


def convergence_rate(n_values, errors):
    """Slope of log(error) vs log(N) over the larger N values."""
    n = np.array(n_values, dtype=float)[-6:]
    e = np.asarray(errors)[-6:]
    return float(np.polyfit(np.log(n), np.log(e), 1)[0])


def gibbs_overshoot_curve(amp, n_values, points=20000):
    """Peak overshoot of the square-wave series as % of the jump (2A)."""
    t = (np.arange(points) + 0.5) / points
    out = []
    for n in n_values:
        a0, a, b = fourier_coefficients("square", amp, n)
        x = synthesize(t, 1.0, a0, a, b)
        out.append((x.max() - amp) / (2 * amp) * 100.0)
    return np.array(out)


# ---------------------------------------------------------------------------
# 3. Plot panels (each draws on a given Matplotlib axis)
# ---------------------------------------------------------------------------
def style_axis(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)


def panel_synthesis(ax, kind, amp, f0, n_harm, n_periods=2):
    """Ideal waveform vs. its N-harmonic Fourier synthesis."""
    t, _ = make_time_axis(f0, n_harm, n_periods)
    a0, a, b = fourier_coefficients(kind, amp, n_harm)
    ax.plot(t, ideal_waveform(kind, t, f0, amp), "--", color=C_IDEAL, lw=1.4,
            label="Ideal waveform")
    ax.plot(t, synthesize(t, f0, a0, a, b), color=C_SYNTH, lw=1.8,
            label=f"Fourier series (N = {n_harm})")
    style_axis(ax, f"{WAVEFORMS[kind]}: ideal vs. synthesized",
               "Time (s)", "Amplitude")
    ax.legend(loc="upper right", fontsize=8)


def panel_gibbs(ax, kind, amp, f0, n_list, n_periods=2):
    """Same waveform synthesized with several different harmonic counts."""
    t, _ = make_time_axis(f0, max(n_list), n_periods)
    ax.plot(t, ideal_waveform(kind, t, f0, amp), "--", color=C_IDEAL, lw=1.3,
            label="Ideal")
    colors = plt.get_cmap("viridis")(np.linspace(0.1, 0.85, len(n_list)))
    for n, color in zip(n_list, colors):
        a0, a, b = fourier_coefficients(kind, amp, n)
        ax.plot(t, synthesize(t, f0, a0, a, b), color=color, lw=1.2,
                label=f"N = {n}")
    style_axis(ax, f"{WAVEFORMS[kind]}: effect of the number of harmonics",
               "Time (s)", "Amplitude")
    ax.legend(loc="upper right", fontsize=8, ncol=2)


def panel_components(ax, kind, amp, f0, n_show=4, n_periods=2):
    """The first few non-zero harmonics and their running sum."""
    a0, a, b = fourier_coefficients(kind, amp, 30)
    used = [k for k in range(1, len(a)) if a[k] != 0 or b[k] != 0][:n_show]
    t, _ = make_time_axis(f0, 30, n_periods)
    w0 = 2 * np.pi * f0
    total = np.full(t.shape, a0)
    if a0 != 0:
        ax.plot(t, np.full(t.shape, a0), ":", color="gray", lw=1,
                label=f"DC = {a0:.3f}")
    colors = plt.get_cmap("plasma")(np.linspace(0.1, 0.75, len(used)))
    for k, color in zip(used, colors):
        term = a[k] * np.cos(k * w0 * t) + b[k] * np.sin(k * w0 * t)
        total += term
        ax.plot(t, term, color=color, lw=1, alpha=0.9, label=f"Harmonic k = {k}")
    ax.plot(t, total, color=C_IDEAL, lw=2.2, label="Sum of terms shown")
    style_axis(ax, f"{WAVEFORMS[kind]}: building the signal harmonic by harmonic",
               "Time (s)", "Amplitude")
    ax.legend(loc="upper right", fontsize=8, ncol=2)


def panel_signal(ax, t, x, title):
    """Plain time-domain plot of a signal."""
    ax.plot(t, x, color=C_SYNTH, lw=1.6)
    style_axis(ax, title, "Time (s)", "Amplitude")


def panel_spectrum(ax, a0, a, b, f0, n_periods=4, title="Amplitude spectrum (FFT)"):
    """FFT of the synthesized signal (bars) vs. theoretical c_k (red x)."""
    n_harm = len(a) - 1
    t, fs = make_time_axis(f0, n_harm, n_periods)
    x = synthesize(t, f0, a0, a, b)
    freqs, spec = amplitude_spectrum(x, fs)
    c = harmonic_amplitudes(a0, a, b)

    f_max = (n_harm + 1) * f0
    show = freqs <= f_max
    ax.vlines(freqs[show], 0, spec[show], colors=C_FFT, lw=2.2)
    visible = show & (spec > 1e-9)
    ax.plot(freqs[visible], spec[visible], "o", color=C_FFT, ms=4,
            label="FFT (measured)")
    ks = np.where(c > 1e-9)[0]
    ax.plot(ks * f0, c[ks], "x", color=C_THEORY, ms=7, mew=1.6,
            label="Theory $c_k$")
    ax.set_xlim(-0.5 * f0, f_max)
    ax.set_ylim(bottom=0)
    style_axis(ax, title, "Frequency (Hz)", "Amplitude")
    ax.legend(loc="upper right", fontsize=8)
    return freqs, spec


def panel_spectra_compare(ax, amp=1.0, n_show=9):
    """Harmonic amplitudes of square / sawtooth / triangle waves side by side."""
    kinds = ["square", "sawtooth", "triangle"]
    k = np.arange(1, n_show + 1)
    width = 0.27
    for i, kind in enumerate(kinds):
        a0, a, b = fourier_coefficients(kind, amp, n_show)
        c = harmonic_amplitudes(a0, a, b)[1:]
        ax.bar(k + (i - 1) * width, c, width, color=KIND_COLORS[kind],
               label=WAVEFORMS[kind])
    ax.set_xticks(k)
    style_axis(ax, "Harmonic amplitudes: square vs. sawtooth vs. triangle",
               "Harmonic number k", "Amplitude $c_k$ (A = 1)")
    ax.legend(fontsize=8)


def panel_error(ax, amp=1.0):
    """RMS approximation error vs. number of harmonics (log-log)."""
    for kind in WAVEFORMS:
        err = np.maximum(rms_error_curve(kind, amp, ERROR_N_VALUES), 1e-12)
        ax.loglog(ERROR_N_VALUES, err, "o-", ms=4, lw=1.4,
                  color=KIND_COLORS[kind], label=WAVEFORMS[kind])
    style_axis(ax, "RMS approximation error vs. number of harmonics",
               "Number of harmonics N", "RMS error")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)


def panel_overshoot(ax, amp=1.0):
    """Gibbs overshoot of the square wave vs. number of harmonics."""
    over = gibbs_overshoot_curve(amp, OVERSHOOT_N_VALUES)
    ax.semilogx(OVERSHOOT_N_VALUES, over, "o-", color=C_SYNTH, lw=1.6, ms=5,
                label="Measured peak overshoot")
    ax.axhline(GIBBS_LIMIT_PERCENT, color=C_THEORY, ls="--", lw=1.3,
               label=f"Gibbs limit ({GIBBS_LIMIT_PERCENT:.2f} %)")
    ax.set_ylim(0, max(over) * 1.15)
    style_axis(ax, "Gibbs phenomenon: overshoot does not vanish",
               "Number of harmonics N", "Overshoot (% of jump)")
    ax.legend(fontsize=8)


# ---------------------------------------------------------------------------
# 4. Figures built from the panels
# ---------------------------------------------------------------------------
def build_dashboard(amp=1.0, f0=5.0):
    """Six-panel summary figure (saved as output_graph.png)."""
    fig, axes = plt.subplots(3, 2, figsize=(15, 13), layout="constrained")
    panel_gibbs(axes[0, 0], "square", amp, f0, [3, 9, 49])
    panel_components(axes[0, 1], "square", amp, f0, n_show=4)
    a0, a, b = fourier_coefficients("square", amp, 25)
    panel_spectrum(axes[1, 0], a0, a, b, f0, n_periods=4,
                   title="Square wave (N = 25): FFT spectrum vs. theory")
    panel_spectra_compare(axes[1, 1], amp)
    panel_error(axes[2, 0], amp)
    panel_overshoot(axes[2, 1], amp)
    fig.suptitle("Fourier Series Synthesizer & Spectrum Analyzer - Summary "
                 f"(A = {amp:g}, f0 = {f0:g} Hz)", fontsize=15, fontweight="bold")
    return fig


# ---------------------------------------------------------------------------
# 5. Console helpers (input validation, tables)
# ---------------------------------------------------------------------------
def ask_float(prompt, default, gt=None):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return float(default)
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if gt is not None and value <= gt:
            print(f"  Value must be greater than {gt}.")
            continue
        return value


def ask_int(prompt, default, ge=None, le=None):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return int(default)
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if ge is not None and value < ge:
            print(f"  Value must be at least {ge}.")
            continue
        if le is not None and value > le:
            print(f"  Value must be at most {le}.")
            continue
        return value


def ask_waveform():
    kinds = list(WAVEFORMS)
    print("\nSelect a waveform:")
    for i, kind in enumerate(kinds, 1):
        print(f"  {i}. {WAVEFORMS[kind]}")
    choice = ask_int("Choice", 1, ge=1, le=len(kinds))
    return kinds[choice - 1]


def ask_number_list(prompt, default, as_int=True):
    """Read a list of numbers separated by spaces and/or commas."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or default
        try:
            parts = raw.replace(",", " ").split()
            values = [int(p) if as_int else float(p) for p in parts]
        except ValueError:
            print("  Please enter numbers separated by spaces or commas.")
            continue
        if not values:
            print("  Please enter at least one value.")
            continue
        if as_int and min(values) < 1:
            print("  All values must be at least 1.")
            continue
        return values


def print_coefficients(kind, amp, n_harm, limit=8):
    a0, a, b = fourier_coefficients(kind, amp, n_harm)
    print(f"\nFourier coefficients - {WAVEFORMS[kind]} (A = {amp:g})")
    print(f"  a0 (DC term) = {a0:.6f}")
    print(f"  {'k':>3} {'a_k':>12} {'b_k':>12} {'c_k':>12}")
    shown = 0
    for k in range(1, n_harm + 1):
        if a[k] != 0 or b[k] != 0:
            print(f"  {k:>3} {a[k]:>12.6f} {b[k]:>12.6f} {np.hypot(a[k], b[k]):>12.6f}")
            shown += 1
            if shown == limit:
                break


def print_spectrum_table(a0, a, b, freqs, spec, f0, n_periods, limit=10):
    c = harmonic_amplitudes(a0, a, b)
    print("\nTheory vs. FFT (first non-zero components)")
    print(f"  {'k':>3} {'f (Hz)':>9} {'Theory':>11} {'FFT':>11} {'|Error|':>11}")
    shown = 0
    for k in range(0, len(c)):
        if c[k] > 1e-9:
            measured = spec[k * n_periods]
            print(f"  {k:>3} {k * f0:>9.2f} {c[k]:>11.6f} {measured:>11.6f} "
                  f"{abs(c[k] - measured):>11.2e}")
            shown += 1
            if shown == limit:
                break
    worst = max(abs(c[k] - spec[k * n_periods]) for k in range(len(c)))
    print(f"  Largest |theory - FFT| over all harmonics: {worst:.2e}")


def maybe_save(fig):
    name = input("Save this figure as PNG? Enter a file name or press Enter to skip: ").strip()
    if name:
        if not name.lower().endswith(".png"):
            name += ".png"
        fig.savefig(name, dpi=200)
        print(f"  Saved -> {name}")


def show_figure(fig):
    maybe_save(fig)
    plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Menu actions
# ---------------------------------------------------------------------------
def action_synthesize():
    kind = ask_waveform()
    amp = ask_float("Amplitude A", 1.0, gt=0)
    f0 = ask_float("Fundamental frequency f0 (Hz)", 5.0, gt=0)
    n_harm = ask_int("Number of harmonics N", 10, ge=1, le=500)
    print_coefficients(kind, amp, n_harm)
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), layout="constrained")
    panel_synthesis(axes[0], kind, amp, f0, n_harm)
    panel_components(axes[1], kind, amp, f0, n_show=4)
    show_figure(fig)


def action_gibbs():
    kind = ask_waveform()
    amp = ask_float("Amplitude A", 1.0, gt=0)
    f0 = ask_float("Fundamental frequency f0 (Hz)", 5.0, gt=0)
    n_list = ask_number_list("Harmonic counts to compare", "3, 9, 49")
    if max(n_list) > 500:
        print("  Limiting to 500 harmonics.")
        n_list = [min(n, 500) for n in n_list]
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    panel_gibbs(ax, kind, amp, f0, n_list)
    show_figure(fig)


def action_spectrum():
    kind = ask_waveform()
    amp = ask_float("Amplitude A", 1.0, gt=0)
    f0 = ask_float("Fundamental frequency f0 (Hz)", 5.0, gt=0)
    n_harm = ask_int("Number of harmonics N", 25, ge=1, le=500)
    n_periods = ask_int("Number of periods to analyze", 4, ge=1, le=50)

    a0, a, b = fourier_coefficients(kind, amp, n_harm)
    t, fs = make_time_axis(f0, n_harm, n_periods)
    x = synthesize(t, f0, a0, a, b)
    freqs, spec = amplitude_spectrum(x, fs)

    print_spectrum_table(a0, a, b, freqs, spec, f0, n_periods)
    p_t, p_f = power_time(x), power_freq(a0, a, b)
    print("\nParseval's theorem (average power)")
    print(f"  Time domain      mean(x^2)                  = {p_t:.8f}")
    print(f"  Frequency domain a0^2 + sum(c_k^2)/2        = {p_f:.8f}")

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), layout="constrained")
    show_n = min(len(t), 2 * (len(t) // n_periods))
    panel_signal(axes[0], t[:show_n], x[:show_n],
                 f"{WAVEFORMS[kind]} synthesized with N = {n_harm} harmonics")
    panel_spectrum(axes[1], a0, a, b, f0, n_periods,
                   title="Amplitude spectrum: FFT vs. theory")
    show_figure(fig)


def action_error():
    amp = ask_float("Amplitude A", 1.0, gt=0)
    print("\nRMS error convergence  (error ~ N^slope, estimated for large N)")
    for kind in WAVEFORMS:
        err = rms_error_curve(kind, amp, ERROR_N_VALUES)
        slope = convergence_rate(ERROR_N_VALUES, np.maximum(err, 1e-12))
        print(f"  {WAVEFORMS[kind]:<26} slope = {slope:6.2f}")
    over = gibbs_overshoot_curve(amp, OVERSHOOT_N_VALUES)
    print("\nGibbs overshoot of the square wave (% of the jump 2A)")
    for n, o in zip(OVERSHOOT_N_VALUES, over):
        print(f"  N = {n:>4}  overshoot = {o:6.3f} %")
    print(f"  Theoretical limit as N -> infinity: {GIBBS_LIMIT_PERCENT:.3f} %")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), layout="constrained")
    panel_error(axes[0], amp)
    panel_overshoot(axes[1], amp)
    show_figure(fig)


def action_custom():
    f0 = ask_float("Fundamental frequency f0 (Hz)", 5.0, gt=0)
    dc = ask_float("DC offset", 0.0)
    amps = ask_number_list(
        "Amplitudes of sine harmonics k = 1, 2, 3, ... (space/comma separated)",
        "1 0 0.333 0 0.2", as_int=False)
    if len(amps) > 200:
        print("  Using the first 200 harmonics only.")
        amps = amps[:200]
    n_harm = len(amps)
    a = np.zeros(n_harm + 1)
    b = np.zeros(n_harm + 1)
    b[1:] = amps
    n_periods = 4
    t, fs = make_time_axis(f0, n_harm, n_periods)
    x = synthesize(t, f0, dc, a, b)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), layout="constrained")
    show_n = 2 * (len(t) // n_periods)
    panel_signal(axes[0], t[:show_n], x[:show_n], "Custom synthesized signal")
    panel_spectrum(axes[1], dc, a, b, f0, n_periods,
                   title="Spectrum of the custom signal")
    show_figure(fig)


def action_dashboard():
    name = input("Output file name [output_graph.png]: ").strip() or "output_graph.png"
    if not name.lower().endswith(".png"):
        name += ".png"
    fig = build_dashboard()
    fig.savefig(name, dpi=200)
    print(f"  Saved -> {name}")
    plt.show()
    plt.close(fig)


MENU = """
==============================================================
      FOURIER SERIES SYNTHESIZER & SPECTRUM ANALYZER
==============================================================
  1. Synthesize a waveform (ideal vs. Fourier series)
  2. Gibbs phenomenon (compare different numbers of harmonics)
  3. Spectrum analyzer (FFT vs. theoretical coefficients)
  4. Error analysis (RMS error & Gibbs overshoot)
  5. Custom harmonic synthesizer
  6. Generate the complete dashboard (output_graph.png)
  0. Exit
--------------------------------------------------------------"""

ACTIONS = {
    "1": action_synthesize,
    "2": action_gibbs,
    "3": action_spectrum,
    "4": action_error,
    "5": action_custom,
    "6": action_dashboard,
}


def run_menu():
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please enter a number from 0 to 6.")
            continue
        try:
            action()
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Fourier Series Synthesizer & Spectrum Analyzer")
    parser.add_argument("--demo", action="store_true",
                        help="generate the summary dashboard image and exit")
    parser.add_argument("--output", default="output_graph.png",
                        help="file name used with --demo (default: output_graph.png)")
    args = parser.parse_args()

    if args.demo:
        fig = build_dashboard()
        fig.savefig(args.output, dpi=200)
        print(f"Saved -> {args.output}")
        plt.close(fig)
    else:
        try:
            run_menu()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")


if __name__ == "__main__":
    main()
