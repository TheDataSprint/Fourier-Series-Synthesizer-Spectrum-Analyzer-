# Fourier Series Synthesizer & Spectrum Analyzer

A Python 3 command-line application that demonstrates how periodic signals can be represented as sums of sinusoidal harmonics. It generates standard waveforms, synthesizes finite Fourier-series approximations, and visualizes the time-domain waveform, amplitude spectrum, and phase spectrum.

---

## Overview

Fourier Series is an important mathematical concept in Signals and Systems. It explains how complex periodic signals can be represented as combinations of simple sinusoidal components.

This project provides an interactive Python application that connects theoretical Fourier Series concepts with numerical computation and graphical visualization.

Users can generate different periodic waveforms, calculate Fourier coefficients, reconstruct signals using a selected number of harmonics, and analyze their frequency-domain properties.

The application supports NumPy for numerical calculations and Matplotlib for visualization. It does not require SciPy or a graphical application framework.

## Problem Statement

A periodic signal can often be described using a Fourier series, but understanding the relationship between its time-domain shape and frequency components can be difficult from mathematical equations alone.

This project addresses that problem by providing an interactive tool that calculates Fourier coefficients and visualizes the resulting waveform and spectrum. It also demonstrates how using a finite number of harmonics affects signal reconstruction.

## Objectives

- Generate four commonly studied periodic signals.
- Calculate trigonometric Fourier-series coefficients.
- Reconstruct signals using a user-selected number of harmonics.
- Support user-entered Fourier coefficients.
- Display harmonic frequencies, peak amplitudes, and phases.
- Generate and save labelled graphs for demonstration and reporting.

## Key Features

### 1. Standard Signal Generation

Generate and visualize four commonly used periodic signals:

- Sine wave
- Square wave
- Triangle wave
- Sawtooth wave

### 2. Fourier Series Synthesis

Reconstruct the selected periodic waveform using a finite number of sinusoidal harmonics.

### 3. Custom Coefficient Mode

Enter Fourier-series coefficients directly:

- DC coefficient (`a0`)
- Cosine coefficients (`an`)
- Sine coefficients (`bn`)

### 4. Spectrum Analysis

Calculate and display:

- Harmonic frequencies
- Cosine coefficients
- Sine coefficients
- Harmonic peak amplitudes
- Phase angles in degrees

### 5. Graphical Visualization

Generate a three-panel graph containing:

- Time-domain waveform and Fourier approximation
- Amplitude spectrum
- Phase spectrum

### 6. Demo Mode

Run the application with a predefined example using:

```bash
python fourier_synthesizer.py --demo
```

### 7. Input Validation

The application validates menu choices, numerical inputs, finite values, and harmonic counts to prevent invalid input.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application logic and command-line interface |
| NumPy | Numerical calculations, arrays, and trigonometric operations |
| Matplotlib | Waveform plotting and spectrum visualization |

## Mathematical Background

For a continuous-time periodic signal with period \(T\), the fundamental frequency is:

\[
f_0 = \frac{1}{T}
\]

The fundamental angular frequency is:

\[
\omega_0 = 2\pi f_0
\]

### Trigonometric Fourier Series

The periodic signal can be represented as:

\[
x(t)=\frac{a_0}{2}+
\sum_{n=1}^{\infty}
\left[
a_n\cos(n\omega_0t)+
b_n\sin(n\omega_0t)
\right]
\]

For finite Fourier synthesis, the summation is limited to \(N\) harmonics:

\[
x_N(t)=\frac{a_0}{2}+
\sum_{n=1}^{N}
\left[
a_n\cos(n\omega_0t)+
b_n\sin(n\omega_0t)
\right]
\]

### Fourier Coefficients

The coefficient definitions over one complete period are:

\[
a_0=\frac{2}{T}
\int_{t_0}^{t_0+T}x(t)\,dt
\]

\[
a_n=\frac{2}{T}
\int_{t_0}^{t_0+T}
x(t)\cos(n\omega_0t)\,dt
\]

\[
b_n=\frac{2}{T}
\int_{t_0}^{t_0+T}
x(t)\sin(n\omega_0t)\,dt
\]

**Coefficient convention:** \(a_0\) is twice the DC value because the Fourier series contains \(a_0/2\). The coefficient \(a_n\) multiplies the cosine term, while \(b_n\) multiplies the sine term.

###
