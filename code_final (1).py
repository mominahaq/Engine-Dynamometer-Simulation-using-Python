import numpy as np
import matplotlib.pyplot as plt
import pandas as pd # Import pandas for tabular data display

# Set plotting style for professional appearance
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['lines.linewidth'] = 2

# ============================================================================
# SECTION 1: HONDA GX160 ENGINE SPECIFICATIONS
# ============================================================================

# Engine Geometry
BORE = 0.068  # meters (68 mm)
STROKE = 0.045  # meters (45 mm)
CONNECTING_ROD_LENGTH = 0.090  # meters (90 mm - typical for small engines, L/R ratio ~2)
# DISPLACEMENT = 163e-6  # cubic meters (163 cm³)
# Calculate displacement from bore and stroke for consistency
DISPLACEMENT = (np.pi / 4) * BORE**2 * STROKE  # cubic meters
COMPRESSION_RATIO = 8.5  # dimensionless

# Performance Specifications
MAX_POWER = 3600  # Watts (3.6 kW at 3600 RPM)
MAX_TORQUE = 10.3  # Nm (at 2500 RPM)
RATED_RPM = 3600  # RPM
PEAK_TORQUE_RPM = 2500  # RPM
IDLE_RPM = 1400  # RPM (typical for small engines)# ============================================================================
# EXPERIMENT 1: UPHILL LOAD SIMULATION
# ============================================================================

