# Engine Dynamometer Simulation using Python

## Project Overview
This project is a Python-based simulation of a small internal combustion engine dynamometer, replicating key experiments used in engine testing. It models engine performance under various loads, estimates friction power using Willans Line theory, and simulates in-cylinder thermodynamics via pressure–volume (P–V) analysis.

The simulation includes:  
- Engine torque–RPM characteristics  
- Friction torque modeling and estimation  
- Fuel consumption analysis and Brake Specific Fuel Consumption (BSFC) using Willans Line  
- Cylinder pressure modeling over a complete 4-stroke cycle  
- Load response simulations (e.g., uphill load scenario)  

It provides graphical outputs for torque curves, RPM dynamics, torque balance, friction power, and fuel consumption, enabling visualization of engine behavior without physical testing.

## Key Features
- **Engine Performance Simulation:** Models torque and RPM under varying loads.  
- **Friction Power Estimation:** Uses a Willans-type approach to compute friction losses.  
- **Fuel Consumption Analysis:** Generates fuel consumption vs. brake power plots.  
- **Cylinder Thermodynamics:** Simulates intake, compression, combustion, expansion, and exhaust strokes with polytropic processes.  
- **Load Response Testing:** Simulates scenarios such as uphill load with dynamically increasing torque demands.  
- **Plots and Data Visualization:** Generates multiple plots for analysis and comparison.

## Experiments Simulated
- **Uphill Load Simulation:**  
  Simulates engine behavior under gradually increasing load.  
  Outputs: RPM vs Time, Engine Torque vs RPM, Torque Balance vs Time.

- **Friction Power Estimation (Willans Method):**  
  Determines engine friction power via extrapolated brake power vs fuel consumption data.  
  Outputs: Friction Power vs RPM plots.

- **Fuel Consumption Analysis (Willans Line):**  
  Simulates fuel mass flow rate at varying loads.  
  Outputs: Fuel Consumption vs Brake Power, BSFC estimation.

- **Cylinder Pressure Simulation:**  
  Calculates P–V diagram for the engine over a full 4-stroke cycle.  
  Includes intake vacuum, compression, smooth combustion, expansion, and exhaust strokes.

## Technology Stack
- **Language:** Python 3.x  
- **Libraries:**  
  - `numpy` for numerical calculations  
  - `matplotlib` for plotting  
  - `pandas` (optional) for tabular data analysis

## How It Works (Logic Overview)
- **Engine Torque Modeling:**  
  Polynomial function fitted to represent torque vs RPM, accounting for idle, peak torque, and rated power RPM.

- **Friction Modeling:**  
  Quadratic model:  
  friction_torque = C0 + C1 * RPM + C2 * RPM^2  
  Represents bearing friction, piston friction, and pumping losses.

- **RPM Dynamics under Load:**  
  Angular acceleration:  
  alpha = net_torque / I_engine  
  RPM updated using:  
  dRPM/dt = alpha * (60 / 2π)

- **Willans Line Analysis:**  
  Linear regression of fuel consumption vs brake power.  
  Friction power calculated from x-intercept.  
  BSFC derived from slope of the line.

- **Cylinder Pressure Simulation:**  
  Uses slider-crank geometry to compute instantaneous cylinder volume.  
  Pressure computed using polytropic compression/expansion.  
  Combustion modeled with a smooth sigmoid rise to simulate realistic flame propagation.

## Installation

Make sure you have Python 3.8+ installed.

Install required Python libraries via pip:

pip install numpy matplotlib pandas

## Running the Simulation

1. Clone or download the project repository to your local machine.

2. Navigate to the project directory in your terminal or command prompt.

3. Run the main simulation script (replace engine_dynamometer_simulation.py with the actual script name if different):

python engine_dynamometer_simulation.py

4. The program will generate graphical outputs such as torque curves, RPM vs time graphs, friction power plots, fuel consumption graphs, and P–V diagrams.

5. Review the plots to analyze engine performance and characteristics under different simulated conditions.

## Outputs

- Engine torque curve  
- RPM vs Time under load  
- Torque balance (Engine – Friction – Load)  
- Friction power vs RPM (model vs Willans Line)  
- Fuel consumption vs brake power (Willans Line)  
- P–V diagram of the engine cycle  

## Assumptions

- Engine modeled after Honda GX160 small gasoline engine.  
- Friction torque modeled empirically using quadratic approximation.  
- Polytropic compression/expansion used to simulate heat losses.  
- Combustion modeled using simplified sigmoid function for flame propagation.  
- Ignition timing and mechanical efficiency are assumed constant.

## Insights

- Engine RPM drops as load increases; net torque indicates performance limits.  
- Willans Line provides a practical method to estimate friction power and BSFC.  
- Cylinder pressure analysis illustrates realistic combustion and expansion dynamics.

## References

- Heywood, J. B. Internal Combustion Engine Fundamentals, McGraw-Hill, 1988.  
- Cengel, Y. A., Thermodynamics: An Engineering Approach, 9th Edition.  
- Empirical Honda GX160 specifications: Bore 68 mm, Stroke 45 mm, Peak torque 10.3 Nm at 2500 RPM.

## Future Work / Improvements

- Add multi-cylinder engine simulation.  
- Include variable ignition timing and dynamic combustion efficiency.  
- Integrate with GUI for real-time parameter adjustment.  
- Compare simulation results with experimental dynamometer data.

---

Feel free to explore, modify parameters, and extend the simulation to fit your research or educational needs!
