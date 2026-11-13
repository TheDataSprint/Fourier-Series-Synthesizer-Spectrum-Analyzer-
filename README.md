Fourier Series Synthesizer and Spectrum Analyzer
A Python 3 command-line application that demonstrates how periodic signals can be represented as sums of sinusoidal harmonics. It generates standard waveforms, synthesizes finite Fourier-series approximations, and displays the time-domain waveform, amplitude spectrum, and phase spectrum.
Project overview
The project connects the mathematical ideas in Signals and Systems with numerical computation and visualization. Users can select a sine, square, triangle, or sawtooth wave; choose its peak amplitude, fundamental frequency, and number of harmonics; and observe how the harmonic terms build the waveform. A custom-coefficient mode is also provided.
The program uses NumPy for numerical calculations and Matplotlib for plotting. It does not require SciPy or a graphical application framework.
Problem statement
A periodic signal can often be described by a Fourier series, but the relationship between its time-domain shape and its frequency components can be difficult to understand from equations alone. This project provides a small interactive tool that calculates the Fourier coefficients and visualizes the resulting waveform and spectrum. It also makes the effect of a finite number of harmonics visible.
Objectives
Generate four commonly studied periodic signals.
Calculate their trigonometric Fourier-series coefficients.
Reconstruct a signal using a user-selected finite number of harmonics.
Support user-entered Fourier coefficients.
Display harmonic frequencies, peak amplitudes, and phases.
Save a labelled three-panel graph for demonstration and reporting.
Features
Standard signal generation: sine, square, triangle, and sawtooth waves.
Fourier synthesis: reconstructs the selected waveform using the requested number of terms.
Custom mode: accepts a0, an, and bn values directly.
Spectrum analysis: reports each harmonic's frequency, cosine coefficient, sine coefficient, peak amplitude, and phase.
Three-panel plot: time-domain waveform, amplitude spectrum, and phase spectrum.
Demo mode: --demo produces a fixed example without asking for input.
Input validation: rejects invalid menu choices, non-numeric values, non-finite values, and out-of-range harmonic counts.
Technologies used
Technology
Purpose
Python 3
Application logic and command-line interface
NumPy
Arrays, trigonometric operations, and coefficient calculations
Matplotlib
Time-domain and frequency-domain visualizations
Mathematical background
For a continuous-time periodic signal with period T, the fundamental frequency is
[ f_0=\frac{1}{T}, \qquad \omega_0=2\pi f_0. ]
The trigonometric Fourier series used by this program is
[ x(t)=\frac{a_0}{2}+\sum_{n=1}^{\infty}\left[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)\right]. ]
For a finite synthesis, the sum is stopped at the selected harmonic count N:
[ x_N(t)=\frac{a_0}{2}+\sum_{n=1}^{N}\left[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)\right]. ]
The coefficient definitions over any complete period are
[ a_0=\frac{2}{T}\int_{t_0}^{t_0+T}x(t),dt, ]
[ a_n=\frac{2}{T}\int_{t_0}^{t_0+T}x(t)\cos(n\omega_0t),dt, \qquad b_n=\frac{2}{T}\int_{t_0}^{t_0+T}x(t)\sin(n\omega_0t),dt. ]
Coefficient convention: a0 is twice the DC value, because the series contains a0/2. an multiplies the cosine term and bn multiplies the sine term. The peak amplitude of harmonic n is
[ R_n=\sqrt{a_n^2+b_n^2}. ]
The program defines phase by
[ a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t) =R_n\cos(n\omega_0t-\phi_n), ]
so
[ \phi_n=\operatorname{atan2}(b_n,a_n). ]
The phase is displayed in degrees in the interval [-180, 180]. Phase is undefined for a zero-amplitude harmonic. The DC term is shown at 0 Hz in the amplitude spectrum; it has no harmonic phase.
Standard signal definitions and coefficients
A is the peak amplitude and theta = omega0*t. All four standard signals are centered around zero, so a0 = 0 and every an = 0.
Signal
Definition / non-zero sine coefficients
Sine
x(t) = A sin(theta); b1 = A, all other bn = 0
Square
x(t) = A sign(sin(theta)); bn = 4A/(n*pi) for odd n, otherwise 0
Triangle
x(t) = (2A/pi) asin(sin(theta)); bn = (8A/(pi^2*n^2)) (-1)^((n-1)/2) for odd n, otherwise 0
Sawtooth
A rising ramp from -A to +A over each period, with its phase wrapped to [-pi, pi); bn = (2A/(n*pi)) (-1)^(n+1)
The square wave contains odd harmonics whose magnitudes decrease in proportion to 1/n. The triangle wave contains odd harmonics that decrease in proportion to 1/n^2. The sawtooth wave contains all integer harmonics with magnitudes decreasing in proportion to 1/n. The sine wave contains only its fundamental component.
Project folder structure
Fourier-Series-Synthesizer-Spectrum-Analyzer/
|
|-- PROJECT_REPORT.pdf
|-- README.md
|-- output_graph.png
|-- fourier_synthesizer.py
`-- requirements.txt
Installation
Install Python 3.9 or newer from python.org. During Windows installation, enable Add Python to PATH.
Download or clone this project folder.
Open Command Prompt, PowerShell, or a terminal.
Change to the project directory. For example:
cd Fourier-Series-Synthesizer-Spectrum-Analyzer
(Recommended) Create and activate a virtual environment:
Windows Command Prompt
python -m venv .venv
.venv\Scripts\activate
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Install the required packages:
python -m pip install -r requirements.txt
How to run the project
Interactive menu
Run:
python fourier_synthesizer.py
Choose option 1 to create a standard signal, option 2 to enter custom coefficients, or option 3 to exit. For a standard signal, enter the peak amplitude, fundamental frequency in hertz, and harmonic count (1 to 100). The graph is saved beside the Python file as output_graph.png and is also displayed in an interactive window.
Non-interactive demonstration mode
Run:
python fourier_synthesizer.py --demo
This creates a square wave with peak amplitude 1, fundamental frequency 5 Hz, and 15 harmonics. It saves the output graph and exits without requesting any input or opening a plot window.
Example usage
For example, select:
Signal: Square wave
Peak amplitude: 1
Fundamental frequency: 5 Hz
Number of harmonics: 15
The program prints the coefficient table. The harmonic frequencies are 5, 10, 15, ... Hz. For this centered square wave, only odd harmonics have non-zero coefficients, and their phases are +90 degrees under the phase convention defined above.
Graph demonstration
The three panels show (1) the ideal waveform and its finite Fourier approximation, (2) the peak amplitude of the DC and harmonic components, and (3) the phase of non-zero harmonics.
�
The included image is generated by the program's --demo mode. Running either mode again overwrites output_graph.png with the latest result.
Expected output
A console table containing n, harmonic frequency in Hz, an, bn, harmonic peak amplitude, and phase in degrees.
A saved PNG containing the time-domain waveform, amplitude spectrum, and phase spectrum.
In interactive mode, a Matplotlib window showing the same graph.
For a square wave, adding more odd harmonics makes the approximation closer to the ideal flat levels and sharper transitions. Oscillations near discontinuities remain; this is the Gibbs phenomenon. Increasing the number of terms narrows the region of the oscillation, but does not remove its characteristic overshoot at a jump.
Learning outcomes
After exploring the project, a student should be able to:
Relate the period, fundamental frequency, and fundamental angular frequency.
Interpret a0, an, and bn in the trigonometric Fourier series.
Explain how harmonics combine to form a periodic waveform.
Read amplitude and phase spectra.
Recognize the effect of truncating a Fourier series and describe the Gibbs phenomenon.
Use NumPy and Matplotlib to implement and visualize mathematical models.
Future improvements
Possible extensions include numerical coefficient estimation from sampled data, user-controlled phase shifts, frequency-domain export, adjustable time windows, and a graphical user interface. These are not required for the current command-line implementation.
References
A. V. Oppenheim, A. S. Willsky, and S. H. Nawab, Signals and Systems, 2nd ed., Prentice Hall, 1997.
B. P. Lathi and R. A. Green, Linear Systems and Signals, 3rd ed., Oxford University Press, 2018.
NumPy documentation, https://numpy.org/doc/.
Matplotlib documentation, https://matplotlib.org/stable/.
