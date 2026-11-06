# We import the libraries we are going to use
import math
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt

# We define the constants we are going to use
R_E = 6371000.0 # Earth's radius in meters
G_M = 3.986e14  # Standard gravitational parameter in m^3/s^2
K_L = 120000    # Kármán line in meters
FCC = 5         # FCC deorbit rule in years

# We create the main function
def main():
    try:
        altitude = float(input("Altitude(m): "))
        mass = float(input("Mass(kg): "))
        area = float(input("Area(m^2): ")) # Cross-sectional area
        cd = float(input("Cd: ")) # Drag coefficient
        b = get_ballistic_coefficient(mass, area, cd)
        density = get_density(altitude)
        delta_v = get_deorbit_deltav(altitude)
        years, days_list, altitude_list = simulate_decay(altitude, b)
        if years <= FCC:
            status = "COMPLIANT (< 5 years)"
        else:
            status = "NON-COMPLIANT (Requires active deorbit)"

    except ValueError:
        sys.exit("Wrong values")

    table = [
        ["Initial altitude", f"{altitude:.1f} m"],
        ["Ballistic coefficient", f"{b:.2f} kg/m^2"],
        ["Initial air density", f"{density:.2e} kg/m^3"],
        ["Estimated orbital lifetime", f"{years:.2f} years"],
        ["5-year rule", status],
        ["Emergency deorbit deltav", f"{delta_v:.2f} m/s"],
    ]
    print("\n" + tabulate(table, headers=["Parameters","Values"], tablefmt="grid"))

    plt.figure(figsize=(8, 5))
    plt.plot(days_list, altitude_list, color="blue", label="Satellite Altitude")
    plt.axhline(y=120000, color="green", linestyle="--", label="Re-entry Interface (120 km)")
    plt.title("LEO Satellite Orbital Decay Simulation")
    plt.xlabel("Time (Days)")
    plt.ylabel("Altitude (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("decay_plot.png")
    print("Plot saved successfully as decay_plot.png")

def get_ballistic_coefficient(mass, area, cd):
    if mass <= 0 or area <= 0 or cd <= 0:
        raise ValueError
    b = mass / (area * cd) # Ballistic coefficient
    return b

def get_density(altitude):
    if altitude < 100000 or altitude > 1000000:
        raise ValueError
    if altitude < 250000:
        rho_0 = 2.0e-8 # Base density reference for lower thermosphere
        h_0 = 120000   # Reference altitude base in meters
        H = 25000.0    # Scale height for this altitude band
    elif altitude < 450000:
        rho_0 = 6.0e-11
        h_0 = 250000
        H = 45000.0
    else:
        rho_0 = 7.0e-13
        h_0 = 450000
        H = 65000.0
    return rho_0 * math.exp(-(altitude - h_0) / H)

def get_deorbit_deltav(altitude):
    if altitude <= K_L or altitude > 1000000:
        raise ValueError
    r_1 = R_E + altitude     # Initial orbital radius
    r_2 = R_E + K_L          # Reentry radius
    v_1 = math.sqrt(G_M/r_1) # Speed at first orbit
    a_t = (r_1 + r_2)/2      # Major semiaxis of the transfer ellipse
    v_t = math.sqrt(G_M*((2/r_1)-(1/a_t))) # Vis-viva equation
    return v_1 - v_t

def simulate_decay(altitude, b):
    if altitude <= K_L or altitude > 1000000 or b <= 0:
        raise ValueError
    current_alt = altitude # Mutable variable tracking altitude loss
    days = 0               # Counter for elapsed mission simulation days
    days_list = [0]        
    altitude_list = [current_alt]
    seconds_per_day = 86400
    while current_alt > K_L and days < 36500:
        r = R_E + current_alt
        rho = get_density(current_alt)
        v = math.sqrt(G_M / r)
        loss = ((rho*r*v)/b)*seconds_per_day
        current_alt -= loss
        if current_alt < K_L:
            current_alt = K_L
        days += 1
        days_list.append(days)
        altitude_list.append(current_alt)
    years = days / 365.25
    return years, days_list, altitude_list

if __name__ == "__main__":
    main()




