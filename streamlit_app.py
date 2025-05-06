# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import math
# import itertools

# # ------------------- Soil Layer Class -------------------
# class SoilLayer:
#     def __init__(self, phi, gamma, thickness, name="Layer"):
#         self.phi = phi
#         self.gamma = gamma
#         self.thickness = thickness
#         self.name = name

#     def ka(self):
#         phi_rad = math.radians(self.phi)
#         return (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))

# # ------------------- Pressure Calculation Functions -------------------
# def calculate_pressure_profile(layers, gwt_depth):
#     pressures = []
#     depth = 0
#     gamma_w = 9.81

#     for layer in layers:
#         ka = layer.ka()
#         top = depth
#         bottom = depth + layer.thickness

#         if gwt_depth is None:
#             gamma_eff = layer.gamma
#         else:
#             gamma_eff = layer.gamma if bottom <= gwt_depth else layer.gamma - gamma_w

#         pressures.append((top, ka * gamma_eff * top))
#         pressures.append((bottom, ka * gamma_eff * bottom))

#         depth = bottom

#     return pressures

# def total_force(layers, gwt_depth):
#     pressures = calculate_pressure_profile(layers, gwt_depth)
#     force = sum(0.5 * (p1 + p2) * (y2 - y1) for (y1, p1), (y2, p2) in zip(pressures[:-1], pressures[1:]))
#     return force

# def optimize_layers(layers, gwt_depth):
#     best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
#     return best_perm, total_force(best_perm, gwt_depth)

# # ------------------- Streamlit App -------------------
# st.title("🧱 Soil Layer Optimizer")

# st.markdown("""
# Upload a CSV file with the following columns:
# - `phi`: Internal friction angle (degrees)
# - `gamma`: Unit weight (kN/m³)
# - `thickness`: Layer thickness (m)
# - `name`: Name of the layer
# """)

# uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
# gwt_depth_input = st.text_input("🌊 Groundwater Table Depth (m):", value="")
# gwt_depth = float(gwt_depth_input) if gwt_depth_input.strip() else None

# if uploaded_file is not None:
#     try:
#         df = pd.read_csv(uploaded_file)

#         required_columns = ['phi', 'gamma', 'thickness', 'name']
#         if not all(col in df.columns for col in required_columns):
#             st.error("CSV file must contain columns: phi, gamma, thickness, name")
#         else:
#             layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]

#             original_force = total_force(layers, gwt_depth)
#             optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)

#             def format_table(layers):
#                 return pd.DataFrame({
#                     'Name': [layer.name for layer in layers],
#                     'φ (°)': [layer.phi for layer in layers],
#                     'γ (kN/m³)': [layer.gamma for layer in layers],
#                     'Thickness (m)': [layer.thickness for layer in layers]
#                 })

#             st.subheader("🔹 Original Layer Order")
#             st.dataframe(format_table(layers))
#             st.subheader("✅ Optimized Layer Order")
#             st.dataframe(format_table(optimized_layers))

#             st.markdown(f"**Original Force:** {original_force:.2f} kN/m")
#             st.markdown(f"**Optimized Force:** {optimized_force:.2f} kN/m")

#             # Plot
#             fig, axs = plt.subplots(1, 2, figsize=(12, 6))

#             for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
#                 pressures = calculate_pressure_profile(set_layers, gwt_depth)
#                 depths = [p[0] for p in pressures]
#                 sigmas = [p[1] for p in pressures]

#                 ax.plot(sigmas, depths, marker='o', label=title)
#                 ax.set_title(f"{title} Pressure Distribution")
#                 ax.set_xlabel("Pressure (kPa)")
#                 ax.set_ylabel("Depth (m)")
#                 ax.invert_yaxis()
#                 ax.grid(True)

#                 if gwt_depth is not None:
#                     ax.axhline(y=gwt_depth, color='blue', linestyle='--', label='GWT')

#                 ax.legend()

#             st.pyplot(fig)

#     except Exception as e:
#         st.error(f"Error processing file: {e}")



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import itertools

# ------------------- Soil Layer Class -------------------
class SoilLayer:
    def __init__(self, phi, gamma, thickness, name="Layer"):
        self.phi = phi
        self.gamma = gamma
        self.thickness = thickness
        self.name = name

    def ka(self):
        phi_rad = math.radians(self.phi)
        return (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))

