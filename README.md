# Fourier Series Synthesizer & Spectrum Analyzer

A Python-based implementation of Fourier Series concepts, designed to generate periodic signals, reconstruct waveforms using harmonics, analyze frequency components, and visualize the mathematical behavior of periodic signals.

The project provides an interactive, menu-driven environment for exploring Fourier Series, harmonic synthesis, FFT analysis, approximation errors, and the Gibbs phenomenon.

## Overview

Fourier Series is an important mathematical concept in Signals and Systems. It represents periodic signals as combinations of sinusoidal harmonics.

This project demonstrates how different periodic waveforms can be reconstructed using a finite number of harmonics. Users can generate standard signals, analyze their frequency components, compare theoretical Fourier coefficients with FFT results, and study the effect of increasing the number of harmonics.

## Key Features

**1. Signal Generation**

Generation of commonly studied periodic signals:

- Square Wave
- Sawtooth Wave
- Triangle Wave
- Full-Wave Rectified Sine
- Half-Wave Rectified Sine

**2. Fourier Series Synthesis**

Reconstruction of periodic waveforms using a user-selected number of harmonics.

**3. Harmonic Analysis**

Visualization of individual harmonic components and their combined waveform.

**4. Spectrum Analysis**

FFT-based frequency analysis and comparison with theoretical Fourier coefficients.

**5. Error and Convergence Analysis**

Calculation and visualization of RMS approximation error for different harmonic counts.

**6. Gibbs Phenomenon**

Demonstration of overshoot near signal discontinuities and its convergence toward the theoretical Gibbs limit.

**7. Custom Harmonic Synthesizer**

Supports user-defined DC offset and sine-harmonic amplitudes.

**8. Additional Features**

- Interactive command-line interface.
- Automatic graph generation and saving.
- Demo mode using `--demo`.
- Input validation for menu choices and numeric inputs.
- Verification of Parseval's theorem.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| NumPy | Numerical computation, FFT, and coefficient calculations |
| Matplotlib | Signal visualization and graph plotting |

## Mathematical Concepts Implemented

The project uses the trigonometric Fourier Series convention:

$$
x(t)=a_0+\sum_{n=1}^{\infty}
[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]
$$

Fundamental angular frequency:

$$
\omega_0=2\pi f_0
$$

Harmonic amplitude:

$$
c_n=\sqrt{a_n^2+b_n^2}
$$

Average power using Parseval's theorem:

$$
P=a_0^2+\frac{1}{2}
\sum_{n=1}^{\infty}(a_n^2+b_n^2)
$$

Here, `a0` represents the DC component directly.

## Gibbs Phenomenon

The Gibbs phenomenon occurs when a periodic signal containing discontinuities, such as a square wave, is approximated using a finite number of Fourier harmonics.

Oscillations appear near discontinuities. Increasing the number of harmonics improves the approximation, but the characteristic overshoot does not completely disappear.

This project demonstrates the Gibbs phenomenon through waveform reconstruction and a numerical overshoot convergence graph.

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

Run the Python program and select an option from the interactive menu:

1. Synthesize a waveform.
2. Compare different harmonic counts and observe the Gibbs phenomenon.
3. Analyze the frequency spectrum using FFT.
4. Perform RMS error and Gibbs overshoot analysis.
5. Generate a custom harmonic signal.
6. Generate the complete six-panel dashboard.

**Demo Mode**

Run the following command to generate the complete dashboard automatically:

```bash
python fourier_synthesizer.py --demo
```

To specify a custom output filename:

```bash
python fourier_synthesizer.py --demo --output my_graph.png
```

## Sample Output

The program generates a six-panel visualization containing:

- **Fourier Approximation:** Compares the ideal square wave with its Fourier-series approximations.
- **Harmonic Construction:** Shows how individual harmonics combine to build a signal.
- **FFT Spectrum Analysis:** Compares measured FFT amplitudes with theoretical Fourier coefficients.
- **Harmonic Comparison:** Compares square, sawtooth, and triangle wave harmonic amplitudes.
- **RMS Error Analysis:** Shows how approximation error changes with the number of harmonics.
- **Gibbs Phenomenon Analysis:** Demonstrates how the overshoot approaches its theoretical limit.

The generated dashboard is saved as `output_graph.png`.

![Fourier Series Synthesizer Dashboard](output_graph.png)

## Learning Outcomes

This project provides practical experience in:

- Understanding Fourier Series representation.
- Reconstructing periodic signals using harmonics.
- Understanding FFT-based spectrum analysis.
- Comparing theoretical and measured frequency components.
- Calculating RMS approximation errors.
- Verifying Parseval's theorem.
- Understanding the Gibbs phenomenon.
- Applying NumPy and Matplotlib to mathematical problems.

## Future Scope

Potential improvements include:

- Phase spectrum analysis.
- Custom cosine and sine coefficient input.
- Fourier Transform visualization.
- Numerical Fourier coefficient estimation from sampled signals.
- Interactive graphical user interface.
- Exporting frequency-domain data.

## References

- A. V. Oppenheim, A. S. Willsky, and S. H. Nawab, *Signals and Systems*, 2nd Edition, Prentice Hall, 1997.
- B. P. Lathi and R. A. Green, *Linear Systems and Signals*, 3rd Edition, Oxford University Press, 2018.
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)

## Author

**Prince Yadav**

Developed for academic and educational purposes.