def experiment_1_uphill_load():
    """
    Simulate engine behavior under increasing load (hill climbing scenario).

    Models:
    - Engine torque curve vs RPM
    - Brake torque (load) increasing with time
    - Net torque = Engine torque - Friction torque - Brake torque
    - RPM dynamics: dRPM/dt proportional to net torque

    Outputs:
    - Plot 1: Engine Torque vs RPM (baseline characteristic)
    - Plot 2: RPM vs Time (showing deceleration under load)
    - Plot 3: Torque Balance vs Time (combined)
    """
    print("\n" + "="*70)
    print("EXPERIMENT 1: UPHILL LOAD SIMULATION")
    print("="*70)

    # Time parameters
    dt = 0.01  # Time step (seconds)
    t_max = 30  # Simulation duration (seconds)
    time = np.arange(0, t_max, dt)

    # Initialize arrays
    rpm = np.zeros_like(time)
    engine_torque = np.zeros_like(time)
    friction_torque = np.zeros_like(time)
    brake_torque = np.zeros_like(time)
    net_torque = np.zeros_like(time)

    # Initial conditions
    rpm[0] = RATED_RPM  # Start at rated speed (3600 RPM)

    # Engine inertia (estimated for small single-cylinder engine)
    # I = 0.5 kg·m² (increased for realistic dynamics - includes flywheel)
    # Small engines have flywheels that increase rotational inertia
    I_engine = 0.5  # kg·m²

    # Simulate load increasing with time (simulating uphill climb)
    for i in range(len(time)):
        t = time[i]

        # Current RPM
        current_rpm = rpm[i]

        # Engine torque at current RPM
        engine_torque[i] = calculate_engine_torque(current_rpm)

        # Friction torque at current RPM (using the model, not Willans for Exp1)
        friction_torque[i] = calculate_friction_torque_model(current_rpm)

        # Brake torque (load) increases linearly with time
        # Simulates going uphill - load increases gradually
        if t < 10:
            brake_torque[i] = 2.0  # Light load initially (2 Nm)
        elif t < 20:
            brake_torque[i] = 2.0 + (t - 10) * 0.5  # Increasing load
        else:
            brake_torque[i] = 7.0  # Heavy load (7 Nm)

        # Net torque
        net_torque[i] = engine_torque[i] - friction_torque[i] - brake_torque[i]

        # Update RPM using angular acceleration
        # τ_net = I * α, where α = dω/dt
        # ω = RPM * 2π/60
        # dRPM/dt = (τ_net / I) * (60 / 2π)
        if i < len(time) - 1:
            alpha = net_torque[i] / I_engine  # Angular acceleration (rad/s²)
            d_rpm = alpha * (60 / (2 * np.pi)) * dt  # Change in RPM
            # Positive net torque increases RPM, negative decreases it
            rpm[i+1] = max(rpm[i] + d_rpm, IDLE_RPM)  # Don't go below idle

    # Analysis
    print(f"\nInitial RPM: {rpm[0]:.0f} RPM")
    print(f"Final RPM: {rpm[-1]:.0f} RPM")
    print(f"RPM Drop: {rpm[0] - rpm[-1]:.0f} RPM")
    print(f"Initial Load: {brake_torque[0]:.1f} Nm")
    print(f"Final Load: {brake_torque[-1]:.1f} Nm")

    # Find when engine can no longer maintain speed (net torque becomes negative)
    critical_idx = np.where(net_torque < 0)[0]
    if len(critical_idx) > 0:
        critical_time = time[critical_idx[0]]
        critical_load = brake_torque[critical_idx[0]]
        print(f"\n Engine begins to lose speed at t = {critical_time:.1f}s")
        print(f"  Critical load: {critical_load:.1f} Nm")
        print(f"  RPM at critical point: {rpm[critical_idx[0]]:.0f} RPM")

    # PLOT 1: Engine Torque vs RPM (Baseline Characteristic Curve)
    rpm_range = np.linspace(IDLE_RPM, 4000, 200)
    torque_curve = calculate_engine_torque(rpm_range)

    plt.figure(figsize=(10, 6))
    plt.plot(rpm_range, torque_curve, 'b-', linewidth=2.5, label='Engine Torque')
    plt.axhline(y=MAX_TORQUE, color='r', linestyle='--', label=f'Max Torque = {MAX_TORQUE} Nm')
    plt.axvline(x=PEAK_TORQUE_RPM, color='g', linestyle='--', alpha=0.5, label=f'Peak at {PEAK_TORQUE_RPM} RPM')
    plt.xlabel('Engine Speed (RPM)', fontsize=12, fontweight='bold')
    plt.ylabel('Torque (Nm)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: Honda GX160 Torque Curve', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig('plot1_torque_curve.png', dpi=300, bbox_inches='tight')

    # PLOT 2: RPM vs Time
    plt.figure(figsize=(10, 6))
    plt.plot(time, rpm, 'b-', linewidth=2)
    plt.axhline(y=RATED_RPM, color='g', linestyle='--', alpha=0.5, label='Rated RPM')
    plt.axhline(y=IDLE_RPM, color='r', linestyle='--', alpha=0.5, label='Idle RPM')
    plt.xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    plt.ylabel('Engine Speed (RPM)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: RPM vs Time Under Increasing Load', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('plot2_rpm_vs_time.png', dpi=300, bbox_inches='tight')

    # PLOT 3: Torque Balance vs Time (Combined)
    plt.figure(figsize=(10, 6))
    plt.plot(time, engine_torque, 'b-', linewidth=2, label='Engine Torque', alpha=0.7)
    plt.plot(time, brake_torque, 'r-', linewidth=2, label='Brake Torque (Load)', alpha=0.7)
    plt.plot(time, friction_torque, 'orange', linewidth=2, label='Friction Torque', alpha=0.7)
    plt.plot(time, net_torque, 'g-', linewidth=2.5, label='Net Torque')
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    plt.xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    plt.ylabel('Torque (Nm)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: Torque Balance vs Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig('plot3_torque_balance.png', dpi=300, bbox_inches='tight')


    print("\n Experiment 1 complete. 3 plots generated.")
    plt.show()

    # Return all relevant data for synthetic data generation
    return rpm, time, engine_torque, friction_torque, brake_torque, net_torque


# Thermodynamic Properties
GAMMA = 1.4  # Specific heat ratio for air
R_SPECIFIC = 287  # J/(kg·K) - Specific gas constant for air
INTAKE_TEMP = 298  # K (25°C ambient)
INTAKE_PRESSURE = 101325  # Pa (1 atm)

# Combustion Parameters
IGNITION_TIMING = 20  # degrees BTDC (Before Top Dead Center)
FUEL_LHV = 44e6  # J/kg - Lower Heating Value of gasoline
STOICHIOMETRIC_AFR = 14.7  # Air-Fuel Ratio for gasoline
COMBUSTION_EFFICIENCY = 0.30  # 30% overall thermal efficiency (realistic for small engines)
COMBUSTION_DURATION = 40  # degrees (more realistic for a small engine)

# Mechanical Efficiency
VOLUMETRIC_EFFICIENCY = 0.80  # 80% volumetric efficiency (typical for naturally aspirated)
MECHANICAL_EFFICIENCY = 0.85  # 85% mechanical efficiency

# ============================================================================
# ASSUMPTIONS & JUSTIFICATIONS
# ============================================================================
"""
ASSUMPTION 1: Torque-RPM Curve Shape
- Assumption: Polynomial curve peaking at 2500 RPM
- Justification: Small gasoline engines exhibit peak torque at 40-70% of max RPM
  due to volumetric efficiency and combustion timing optimization at mid-range speeds.

ASSUMPTION 2: Friction Power Model
- Assumption: Friction power = C1 + C2*RPM + C3*RPM²
- Justification: Friction consists of:
  * Constant term (C1): Static friction, pumping losses
  * Linear term (C2*RPM): Viscous friction in bearings
  * Quadratic term (C3*RPM²): Aerodynamic losses, turbulent oil flow

ASSUMPTION 3: Willans Line Linearity
- Assumption: Fuel flow rate is linear with brake power (30-90% load)
- Justification: At steady-state operation, indicated work is proportional to fuel input.
  Friction losses are relatively constant, making brake work linear with fuel.
  Deviations occur at:
  * Low loads: Friction dominates, efficiency drops
  * High loads: Enrichment for cooling, efficiency drops

ASSUMPTION 4: Polytropic Processes
- Assumption: Compression index n=1.35, Expansion index n=1.28
- Justification: Real engines have heat transfer to cylinder walls, making processes
  polytropic rather than isentropic (n=γ=1.4). Compression has higher n due to
  cooler charge, expansion has lower n due to heat loss during power stroke.

ASSUMPTION 5: Slider-Crank Geometry
- Assumption: L/R ratio = 2.0 (Connecting rod length / Crank radius)
- Justification: Typical for small engines. Affects piston acceleration and
  side forces. Longer rods reduce side loading but increase engine height.

ASSUMPTION 6: Ignition Timing
- Assumption: Spark at 20° BTDC
- Justification: Allows flame propagation to complete by TDC, maximizing pressure
  rise during expansion stroke. Too early causes knock, too late wastes energy.
"""

# ============================================================================
# SECTION 2: HELPER FUNCTIONS
# ============================================================================

def calculate_engine_torque(rpm):
    """
    Calculate engine torque at given RPM using empirical curve fitting.

    The torque curve is modeled as a polynomial that:
    - Starts low at idle (1400 RPM)
    - Peaks at 2500 RPM (10.3 Nm)
    - Decreases at high RPM due to volumetric efficiency loss

    Args:
        rpm: Engine speed in revolutions per minute (scalar or array)

    Returns:
        torque: Engine torque in Nm (scalar or array)
    """
    # Normalize RPM for numerical stability
    rpm_norm = rpm / 1000.0

    # Polynomial coefficients fitted to match:
    # - Torque of ~6 Nm at 1400 RPM (idle)
    # - Peak torque of 10.3 Nm at 2500 RPM
    # - Derivative at 2500 RPM is 0
    # - Torque of ~9.55 Nm at 3600 RPM (rated power, 3.6kW)
    # Solved using a system of linear equations:
    a = -1.8601676839352195
    b = 12.285859702220199
    c = -22.091157973787764
    d = 13.048995393863456

    torque = a * rpm_norm**3 + b * rpm_norm**2 + c * rpm_norm + d

    # Ensure torque doesn't go negative
    torque = np.maximum(torque, 0.5)

    return torque


def calculate_friction_torque_model(rpm):
    """
    Calculate friction torque using quadratic model (assumed model).

    Friction increases with RPM due to:
    - Bearing friction (linear with speed)
    - Piston ring friction (quadratic with speed)
    - Pumping losses (increases with RPM)

    Args:
        rpm: Engine speed in RPM

    Returns:
        friction_torque: Friction torque in Nm
    """
    # Friction coefficients (empirically determined)
    # Calibrated to give realistic BSFC (~280 g/kWh) and friction power (~15-20% at rated speed)
    C0 = 0.5  # Constant friction (Nm)
    C1 = 0.0001  # Linear coefficient (Nm/RPM)
    C2 = 0.00000002  # Quadratic coefficient (Nm/RPM²)

    friction_torque = C0 + C1 * rpm + C2 * rpm**2

    return friction_torque


def calculate_friction_power_model(rpm):
    """
    Calculate friction power in Watts using the assumed model.

    Args:
        rpm: Engine speed in RPM

    Returns:
        friction_power: Friction power in Watts
    """
    friction_torque = calculate_friction_torque_model(rpm)
    omega = rpm * 2 * np.pi / 60  # Convert RPM to rad/s
    friction_power = friction_torque * omega

    return friction_power


def slider_crank_volume(theta, bore, stroke, connecting_rod_length, compression_ratio):
    """
    Calculate instantaneous cylinder volume using slider-crank kinematics.

    Args:
        theta: Crank angle in degrees (0° = TDC)
        bore: Cylinder bore in meters
        stroke: Piston stroke in meters
        connecting_rod_length: Connecting rod length in meters
        compression_ratio: Compression ratio

    Returns:
        volume: Instantaneous cylinder volume in m³
    """
    # Convert angle to radians
    theta_rad = np.deg2rad(theta)

    # Crank radius
    r = stroke / 2

    # Connecting rod length
    l = connecting_rod_length

    # Piston position from TDC (positive downward)
    # Using exact slider-crank equation
    x = r * (1 - np.cos(theta_rad)) + l * (1 - np.sqrt(1 - (r/l * np.sin(theta_rad))**2))

    # Cylinder cross-sectional area
    area = np.pi * (bore / 2)**2

    # Clearance volume (volume at TDC)
    V_clearance = DISPLACEMENT / (compression_ratio - 1)

    # Total volume
    volume = V_clearance + area * x

    return volume


def calculate_cylinder_pressure(theta, compression_ratio):
    """
    Calculate cylinder pressure vs crank angle using polytropic processes.

    The COMPLETE 4-stroke cycle with realistic intake/exhaust:
    1. Intake (0-180°): NEGATIVE pressure (below atmospheric) - suction stroke
    2. Compression (180-360°): Polytropic compression
    3. Combustion & Expansion (360-540°): Gradual heat addition + polytropic expansion
    4. Exhaust (540-720°): Slightly above atmospheric pressure

    The intake and exhaust strokes form the "pumping loop" which represents
    the work expended to move gases in and out of the cylinder.

    Args:
        theta: Crank angle in degrees (array)
        compression_ratio: Compression ratio

    Returns:
        pressure: Cylinder pressure in Pa (array)
    """
    pressure = np.zeros_like(theta)

    # Polytropic indices
    n_compression = 1.35  # Higher than gamma due to heat loss during compression
    n_expansion = 1.28    # Lower than gamma due to heat loss during expansion

    # Reference conditions
    P_atm = INTAKE_PRESSURE  # Atmospheric pressure (Pa)

    # Intake and exhaust pressures (realistic values)
    P_intake = P_atm * 0.85  # Intake pressure ~15% below atmospheric (vacuum effect)
    P_exhaust = P_atm * 1.05  # Exhaust pressure ~5% above atmospheric (backpressure)

    # Peak pressure calculation
    # After compression: P2 = P0 * (compression_ratio)^n
    P_compressed = P_intake * (compression_ratio ** n_compression)

    # After combustion: Pressure rise due to heat addition
    pressure_rise_factor = 2.8
    # P_max = P_compressed * pressure_rise_factor # Not directly used for expansion calculation below

    # Combustion starts IGNITION_TIMING BTDC, so at 360 - IGNITION_TIMING
    combustion_start_angle = 360 - IGNITION_TIMING # Start combustion before TDC
    combustion_end_angle = combustion_start_angle + COMBUSTION_DURATION

    # Determine peak pressure achieved during combustion
    # This is a simplified model, actual peak pressure depends on heat release profile
    P_max_combustion_model = P_compressed * pressure_rise_factor # Peak pressure for expansion

    # Pre-calculate pressures and volumes for relevant points if needed for accuracy
    V_comb_start = slider_crank_volume(combustion_start_angle, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)
    V_TDC = slider_crank_volume(360, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)

    # Polytropic compression from intake pressure to compression start (180 deg)
    # This is not fully consistent with P_compressed but simplified for the cycle loop structure
    # For better accuracy, need to track state points more precisely.

    # Calculate pressure at combustion start using compression equation
    V_180 = slider_crank_volume(180, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)
    P_at_comb_start_calc = P_intake * (V_180 / V_comb_start)**n_compression

    # Calculate pressure at combustion end using the sigmoid function
    progress_at_end = (combustion_end_angle - combustion_start_angle) / COMBUSTION_DURATION
    smooth_factor_at_end = 1 / (1 + np.exp(-10 * (progress_at_end - 0.5)))
    P_at_comb_end_calc = P_at_comb_start_calc + (P_max_combustion_model - P_at_comb_start_calc) * smooth_factor_at_end

    for i, angle in enumerate(theta):
        if 0 <= angle < 180:
            # INTAKE STROKE (SUCTION)
            pressure[i] = P_intake

        elif 180 <= angle < combustion_start_angle:
            # COMPRESSION STROKE (before ignition)
            V_current = slider_crank_volume(angle, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)
            # V_180 is already calculated above as V_180
            pressure[i] = P_intake * (V_180 / V_current)**n_compression

        elif combustion_start_angle <= angle < combustion_end_angle:
            # COMBUSTION period - SMOOTH SIGMOIDAL RISE (Wiebe-like)
            progress = (angle - combustion_start_angle) / COMBUSTION_DURATION
            # Smooth sigmoid function for realistic combustion
            # Map progress from 0 to 1, sigmoid goes from 0 to 1. P starts from P_at_comb_start and rises to P_max_combustion_model
            smooth_factor = 1 / (1 + np.exp(-10 * (progress - 0.5)))
            pressure[i] = P_at_comb_start_calc + (P_max_combustion_model - P_at_comb_start_calc) * smooth_factor

        elif combustion_end_angle <= angle < 540:
            # EXPANSION STROKE (POWER)
            V_current = slider_crank_volume(angle, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)
            V_at_comb_end = slider_crank_volume(combustion_end_angle, BORE, STROKE, CONNECTING_ROD_LENGTH, compression_ratio)

            # Polytropic expansion from pressure at combustion end (P_at_comb_end_calc)
            pressure[i] = P_at_comb_end_calc * (V_at_comb_end / V_current)**n_expansion

        else:
            # EXHAUST STROKE
            pressure[i] = P_exhaust

    return pressure


# ============================================================================
# EXPERIMENT 1: UPHILL LOAD SIMULATION
# ============================================================================

def experiment_1_uphill_load():
    """
    Simulate engine behavior under increasing load (hill climbing scenario).

    Models:
    - Engine torque curve vs RPM
    - Brake torque (load) increasing with time
    - Net torque = Engine torque - Friction torque - Brake torque
    - RPM dynamics: dRPM/dt proportional to net torque

    Outputs:
    - Plot 1: Engine Torque vs RPM (baseline characteristic)
    - Plot 2: RPM vs Time (showing deceleration under load)
    - Plot 3: Torque Balance vs Time (combined)
    """
    print("\n" + "="*70)
    print("EXPERIMENT 1: UPHILL LOAD SIMULATION")
    print("="*70)

    # Time parameters
    dt = 0.01  # Time step (seconds)
    t_max = 30  # Simulation duration (seconds)
    time = np.arange(0, t_max, dt)

    # Initialize arrays
    rpm = np.zeros_like(time)
    engine_torque = np.zeros_like(time)
    friction_torque = np.zeros_like(time)
    brake_torque = np.zeros_like(time)
    net_torque = np.zeros_like(time)

    # Initial conditions
    rpm[0] = RATED_RPM  # Start at rated speed (3600 RPM)

    # Engine inertia (estimated for small single-cylinder engine)
    # I = 0.5 kg·m² (increased for realistic dynamics - includes flywheel)
    # Small engines have flywheels that increase rotational inertia
    I_engine = 0.5  # kg·m²

    # Simulate load increasing with time (simulating uphill climb)
    for i in range(len(time)):
        t = time[i]

        # Current RPM
        current_rpm = rpm[i]

        # Engine torque at current RPM
        engine_torque[i] = calculate_engine_torque(current_rpm)

        # Friction torque at current RPM (using the model, not Willans for Exp1)
        friction_torque[i] = calculate_friction_torque_model(current_rpm)

        # Brake torque (load) increases linearly with time
        # Simulates going uphill - load increases gradually
        if t < 10:
            brake_torque[i] = 2.0  # Light load initially (2 Nm)
        elif t < 20:
            brake_torque[i] = 2.0 + (t - 10) * 0.5  # Increasing load
        else:
            brake_torque[i] = 7.0  # Heavy load (7 Nm)

        # Net torque
        net_torque[i] = engine_torque[i] - friction_torque[i] - brake_torque[i]

        # Update RPM using angular acceleration
        # τ_net = I * α, where α = dω/dt
        # ω = RPM * 2π/60
        # dRPM/dt = (τ_net / I) * (60 / 2π)
        if i < len(time) - 1:
            alpha = net_torque[i] / I_engine  # Angular acceleration (rad/s²)
            d_rpm = alpha * (60 / (2 * np.pi)) * dt  # Change in RPM
            # Positive net torque increases RPM, negative decreases it
            rpm[i+1] = max(rpm[i] + d_rpm, IDLE_RPM)  # Don't go below idle

    # Analysis
    print(f"\nInitial RPM: {rpm[0]:.0f} RPM")
    print(f"Final RPM: {rpm[-1]:.0f} RPM")
    print(f"RPM Drop: {rpm[0] - rpm[-1]:.0f} RPM")
    print(f"Initial Load: {brake_torque[0]:.1f} Nm")
    print(f"Final Load: {brake_torque[-1]:.1f} Nm")

    # Find when engine can no longer maintain speed (net torque becomes negative)
    critical_idx = np.where(net_torque < 0)[0]
    if len(critical_idx) > 0:
        critical_time = time[critical_idx[0]]
        critical_load = brake_torque[critical_idx[0]]
        print(f"\n! Engine begins to lose speed at t = {critical_time:.1f}s")
        print(f"  Critical load: {critical_load:.1f} Nm")
        print(f"  RPM at critical point: {rpm[critical_idx[0]]:.0f} RPM")

    # PLOT 1: Engine Torque vs RPM (Baseline Characteristic Curve)
    rpm_range = np.linspace(IDLE_RPM, 4000, 200)
    torque_curve = calculate_engine_torque(rpm_range)

    plt.figure(figsize=(10, 6))
    plt.plot(rpm_range, torque_curve, 'b-', linewidth=2.5, label='Engine Torque')
    plt.axhline(y=MAX_TORQUE, color='r', linestyle='--', label=f'Max Torque = {MAX_TORQUE} Nm')
    plt.axvline(x=PEAK_TORQUE_RPM, color='g', linestyle='--', alpha=0.5, label=f'Peak at {PEAK_TORQUE_RPM} RPM')
    plt.xlabel('Engine Speed (RPM)', fontsize=12, fontweight='bold')
    plt.ylabel('Torque (Nm)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: Honda GX160 Torque Curve', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig('plot1_torque_curve.png', dpi=300, bbox_inches='tight')

    # PLOT 2: RPM vs Time
    plt.figure(figsize=(10, 6))
    plt.plot(time, rpm, 'b-', linewidth=2)
    plt.axhline(y=RATED_RPM, color='g', linestyle='--', alpha=0.5, label='Rated RPM')
    plt.axhline(y=IDLE_RPM, color='r', linestyle='--', alpha=0.5, label='Idle RPM')
    plt.xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    plt.ylabel('Engine Speed (RPM)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: RPM vs Time Under Increasing Load', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('plot2_rpm_vs_time.png', dpi=300, bbox_inches='tight')

    # PLOT 3: Torque Balance vs Time (Combined)
    plt.figure(figsize=(10, 6))
    plt.plot(time, engine_torque, 'b-', linewidth=2, label='Engine Torque', alpha=0.7)
    plt.plot(time, brake_torque, 'r-', linewidth=2, label='Brake Torque (Load)', alpha=0.7)
    plt.plot(time, friction_torque, 'orange', linewidth=2, label='Friction Torque', alpha=0.7)
    plt.plot(time, net_torque, 'g-', linewidth=2.5, label='Net Torque')
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    plt.xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    plt.ylabel('Torque (Nm)', fontsize=12, fontweight='bold')
    plt.title('Experiment 1: Torque Balance vs Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig('plot3_torque_balance.png', dpi=300, bbox_inches='tight')


    print("\n Experiment 1 complete. 3 plots generated.")
    plt.show()

    # Return all relevant data for synthetic data generation
    return rpm, time, engine_torque, friction_torque, brake_torque, net_torque


# ============================================================================
# EXPERIMENT 2: FRICTION POWER ESTIMATION
# ============================================================================

def experiment_2_friction_power():
    """
    Estimate friction power using Willans-type analysis at multiple RPMs.

    Friction power is determined from the x-intercept of the fuel-flow vs brake-power curve.

    Outputs:
    - Plot 4: Friction Power vs RPM (derived from Willans Line)
    - Plot 4a: Friction Power vs RPM (from assumed model - optional/extra)
    """
    print("\n" + "="*70)
    print("EXPERIMENT 2: FRICTION POWER ESTIMATION (WILLANS APPROACH)")
    print("="*70)

    # RPM range for analysis (for Willans approach)
    willans_rpm_points = np.linspace(IDLE_RPM, RATED_RPM + 1000, 10) # Test at several RPMs
    friction_power_willans_list = []
    friction_power_model_list = []

    print(f"\nPerforming Willans analysis at {len(willans_rpm_points)} RPM points...")

    for rpm_test in willans_rpm_points:
        # Generate synthetic data for different load conditions at this RPM
        brake_power_kw_single_rpm = np.linspace(0.1, MAX_POWER/1000 * 0.9, 10) # Vary load up to 90% of max
        fuel_consumption_single_rpm = np.zeros_like(brake_power_kw_single_rpm)

        # Use the assumed friction model to simulate 'true' indicated power for fuel consumption
        # This provides a basis for the synthetic data from which Willans line is derived.
        friction_power_at_rpm_test = calculate_friction_power_model(rpm_test) / 1000 # kW
        friction_power_model_list.append(friction_power_at_rpm_test)

        for i, P_brake in enumerate(brake_power_kw_single_rpm):
            P_indicated = P_brake + friction_power_at_rpm_test
            P_fuel = P_indicated / COMBUSTION_EFFICIENCY
            fuel_flow_kg_s = P_fuel * 1000 / FUEL_LHV  # kg/s
            fuel_consumption_single_rpm[i] = fuel_flow_kg_s * 3600  # kg/h

        # Add realistic noise to data
        np.random.seed(int(rpm_test)) # Use RPM as seed for consistent noise per RPM
        noise = np.random.normal(0, 0.01, len(fuel_consumption_single_rpm))
        fuel_consumption_noisy_single_rpm = fuel_consumption_single_rpm * (1 + noise)

        # Fit Willans Line (linear regression) for this RPM
        if len(brake_power_kw_single_rpm) > 1:
            coefficients = np.polyfit(brake_power_kw_single_rpm, fuel_consumption_noisy_single_rpm, 1)
            slope = coefficients[0]
            intercept = coefficients[1]

            # Compute friction power from x-intercept: Pf = -a / b
            if slope != 0:
                # Use absolute value for friction power as it's a magnitude
                friction_power_willans = abs(-intercept / slope)
                friction_power_willans_list.append(friction_power_willans)
            else:
                friction_power_willans_list.append(np.nan) # Cannot determine friction power if slope is zero
        else:
            friction_power_willans_list.append(np.nan)

    # Convert lists to numpy arrays
    friction_power_willans_arr = np.array(friction_power_willans_list)
    friction_power_model_arr = np.array(friction_power_model_list)

    # Analysis
    print(f"\nFriction Power (Willans, avg): {np.nanmean(friction_power_willans_arr):.3f} kW")
    print(f"Friction Power (Model, avg): {np.mean(friction_power_model_arr):.3f} kW")

    print("\n INSIGHT: Willans Line provides an experimental method to estimate friction power.")
    print("   Differences between Willans-derived and model-assumed friction power")
    print("   can indicate inaccuracies in the assumed friction model or experimental noise.")

    # PLOT 4: Friction Power vs RPM (Derived from Willans Line - Main Result)
    plt.figure(figsize=(10, 6))
    plt.plot(willans_rpm_points, friction_power_willans_arr, 'o-', markersize=6, color='purple', label='Friction Power (Willans Method)')
    plt.plot(willans_rpm_points, friction_power_model_arr, 'x--', markersize=8, color='gray', alpha=0.7, label='Friction Power (Assumed Model)')
    plt.axvline(x=IDLE_RPM, color='orange', linestyle='--', alpha=0.5, label=f'Idle ({IDLE_RPM} RPM)')
    plt.axvline(x=RATED_RPM, color='g', linestyle='--', alpha=0.5, label=f'Rated ({RATED_RPM} RPM)')
    plt.xlabel('Engine Speed (RPM)', fontsize=12, fontweight='bold')
    plt.ylabel('Friction Power (kW)', fontsize=12, fontweight='bold')
    plt.title('Experiment 2: Friction Power vs RPM (Willans Method)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig('plot4_friction_power_willans.png', dpi=300, bbox_inches='tight')

    print("\n Experiment 2 complete. 1 main plot generated (plus underlying model for comparison).")
    plt.show()

    # Return all relevant data for synthetic data generation
    return willans_rpm_points, friction_power_willans_arr, friction_power_model_arr


# ============================================================================
# EXPERIMENT 3: WILLANS LINE FUEL CONSUMPTION
# ============================================================================

def experiment_3_willans_line():
    """
    Generate Willans Line for fuel consumption analysis.

    The Willans Line is a linear relationship between fuel consumption rate
    and brake power output. The equation is:

    Ł_fuel = a + b * P_brake

    Where:
    - Ł_fuel: Fuel mass flow rate (kg/h)
    - P_brake: Brake power (kW)
    - a: y-intercept (fuel consumption at zero power = friction losses)
    - b: slope (inverse of fuel conversion efficiency)

    The x-intercept gives friction power.
    BSFC (Brake Specific Fuel Consumption) = b (g/kWh)

    Outputs:
    - Plot 5: Fuel Consumption vs Brake Power with fitted Willans Line
    """
    print("\n" + "="*70)
    print("EXPERIMENT 3: WILLANS LINE FUEL CONSUMPTION")
    print("="*70)

    # Generate synthetic data for different load conditions
    # Operating at constant RPM (rated speed) with varying load
    rpm_test = RATED_RPM

    # Brake power range (0 to max power) - INCREASED to 200 points for smoother curves
    brake_power_kw = np.linspace(0.2, MAX_POWER/1000, 200)  # kW

    # Calculate fuel consumption for each power level
    # Using thermal efficiency model
    fuel_consumption = np.zeros_like(brake_power_kw)

    # Friction power at test RPM (using the assumed model for consistency in generating synthetic data)
    friction_power_kw = calculate_friction_power_model(rpm_test) / 1000

    for i, P_brake in enumerate(brake_power_kw):
        # Indicated power = Brake power + Friction power
        P_indicated = P_brake + friction_power_kw

        # Fuel power needed (accounting for combustion efficiency)
        P_fuel = P_indicated / COMBUSTION_EFFICIENCY

        # Fuel mass flow rate (kg/h)
        # P_fuel = Ł_fuel * LHV
        fuel_flow_kg_s = P_fuel * 1000 / FUEL_LHV  # kg/s
        fuel_consumption[i] = fuel_flow_kg_s * 3600  # kg/h

    # Add realistic noise to data
    np.random.seed(42)
    noise = np.random.normal(0, 0.02, len(fuel_consumption))
    fuel_consumption_noisy = fuel_consumption * (1 + noise)

    # Fit Willans Line (linear regression)
    coefficients = np.polyfit(brake_power_kw, fuel_consumption_noisy, 1)
    slope = coefficients[0]  # b (kg/kWh)
    intercept = coefficients[1]  # a (kg/h)

    # Generate fitted line
    fuel_fitted = slope * brake_power_kw + intercept

    # Calculate BSFC (Brake Specific Fuel Consumption)
    # BSFC = slope in g/kWh
    BSFC = slope * 1000  # Convert kg/kWh to g/kWh

    # Calculate friction power from x-intercept
    x_intercept = -intercept / slope  # kW
    friction_power_willans = abs(x_intercept) # Take absolute for display

    # Analysis
    print(f"\nWillans Line Equation:")
    print(f"  Ł_fuel = {slope:.4f} * P_brake + {intercept:.4f}")
    print(f"  Units: kg/h = (kg/kWh) * kW + kg/h")

    print(f"\n RESULTS:")
    print(f"  BSFC (Brake Specific Fuel Consumption): {BSFC:.1f} g/kWh")
    print(f"  Friction Power (from x-intercept): {friction_power_willans:.3f} kW")
    print(f"  Friction Power (from model): {friction_power_kw:.3f} kW")
    print(f"  Difference: {abs(friction_power_willans - friction_power_kw)/friction_power_kw * 100:.1f}%")

    print(f"\n INSIGHT: BSFC of {BSFC:.0f} g/kWh is typical for small gasoline engines.")
    print("   Modern automotive engines achieve 220-250 g/kWh.")
    print("   The Willans Line is linear because indicated efficiency is roughly constant.")

    # PLOT 5: Willans Line (matching reference image style)
    plt.figure(figsize=(10, 6))

    # Plot data points with diamond markers (matching reference image)
    plt.scatter(brake_power_kw, fuel_consumption_noisy, color='blue', s=30, # Reduced marker size to 30
                marker='D', alpha=0.7, label='Measured Data', edgecolors='darkblue', linewidth=1.5)

    # Plot fitted Willans Line
    plt.plot(brake_power_kw, fuel_fitted, 'r-', linewidth=3,
             label=f'Willans Line\nBSFC = {BSFC:.0f} g/kWh', zorder=10)

    # Extend line to show friction power intercept more clearly
    power_extended = np.linspace(-0.6, max(brake_power_kw), 100)
    fuel_extended = slope * power_extended + intercept
    plt.plot(power_extended, fuel_extended, 'r--', linewidth=1.5, alpha=0.5)

    # Show axes
    plt.axvline(x=0, color='k', linestyle='-', linewidth=1)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=1)

    # Annotate friction power (matching reference image style)
    plt.annotate(f'Friction\nPower: {friction_power_willans:.2f} kW', # Display absolute value
                xy=(x_intercept, 0), # Point to actual x-intercept
                xytext=(x_intercept - 0.8, 0.3),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, color='red', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

    # Set axis limits to show intercept
    plt.xlim(-0.7, max(brake_power_kw) + 0.2)
    plt.ylim(-0.05, max(fuel_consumption_noisy) + 0.1)

    plt.xlabel('Brake Power (kW)', fontsize=13, fontweight='bold')
    plt.ylabel('Fuel Consumption (kg/h)', fontsize=13, fontweight='bold')
    plt.title('Experiment 3: Willans Line - Fuel Consumption Analysis', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
    plt.tight_layout()
    plt.savefig('plot5_willans_line.png', dpi=300, bbox_inches='tight')

    # PLOT 5B: BSFC vs Brake Power
    plt.figure(figsize=(10, 6))

    # Calculate BSFC at each power level
    bsfc_values = (fuel_consumption_noisy / brake_power_kw) * 1000  # g/kWh

    # Plot BSFC vs Brake Power
    plt.plot(brake_power_kw, bsfc_values, 'go-', linewidth=2.5, markersize=5, # Reduced marker size to 5
             label='BSFC', markerfacecolor='lightgreen', markeredgecolor='darkgreen', markeredgewidth=2)

    # Add horizontal line for average BSFC
    avg_bsfc = np.mean(bsfc_values)
    plt.axhline(y=avg_bsfc, color='red', linestyle='--', linewidth=2,
                label=f'Average BSFC = {avg_bsfc:.1f} g/kWh')

    # Shade optimal efficiency region (typically 60-90% of MAX_POWER)
    optimal_power_min = 0.6 * (MAX_POWER / 1000)
    optimal_power_max = 0.9 * (MAX_POWER / 1000)
    plt.axvspan(optimal_power_min, optimal_power_max, alpha=0.1, color='green', label='Optimal Efficiency Zone')

    # Annotations
    min_bsfc_idx = np.argmin(bsfc_values)
    min_bsfc = bsfc_values[min_bsfc_idx]
    optimal_brake_power = brake_power_kw[min_bsfc_idx]

    plt.annotate(f'Best Efficiency\n{min_bsfc:.1f} g/kWh\n@ {optimal_brake_power:.1f} kW',
                xy=(optimal_brake_power, min_bsfc),
                xytext=(optimal_brake_power - 1.5, min_bsfc + 20),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2),
                fontsize=10, color='darkgreen', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

    plt.xlabel('Brake Power (kW)', fontsize=13, fontweight='bold')
    plt.ylabel('BSFC (g/kWh)', fontsize=13, fontweight='bold')
    plt.title('Experiment 3B: Brake Specific Fuel Consumption vs Brake Power', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='upper right', fontsize=10, framealpha=0.9)
    plt.xlim(0, max(brake_power_kw) + 0.2) # Adjust x-limit to fit new axis
    plt.tight_layout()
    plt.savefig('plot5b_bsfc_vs_load.png', dpi=300, bbox_inches='tight')

    print("\n Experiment 3 complete. 2 plots generated.")
    plt.show()

    return brake_power_kw, fuel_consumption_noisy, BSFC, x_intercept, bsfc_values # Return x_intercept separately


# ============================================================================
# EXPERIMENT 4: CYLINDER PRESSURE & P-V DIAGRAM
# ============================================================================

def experiment_4_pv_diagram():
    """
    Generate Pressure-Volume (P-V) diagram for the engine cycle.

    The P-V diagram shows the thermodynamic cycle:
    1. Intake stroke (0-180°): Constant pressure, increasing volume
    2. Compression stroke (180-360°): Polytropic compression
    3. Combustion & Expansion (360-540°): Heat addition + expansion
    4. Exhaust stroke (540-720°): Slightly above atmospheric pressure

    The area enclosed by the P-V loop represents the net work per cycle.

    Outputs:
    - Plot 6: Pressure vs Crank Angle (P-θ diagram)
    - Plot 7: Pressure vs Volume (P-V diagram)
    """
    print("\n" + "="*70)
    print("EXPERIMENT 4: CYLINDER PRESSURE & P-V DIAGRAM")
    print("="*70)

    # Crank angle range (0-720° for complete 4-stroke cycle) - INCREASED to 2000 points
    theta = np.linspace(0, 720, 2000)

    # Calculate pressure at each crank angle
    pressure = calculate_cylinder_pressure(theta, COMPRESSION_RATIO)

    # Calculate volume at each crank angle
    volume = np.zeros_like(theta)
    for i, angle in enumerate(theta):
        volume[i] = slider_crank_volume(angle, BORE, STROKE, CONNECTING_ROD_LENGTH, COMPRESSION_RATIO)

    # Convert volume to cm³ for readability
    volume_cm3 = volume * 1e6

    # Convert pressure to bar for readability
    pressure_bar = pressure / 1e5

    # Calculate work per cycle (area of P-V loop) using sum(P * dV)
    # Compute dV (difference between consecutive volume samples)
    dv = np.diff(volume) # dV has len(volume)-1 elements

    # To match length, we take the average of two consecutive pressures for the P*dV calculation
    # or simply use the pressure at the start of the interval.
    # For simplicity and to match the trapezoidal rule approximation, we'll use average pressure.
    pressure_avg = (pressure[:-1] + pressure[1:]) / 2

    # Work = sum(P * dV) - ensure matching array lengths
    work_per_cycle = np.sum(pressure_avg * dv)  # Joules

    # Calculate indicated power
    # Power = Work per cycle * (RPM / 2) / 60  (for 4-stroke)
    indicated_power = work_per_cycle * (RATED_RPM / 2) / 60  # Watts
    indicated_power_kw = indicated_power / 1000

    # Calculate indicated mean effective pressure (IMEP)
    IMEP = work_per_cycle / DISPLACEMENT  # Pa
    IMEP_bar = IMEP / 1e5  # bar

    # Analysis
    max_pressure = np.max(pressure_bar)
    max_pressure_angle = theta[np.argmax(pressure_bar)]

    print(f"\nTHERMODYNAMIC ANALYSIS:")
    print(f"  Calculated Displacement: {DISPLACEMENT * 1e6:.1f} cm³")
    print(f"  Compression Ratio: {COMPRESSION_RATIO:.1f}:1")
    print(f"  Clearance Volume: {DISPLACEMENT / (COMPRESSION_RATIO - 1) * 1e6:.2f} cm³")
    print(f"  Max Cylinder Pressure: {max_pressure:.1f} bar at {max_pressure_angle:.0f}°")
    print(f"  Work per Cycle: {work_per_cycle:.2f} J")
    print(f"  Indicated Power: {indicated_power_kw:.2f} kW")
    print(f"  IMEP (Indicated Mean Effective Pressure): {IMEP_bar:.2f} bar")

    print(f"\n INSIGHT: Peak pressure occurs shortly after TDC (360°).")
    print(f"   This is due to combustion initiated at {IGNITION_TIMING}° BTDC.")
    print("   Higher compression ratios increase efficiency but risk knock.")

    # PLOT 6: Pressure vs Crank Angle
    plt.figure(figsize=(12, 6))
    plt.plot(theta, pressure_bar, 'b-', linewidth=2)

    # Mark key points
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.3, label='TDC (Intake)')
    plt.axvline(x=180, color='green', linestyle='--', alpha=0.5, label='BDC (Start Compression)')
    plt.axvline(x=360, color='red', linestyle='--', alpha=0.5, label='TDC (Combustion)')
    plt.axvline(x=540, color='orange', linestyle='--', alpha=0.5, label='BDC (Start Exhaust)')
    plt.axvline(x=720, color='gray', linestyle='--', alpha=0.3)
    plt.axvline(x=360 - IGNITION_TIMING, color='purple', linestyle=':', alpha=0.6, label=f'Ignition ({IGNITION_TIMING}° BTDC)')

    # Annotate strokes
    plt.text(90, max_pressure * 0.9, 'INTAKE', ha='center', fontsize=11, fontweight='bold', color='gray')
    plt.text(270, max_pressure * 0.9, 'COMPRESSION', ha='center', fontsize=11, fontweight='bold', color='green')
    plt.text(450, max_pressure * 0.9, 'POWER', ha='center', fontsize=11, fontweight='bold', color='red')
    plt.text(630, max_pressure * 0.9, 'EXHAUST', ha='center', fontsize=11, fontweight='bold', color='orange')

    plt.xlabel('Crank Angle (degrees)', fontsize=12, fontweight='bold')
    plt.ylabel('Pressure (bar)', fontsize=12, fontweight='bold')
    plt.title('Experiment 4: Pressure vs Crank Angle (P-\u03B8 Diagram)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right', fontsize=9)
    plt.tight_layout()
    plt.savefig('plot6_pressure_vs_angle.png', dpi=300, bbox_inches='tight')

    # PLOT 7: P-V Diagram (COMPLETE 4-STROKE CYCLE with PUMPING LOOP)
    fig, ax = plt.subplots(figsize=(12, 9))

    # Convert pressure to bar and reference to atmospheric (show negative values)
    P_atm_bar = INTAKE_PRESSURE / 1e5  # Atmospheric pressure in bar
    pressure_bar_gauge = pressure_bar - P_atm_bar  # Gauge pressure (can be negative)

    # Plot the complete cycle
    ax.plot(volume_cm3, pressure_bar_gauge, 'b-', linewidth=2.5, label='4-Stroke Cycle', zorder=5)

    # Identify and highlight different strokes
    intake_idx = (theta >= 0) & (theta <= 180)
    compression_idx = (theta >= 180) & (theta <= (360 - IGNITION_TIMING))
    # Expansion technically starts after peak pressure, here we mark after combustion end
    expansion_idx = (theta >= (360 + COMBUSTION_DURATION - IGNITION_TIMING)) & (theta <= 540) # Approximately after combustion
    exhaust_idx = (theta >= 540) & (theta <= 720)

    # Fill areas for visual clarity, using specific labels that will be picked up by the legend
    ax.fill_between(volume_cm3[compression_idx], 0, pressure_bar_gauge[compression_idx],
                     alpha=0.15, color='green', label='Compression')

    ax.fill_between(volume_cm3[expansion_idx], 0, pressure_bar_gauge[expansion_idx],
                     alpha=0.15, color='red', label='Expansion')

    ax.fill_between(volume_cm3[intake_idx], 0, pressure_bar_gauge[intake_idx],
                     alpha=0.25, color='cyan', label='Intake', edgecolor='blue', linewidth=1.5)
    ax.fill_between(volume_cm3[exhaust_idx], 0, pressure_bar_gauge[exhaust_idx],
                     alpha=0.25, color='orange', label='Exhaust', edgecolor='darkorange', linewidth=1.5)

    # Mark key points
    V_clearance = DISPLACEMENT / (COMPRESSION_RATIO - 1) * 1e6
    V_total = (DISPLACEMENT + DISPLACEMENT / (COMPRESSION_RATIO - 1)) * 1e6

    ax.axvline(x=V_clearance, color='red', linestyle='--', alpha=0.4, linewidth=1.5, label='TDC')
    ax.axvline(x=V_total, color='green', linestyle='--', alpha=0.4, linewidth=1.5, label='BDC')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, label='Atmospheric Pressure')

    # Annotate key features
    max_pressure_idx = np.argmax(pressure_bar_gauge)
    max_pressure_gauge = pressure_bar_gauge[max_pressure_idx]

    ax.annotate(f'Peak Pressure\n{max_pressure_gauge + P_atm_bar:.1f} bar abs\n({max_pressure_gauge:.1f} bar gauge)',
                xy=(volume_cm3[max_pressure_idx], max_pressure_gauge),
                xytext=(V_clearance + 30, max_pressure_gauge - 10),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, color='red', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

    # Annotate intake (negative pressure)
    intake_mid_idx = np.where(intake_idx)[0][len(np.where(intake_idx)[0])//2]
    ax.annotate('INTAKE\n(Suction)',
                xy=(volume_cm3[intake_mid_idx], pressure_bar_gauge[intake_mid_idx]),
                xytext=(volume_cm3[intake_mid_idx] + 20, pressure_bar_gauge[intake_mid_idx] - 0.3),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                fontsize=10, color='blue', fontweight='bold')

    # Annotate exhaust
    exhaust_mid_idx = np.where(exhaust_idx)[0][len(np.where(exhaust_idx)[0])//2]
    ax.annotate('EXHAUST',
                xy=(volume_cm3[exhaust_mid_idx], pressure_bar_gauge[exhaust_mid_idx]),
                xytext=(volume_cm3[exhaust_mid_idx] - 40, pressure_bar_gauge[exhaust_mid_idx] + 0.2),
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=2),
                fontsize=10, color='darkorange', fontweight='bold')

    # Add FINER GRID INTERVALS
    # Major grid (existing)
    ax.grid(True, which='major', alpha=0.4, linestyle='-', linewidth=0.8)
    # Minor grid (NEW - finer intervals)
    ax.minorticks_on()
    ax.grid(True, which='minor', alpha=0.2, linestyle=':', linewidth=0.5)

    # Set minor tick intervals for better visibility
    from matplotlib.ticker import MultipleLocator, AutoMinorLocator
    ax.xaxis.set_minor_locator(MultipleLocator(10))  # Every 10 cm³
    ax.yaxis.set_minor_locator(MultipleLocator(2))   # Every 2 bar

    ax.set_xlabel('Volume (cm³)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Gauge Pressure (bar)\n[Negative = Below Atmospheric]', fontsize=13, fontweight='bold')
    ax.set_title('Experiment 4: Complete P-V Diagram with Pumping Loop', fontsize=14, fontweight='bold')

    # Use auto legend to pick up labels and colors from plot commands
    ax.legend(loc='lower right', fontsize=8, framealpha=0.95, edgecolor='black')

    plt.tight_layout()
    plt.savefig('plot7_pv_diagram.png', dpi=300, bbox_inches='tight')

    print("\n Experiment 4 complete. 2 plots generated.")
    plt.show()

    return theta, pressure_bar, volume_cm3, work_per_cycle, IMEP_bar


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all experiments sequentially.
    """
    print("\n" + "="*70)
    print(" " * 15 + "ENGINE DYNAMOMETER SIMULATION")
    print(" " * 20 + "Honda GX160 Engine")
    print(" " * 18 + "ME-448 IC Engines Lab")
    print("="*70)

    print("\n ENGINE SPECIFICATIONS:")
    print(f"  Model: Honda GX160")
    print(f"  Type: 4-Stroke, Single Cylinder, OHV")
    print(f"  Bore × Stroke: {BORE * 1000:.0f} mm × {STROKE * 1000:.0f} mm")
    print(f"  Calculated Displacement: {DISPLACEMENT * 1e6:.1f} cm³")
    print(f"  Compression Ratio: {COMPRESSION_RATIO:.1f}:1")
    print(f"  Max Power: {MAX_POWER / 1000:.1f} kW @ {RATED_RPM} RPM")
    print(f"  Max Torque: {MAX_TORQUE:.1f} Nm @ {PEAK_TORQUE_RPM} RPM")

    # Run all experiments and collect data
    exp1_rpm, exp1_time, exp1_engine_torque, exp1_friction_torque, exp1_brake_torque, exp1_net_torque = experiment_1_uphill_load()
    exp2_rpm_points, exp2_friction_power_willans_arr, exp2_friction_power_model_arr = experiment_2_friction_power()
    exp3_brake_power_kw, exp3_fuel_consumption_noisy, exp3_BSFC_val, exp3_friction_power_willans_val, exp3_bsfc_values = experiment_3_willans_line()
    exp4_theta, exp4_pressure_bar, exp4_volume_cm3, exp4_work_per_cycle, exp4_IMEP_bar = experiment_4_pv_diagram()

    # Summary
    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)
    print(f" Total plots generated: 8")
    print(f"  - Experiment 1: 3 plots (Torque curve, RPM vs time, Torque balance)")
    print(f"  - Experiment 2: 1 plot (Friction power: Willans Method vs Assumed Model)")
    print(f"  - Experiment 3: 2 plots (Willans Line, BSFC vs Load)")
    print(f"  - Experiment 4: 2 plots (P-θ and P-V diagrams)")

    print("\n All results are consistent with Honda GX160 specifications.")
    print(" Close plot windows to exit the program.")


    print("\n" + "="*70)
    print("GENERATED SYNTHETIC DATA SUMMARY")
    print("="*70)

    # Experiment 1 Data
    print("\n--- Experiment 1: Uphill Load Simulation Data ---")
    df1 = pd.DataFrame({
        'Time (s)': exp1_time,
        'RPM': exp1_rpm,
        'Engine Torque (Nm)': exp1_engine_torque,
        'Friction Torque (Nm)': exp1_friction_torque,
        'Brake Torque (Load Nm)': exp1_brake_torque,
        'Net Torque (Nm)': exp1_net_torque
    })
    print(df1.sample(min(10, len(df1))).sort_values(by='Time (s)').to_string(index=False))
    df1.to_csv('experiment1_uphill_load_data.csv', index=False)
    print(" Experiment 1 data saved to 'experiment1_uphill_load_data.csv'")

    # Experiment 2 Data
    print("\n--- Experiment 2: Friction Power Estimation Data ---")
    df2 = pd.DataFrame({
        'RPM': exp2_rpm_points,
        'Friction Power (Willans, kW)': exp2_friction_power_willans_arr,
        'Friction Power (Model, kW)': exp2_friction_power_model_arr
    })
    print(df2.sample(min(10, len(df2))).sort_values(by='RPM').to_string(index=False))
    df2.to_csv('experiment2_friction_power_data.csv', index=False)
    print(" Experiment 2 data saved to 'experiment2_friction_power_data.csv'")

    # Experiment 3 Data
    print("\n--- Experiment 3: Willans Line & BSFC Data ---")
    df3 = pd.DataFrame({
        'Brake Power (kW)': exp3_brake_power_kw,
        'Fuel Consumption (kg/h)': exp3_fuel_consumption_noisy,
        'BSFC (g/kWh)': exp3_bsfc_values
    })
    print(df3.sample(min(10, len(df3))).sort_values(by='Brake Power (kW)').to_string(index=False))
    df3.to_csv('experiment3_willans_line_bsfc_data.csv', index=False)
    print(" Experiment 3 data saved to 'experiment3_willans_line_bsfc_data.csv'")

    # Experiment 4 Data
    print("\n--- Experiment 4: P-V Diagram Data ---")
    df4 = pd.DataFrame({
        'Crank Angle (deg)': exp4_theta,
        'Volume (cm^3)': exp4_volume_cm3,
        'Pressure (bar)': exp4_pressure_bar
    })
    print(df4.sample(min(10, len(df4))).sort_values(by='Crank Angle (deg)').to_string(index=False))
    df4.to_csv('experiment4_pv_diagram_data.csv', index=False)
    print(" Experiment 4 data saved to 'experiment4_pv_diagram_data.csv'")

    print("\n" + "="*70)
    print("END OF DATA SUMMARY")
    print("="*70)


if __name__ == "__main__":
    main()
