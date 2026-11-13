# Fourier Series Synthesizer & Spectrum Analyzer

A Python-based implementation of Fourier Series concepts, designed to generate periodic signals, calculate Fourier coefficients, reconstruct waveforms, and analyze frequency components through numerical computation and visualization.

The project provides an interactive, menu-driven environment for understanding harmonic synthesis and the relationship between time-domain signals and frequency-domain representations.

## Overview

Fourier Series is an important mathematical concept in Signals and Systems. It represents periodic signals as combinations of sinusoidal harmonics.

This project demonstrates how periodic waveforms can be reconstructed using a finite number of harmonics. Users can generate standard signals, enter custom Fourier coefficients, and observe their corresponding waveforms and spectra.

## Key Features

**1. Signal Generation**

Generation of commonly studied periodic signals:

- Sine Wave
- Square Wave
- Triangle Wave
- Sawtooth Wave

**2. Fourier Series Synthesis**

Reconstruction of periodic signals using a user-selected number of harmonics.

**3. Custom Coefficient Mode**

Supports user-defined Fourier coefficients (`a0`, `an`, and `bn`).

**4. Spectrum Analysis**

Calculation and visualization of:

- Harmonic frequencies
- Cosine and sine coefficients
- Peak amplitudes
- Phase angles

**5. Graphical Visualization**

Matplotlib-based visualization of:

- Time-domain waveform
- Amplitude spectrum
- Phase spectrum

**6. Additional Features**

- Interactive command-line interface.
- Automatic graph generation and saving.
- Demo mode using `--demo`.
- Input validation for reliable execution.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| NumPy | Numerical computation and coefficient calculations |
| Matplotlib | Signal visualization and graph plotting |

## Mathematical Concepts Implemented

The project demonstrates the trigonometric Fourier Series:

$$
x(t)=\frac{a_0}{2}+\sum_{n=1}^{\infty}\left[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)\right]
$$

Fundamental frequency:

$$
f_0=\frac{1}{T}, \qquad \omega_0=2\pi f_0
$$

Harmonic peak amplitude:

$$
R_n=\sqrt{a_n^2+b_n^2}
$$

Phase angle:

$$
\phi_n=\mathrm{atan2}(b_n,a_n)
$$

The phase convention is defined by:

$$
a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)
=R_n\cos(n\omega_0t-\phi_n)
$$

The phase is undefined for a zero-amplitude harmonic.

## Gibbs Phenomenon

The Gibbs phenomenon occurs when a periodic signal containing discontinuities, such as a square wave, is approximated using a finite number of Fourier harmonics.

Oscillations and overshoots appear near the discontinuities. Increasing the number of harmonics improves the approximation and narrows the oscillation region, but the characteristic overshoot does not completely disappear.

This project demonstrates the Gibbs phenomenon through finite Fourier Series reconstruction.

## Project Structure

```text
Fourier-Series-Synthesizer-Spectrum-Analyzer/
│
├── PROJECT_REPORT.pdf
├── README.md
├── output_graph.png
├── fourier_synthesizer.py
└── requirements.txt
```

## Installation and Setup

**Prerequisites**

- Python 3.9 or higher
- pip package manager

**Step 1: Clone the Repository**

```bash
git clone <your-repository-url>
```

**Step 2: Navigate to the Project Directory**

```bash
cd Fourier-Series-Synthesizer-Spectrum-Analyzer
```

**Step 3: Install Dependencies**

```bash
python -m pip install -r requirements.txt
```

**Step 4: Run the Program**

```bash
python fourier_synthesizer.py
```

## How to Use

1. Execute the Python program.
2. Select a standard signal or custom coefficient mode.
3. Enter the required amplitude and frequency values.
4. Specify the number of harmonics.
5. View the calculated Fourier coefficients in the terminal.
6. Observe the generated waveform and frequency spectra.
7. Access the automatically saved graph as `output_graph.png`.

**Demo Mode**

Run the following command to generate a predefined example:

```bash
python fourier_synthesizer.py --demo
```

The demo generates a square wave with an amplitude of 1, a fundamental frequency of 5 Hz, and 15 harmonics.

## Sample Output

The program generates a three-panel visualization containing:

- **Time-Domain Waveform:** Compares the ideal waveform with its finite Fourier approximation.
- **Amplitude Spectrum:** Displays the peak amplitudes of DC and harmonic components.
- **Phase Spectrum:** Displays the phase angles of non-zero harmonics.

The generated graph is saved as a PNG image.

![Fourier Series Output](output_graph.png)

## Learning Outcomes

This project provides practical experience in:

- Understanding Fourier Series representation.
- Calculating trigonometric Fourier coefficients.
- Reconstructing signals using harmonics.
- Interpreting amplitude and phase spectra.
- Understanding the Gibbs phenomenon.
- Applying NumPy and Matplotlib to mathematical problems.

## Future Scope

Potential improvements include:

- Fourier Transform and frequency-domain analysis.
- User-controlled phase shifting.
- Numerical coefficient estimation from sampled signals.
- Interactive graphical user interface.
- Frequency-domain data export.

## References

- A. V. Oppenheim, A. S. Willsky, and S. H. Nawab, *Signals and Systems*, 2nd Edition, Prentice Hall, 1997.
- B. P. Lathi and R. A. Green, *Linear Systems and Signals*, 3rd Edition, Oxford University Press, 2018.
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)

## Author

**Prince Yadav**

Developed for academic and educational purposes.
