import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import itertools

# ------------------- Soil Layer Class -------------------
class SoilLayer:
    def _init_(self, phi, gamma, thickness, name="Layer"):
        self.phi = phi
        self.gamma = gamma
        self.thickness = thickness
        self.name = name

    def ka(self):
        phi_rad = math.radians(self.phi)
        return (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))


# ------------------- Pressure Calculation -------------------
def calculate_pressure_profile(layers, gwt_depth=None):
    pressures = []
    depth = 0
    gamma_w = 9.81

    for layer in layers:
        ka = layer.ka()
        top = depth
        bottom = depth + layer.thickness

        if gwt_depth is not None:
            if top < gwt_depth < bottom:
                sigma_top = ka * layer.gamma * top
                sigma_gwt = ka * layer.gamma * gwt_depth
                gamma_eff = layer.gamma - gamma_w
                sigma_bottom = ka * (gamma_eff * bottom + gamma_w * (bottom - gwt_depth))
                pressures += [(top, sigma_top), (gwt_depth, sigma_gwt), (bottom, sigma_bottom)]
            elif bottom <= gwt_depth:
                sigma_top = ka * layer.gamma * top
                sigma_bottom = ka * layer.gamma * bottom
                pressures += [(top, sigma_top), (bottom, sigma_bottom)]
            else:
                gamma_eff = layer.gamma - gamma_w
                sigma_top = ka * (gamma_eff * top + gamma_w * (top - gwt_depth))
                sigma_bottom = ka * (gamma_eff * bottom + gamma_w * (bottom - gwt_depth))
                pressures += [(top, sigma_top), (bottom, sigma_bottom)]
        else:
            sigma_top = ka * layer.gamma * top
            sigma_bottom = ka * layer.gamma * bottom
            pressures += [(top, sigma_top), (bottom, sigma_bottom)]

        depth = bottom
    return pressures


def total_force(layers, gwt_depth=None):
    pressures = calculate_pressure_profile(layers, gwt_depth)
    return sum(0.5 * (p1 + p2) * (y2 - y1) for (y1, p1), (y2, p2) in zip(pressures[:-1], pressures[1:]))


def optimize_layers(layers, gwt_depth=None):
    best_perm = min(itertools.permutations(layers), key=lambda p: total_force(p, gwt_depth))
    return best_perm, total_force(best_perm, gwt_depth)


def plot_pressure_graphs(original_layers, optimized_layers, gwt_depth):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    for ax, layers, title in zip(axs, [original_layers, optimized_layers], ["Original", "Optimized"]):
        pressures = calculate_pressure_profile(layers, gwt_depth)
        depths = [d for d, _ in pressures]
        sigmas = [s for _, s in pressures]

        ax.plot(sigmas, depths, marker='o')
        ax.set_title(f"{title} Pressure Distribution")
        ax.set_xlabel("Active Earth Pressure (kPa)")
        ax.set_ylabel("Depth (m)")
        ax.invert_yaxis()
        if gwt_depth is not None:
            ax.axhline(y=gwt_depth, color='blue', linestyle='--', label="GWT")
            ax.legend()
        ax.grid()

    st.pyplot(fig)


# ------------------- Streamlit App -------------------
st.title("🧱 Soil Layer Optimizer (Rankine Earth Pressure)")
st.write("Upload a CSV file with columns: name, phi, gamma, thickness")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

gwt_input = st.text_input("Groundwater Table Depth (m):", placeholder="Leave empty if no GWT")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if not all(col in df.columns for col in ['phi', 'gamma', 'thickness', 'name']):
            st.error("CSV must contain columns: 'name', 'phi', 'gamma', 'thickness'")
        else:
            layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]
            gwt_depth = float(gwt_input) if gwt_input.strip() else None

            original_force = total_force(layers, gwt_depth)
            optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)

            st.subheader("📊 Layer Configurations")
            st.markdown("*Original Order:*")
            for layer in layers:
                st.write(f"{layer.name} | φ={layer.phi}° | γ={layer.gamma} kN/m³ | Thickness={layer.thickness} m")

            st.markdown("*Optimized Order:*")
            for layer in optimized_layers:
                st.write(f"{layer.name} | φ={layer.phi}° | γ={layer.gamma} kN/m³ | Thickness={layer.thickness} m")

            st.success(f"Total Active Force (Original): {original_force:.2f} kN/m")
            st.success(f"Total Active Force (Optimized): {optimized_force:.2f} kN/m")

            st.subheader("📈 Pressure Distribution")
            plot_pressure_graphs(layers, optimized_layers, gwt_depth)

    except Exception as e:
        st.error(f"Error processing file: {e}")