# ------------------- Pressure Calculation Functions -------------------
def calculate_pressure_profile(layers, gwt_depth):
    pressures = []
    depth = 0
    gamma_w = 9.81

    for layer in layers:
        ka = layer.ka()
        top = depth
        bottom = depth + layer.thickness

        if gwt_depth is None:
            gamma_eff = layer.gamma
        else:
            gamma_eff = layer.gamma if bottom <= gwt_depth else layer.gamma - gamma_w

        pressures.append((top, ka * gamma_eff * top))
        pressures.append((bottom, ka * gamma_eff * bottom))

        depth = bottom

    return pressures

def total_force(layers, gwt_depth):
    pressures = calculate_pressure_profile(layers, gwt_depth)
    force = sum(0.5 * (p1 + p2) * (y2 - y1) for (y1, p1), (y2, p2) in zip(pressures[:-1], pressures[1:]))
    return force

def optimize_layers(layers, gwt_depth):
    best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
    return best_perm, total_force(best_perm, gwt_depth)

# ------------------- Streamlit App -------------------
st.set_page_config(page_title="Soil Layer Optimizer", layout="wide")
st.title("🧱 Soil Layer Optimizer")

with st.expander("📘 Theory - Rankine Earth Pressure & Optimization", expanded=True):
    st.markdown("""
    <style> .theory-box { background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; } </style>
    <div class="theory-box">
    <b>Rankine's Earth Pressure Theory</b> is used to calculate the lateral earth pressure exerted by soil. The <b>Active Earth Pressure Coefficient</b> \(K_a\) is calculated as:

    \[ K_a = \frac{1 - \sin(\phi)}{1 + \sin(\phi)} \]

    where \(\phi\) is the internal friction angle of the soil.

    This app calculates the total lateral earth pressure acting on a retaining structure due to a layered soil profile and explores <b>optimal layer arrangements</b> that minimize that total pressure.

    If a <b>groundwater table</b> is present, the effective unit weight of soil is reduced by the unit weight of water \(\gamma_w = 9.81 \text{ kN/m}^3\) below the water table, affecting pressure distribution.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
### 📂 Input Instructions
Upload a CSV file with the following columns:
- `phi`: Internal friction angle (degrees)
- `gamma`: Unit weight (kN/m³)
- `thickness`: Layer thickness (m)
- `name`: Name of the layer
""")

uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
gwt_depth = st.slider("🌊 Groundwater Table Depth (m):", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

gwt_active = st.checkbox("Include Groundwater Table Adjustment", value=True)
if not gwt_active:
    gwt_depth = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = ['phi', 'gamma', 'thickness', 'name']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV file must contain columns: phi, gamma, thickness, name")
        else:
            layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]

            original_force = total_force(layers, gwt_depth)
            optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)

            def format_table(layers):
                return pd.DataFrame({
                    'Name': [layer.name for layer in layers],
                    'φ (°)': [layer.phi for layer in layers],
                    'γ (kN/m³)': [layer.gamma for layer in layers],
                    'Thickness (m)': [layer.thickness for layer in layers]
                })

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔹 Original Layer Order")
                st.dataframe(format_table(layers), use_container_width=True)
            with col2:
                st.subheader("✅ Optimized Layer Order")
                st.dataframe(format_table(optimized_layers), use_container_width=True)

            st.markdown(f"**📉 Original Force:** `{original_force:.2f} kN/m`")
            st.markdown(f"**🧠 Optimized Force:** `{optimized_force:.2f} kN/m`")

            # Plot
            fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

            for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
                pressures = calculate_pressure_profile(set_layers, gwt_depth)
                depths = [p[0] for p in pressures]
                sigmas = [p[1] for p in pressures]

                ax.plot(sigmas, depths, marker='o', linestyle='-', color='darkgreen', label="Lateral Pressure")
                ax.set_title(f"{title} Pressure Distribution")
                ax.set_xlabel("Pressure (kPa)")
                ax.set_ylabel("Depth (m)")
                ax.invert_yaxis()
                ax.grid(True)

                if gwt_depth is not None:
                    ax.axhline(y=gwt_depth, color='blue', linestyle='--', label='GWT')

                ax.legend()

            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error processing file: {e}")
