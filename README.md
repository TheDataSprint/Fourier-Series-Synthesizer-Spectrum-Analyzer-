# Fourier Series Synthesizer & Spectrum Analyzer

A Python-based project that demonstrates Fourier Series, harmonic synthesis, signal reconstruction, and frequency spectrum analysis using NumPy and Matplotlib.

The project helps understand how periodic signals are formed by combining sinusoidal harmonics.

## Overview

This project provides an interactive, menu-driven program to generate and analyze different periodic signals.

Users can explore Fourier Series, compare harmonic components, analyze FFT results, and observe the Gibbs phenomenon through graphical visualizations.

## Key Features

**1. Signal Generation**

- Square Wave
- Sawtooth Wave
- Triangle Wave
- Full-Wave Rectified Sine
- Half-Wave Rectified Sine

**2. Fourier Series Synthesis**

Reconstructs periodic signals using different numbers of harmonics.

**3. Spectrum Analysis**

Compares theoretical Fourier coefficients with FFT results.

**4. Error Analysis**

Calculates RMS approximation error and studies signal convergence.

**5. Gibbs Phenomenon**

Visualizes overshoot near signal discontinuities.

**6. Custom Signal Generation**

Allows users to create signals using a DC offset and custom harmonic amplitudes.

**7. Graphical Visualization**

Generates a six-panel dashboard showing signal waveforms, harmonics, spectrum, approximation error, and Gibbs phenomenon.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| NumPy | Numerical calculations and FFT |
| Matplotlib | Graphs and visualization |

## Project Structure

```text
Fourier-Series-Synthesizer-Spectrum-Analyzer/
│
├── PROJECT_REPORT.pdf
├── README.md
├── output_graph[1].png
├── fourier_synthesizer[1].py
└── requirements.txt
```

## Installation and Setup

**1. Clone the Repository**

```bash
git clone <https://github.com/TheDataSprint/Fourier-Series-Synthesizer-Spectrum-Analyzer-.git>
```

**2. Open the Project Folder**

```bash
cd Fourier-Series-Synthesizer-Spectrum-Analyzer
```

**3. Install Dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Run the Program**

```bash
python fourier_synthesizer[1].py
```

## How to Use

Run the program and select an option from the menu:

1. Synthesize a waveform.
2. Explore the Gibbs phenomenon.
3. Analyze the frequency spectrum.
4. Perform error analysis.
5. Generate a custom signal.
6. Generate the complete dashboard.

**Generate Dashboard Directly**

```bash
python fourier_synthesizer[1].py --demo
```

The generated graph is saved as `output_graph[1].png`.

## Sample Output

The project generates a six-panel dashboard containing:

- Fourier Series Approximation
- Harmonic Construction
- FFT Spectrum Analysis
- Harmonic Amplitude Comparison
- RMS Error Analysis
- Gibbs Phenomenon Analysis

## Learning Outcomes

- Understanding Fourier Series and harmonics.
- Signal generation and reconstruction.
- FFT-based frequency analysis.
- RMS error calculation.
- Parseval's theorem.
- Understanding the Gibbs phenomenon.
- Numerical computation and visualization using Python.

## Future Scope

- Fourier Transform visualization.
- Phase spectrum analysis.
- Custom cosine and sine coefficient input.
- Interactive graphical user interface.

## Author

**Prince Yadav**
