import tkinter as tk
from math import pi, sqrt, cos, sin, acos
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate impedance, current, power, and other parameters
def calculate():
    try:
        # Given values
        R = float(entry_R.get())  # User input for Resistor (Ω)
        L = 16e-3  # Inductor value (16 mH = 16 * 10^-3 H)
        C = 150e-6  # Capacitor value (150 µF = 150 * 10^-6 F)
        V = 230  # Voltage (V)
        f = 50  # Frequency (Hz)

        # Calculate reactance
        XL = 2 * pi * f * L  # Inductive reactance
        XC = 1 / (2 * pi * f * C)  # Capacitive reactance

        # Calculate impedance (Z)
        Z = sqrt(R**2 + (XL - XC)**2)
        
        # Calculate current (I)
        I = V / Z
        
        # Power Factor (cos(φ)) = R / Z
        power_factor = R / Z
        
        # Active Power (P)
        P = V * I * power_factor
        
        # Reactive Power (Q)
        Q = V * I * sqrt(1 - power_factor**2)
        
        # Apparent Power (S)
        S = V * I
        
        # Update output labels
        label_result.config(text=f"Impedance: {Z:.2f} Ω\nCurrent: {I:.2f} A\n"
                                f"Power Factor: {power_factor:.2f}\nPower: {P:.2f} W\n"
                                f"Reactive Power: {Q:.2f} VAR\nApparent Power: {S:.2f} VA")
        
        # Plotting the waveforms and vector diagram
        plot_waveforms(V, I, f, Z, R)
        plot_vector_diagram(V, R, XL - XC, Z, power_factor)

    except ValueError:
        label_result.config(text="Please enter valid numeric values.")

# Function to plot voltage, current, and power waveforms
def plot_waveforms(V, I, f, Z, R):
    t = np.linspace(0, 0.1, 1000)  # Time array for one cycle (in seconds)
    voltage_waveform = V * np.sin(2 * pi * f * t)  # Voltage waveform (sinusoidal)
    current_waveform = (V / Z) * np.sin(2 * pi * f * t - np.arccos(R / Z))  # Current waveform
    power_waveform = voltage_waveform * current_waveform  # Instantaneous power
    
    # Plotting
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))

    # Voltage waveform
    ax[0].plot(t, voltage_waveform, label="Voltage (V)", color='b')
    ax[0].set_title('Voltage vs Time')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Voltage (V)')
    ax[0].grid(True)

    # Current waveform
    ax[1].plot(t, current_waveform, label="Current (I)", color='g')
    ax[1].set_title('Current vs Time')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Current (A)')
    ax[1].grid(True)

    # Power waveform
    ax[2].plot(t, power_waveform, label="Instantaneous Power (P)", color='r')
    ax[2].set_title('Power vs Time')
    ax[2].set_xlabel('Time (s)')
    ax[2].set_ylabel('Power (W)')
    ax[2].grid(True)

    plt.tight_layout()
    plt.show()

# Function to plot vector diagram
def plot_vector_diagram(V, R, X, Z, power_factor):
    # Calculate phase angle (φ)
    phi = acos(power_factor)  # Phase angle between current and voltage

    # Create the figure and axis for the vector diagram
    fig, ax = plt.subplots(figsize=(6, 6))

    # Voltage vector (V) - along the horizontal axis (Real axis)
    ax.quiver(0, 0, V, 0, angles='xy', scale_units='xy', scale=1, color='b', label="Voltage (V)")

    # Current vector (I) - lagging by phase angle φ
    ax.quiver(0, 0, V * cos(phi), V * sin(phi), angles='xy', scale_units='xy', scale=1, color='g', label="Current (I)")

    # Impedance vector (Z) - combination of R and X (R along the real axis and X along the imaginary axis)
    ax.quiver(0, 0, R, X, angles='xy', scale_units='xy', scale=1, color='r', label="Impedance (Z)")

    # Set axis limits and labels
    ax.set_xlim(-1.5 * V, 1.5 * V)
    ax.set_ylim(-1.5 * V, 1.5 * V)
    ax.set_xlabel("Real (Re)")
    ax.set_ylabel("Imaginary (Im)")
    ax.set_title("Vector Diagram of Series RLC Circuit")

    # Add grid, legend, and origin
    ax.grid(True)
    ax.legend()
    ax.axhline(0, color='black',linewidth=1)
    ax.axvline(0, color='black',linewidth=1)

    # Show the plot
    plt.show()

# Set up the GUI
root = tk.Tk()
root.title("Series RLC Circuit Simulator")

# Labels and entries for inputs
tk.Label(root, text="Resistor (R) in Ohms:").grid(row=1, column=0)
entry_R = tk.Entry(root)
entry_R.grid(row=1, column=1)

# Calculate button
btn_calculate = tk.Button(root, text="Calculate", command=calculate)
btn_calculate.grid(row=2, columnspan=2)

# Label to display results
label_result = tk.Label(root, text="Results will be shown here", justify="left")
label_result.grid(row=3, columnspan=2)

# Run the Tkinter loop
root.mainloop()
