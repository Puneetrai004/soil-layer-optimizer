# # import streamlit as st
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import math
# # import itertools

# # # ------------------- Soil Layer Class -------------------
# # class SoilLayer:
# #     def __init__(self, phi, gamma, thickness, name="Layer"):
# #         self.phi = phi
# #         self.gamma = gamma
# #         self.thickness = thickness
# #         self.name = name

# #     def ka(self):
# #         phi_rad = math.radians(self.phi)
# #         return (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))

# # # ------------------- Pressure Calculation Functions -------------------
# # def calculate_pressure_profile(layers, gwt_depth):
# #     pressures = []
# #     depth = 0
# #     gamma_w = 9.81

# #     for layer in layers:
# #         ka = layer.ka()
# #         top = depth
# #         bottom = depth + layer.thickness

# #         if gwt_depth is None:
# #             gamma_eff = layer.gamma
# #         else:
# #             gamma_eff = layer.gamma if bottom <= gwt_depth else layer.gamma - gamma_w

# #         pressures.append((top, ka * gamma_eff * top))
# #         pressures.append((bottom, ka * gamma_eff * bottom))

# #         depth = bottom

# #     return pressures

# # def total_force(layers, gwt_depth):
# #     pressures = calculate_pressure_profile(layers, gwt_depth)
# #     force = sum(0.5 * (p1 + p2) * (y2 - y1) for (y1, p1), (y2, p2) in zip(pressures[:-1], pressures[1:]))
# #     return force

# # def optimize_layers(layers, gwt_depth):
# #     best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
# #     return best_perm, total_force(best_perm, gwt_depth)

# # # ------------------- Streamlit App -------------------
# # st.title("🧱 Soil Layer Optimizer")

# # st.markdown("""
# # Upload a CSV file with the following columns:
# # - `phi`: Internal friction angle (degrees)
# # - `gamma`: Unit weight (kN/m³)
# # - `thickness`: Layer thickness (m)
# # - `name`: Name of the layer
# # """)

# # uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
# # gwt_depth_input = st.text_input("🌊 Groundwater Table Depth (m):", value="")
# # gwt_depth = float(gwt_depth_input) if gwt_depth_input.strip() else None

# # if uploaded_file is not None:
# #     try:
# #         df = pd.read_csv(uploaded_file)

# #         required_columns = ['phi', 'gamma', 'thickness', 'name']
# #         if not all(col in df.columns for col in required_columns):
# #             st.error("CSV file must contain columns: phi, gamma, thickness, name")
# #         else:
# #             layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]

# #             original_force = total_force(layers, gwt_depth)
# #             optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)

# #             def format_table(layers):
# #                 return pd.DataFrame({
# #                     'Name': [layer.name for layer in layers],
# #                     'φ (°)': [layer.phi for layer in layers],
# #                     'γ (kN/m³)': [layer.gamma for layer in layers],
# #                     'Thickness (m)': [layer.thickness for layer in layers]
# #                 })

# #             st.subheader("🔹 Original Layer Order")
# #             st.dataframe(format_table(layers))
# #             st.subheader("✅ Optimized Layer Order")
# #             st.dataframe(format_table(optimized_layers))

# #             st.markdown(f"**Original Force:** {original_force:.2f} kN/m")
# #             st.markdown(f"**Optimized Force:** {optimized_force:.2f} kN/m")

# #             # Plot
# #             fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# #             for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
# #                 pressures = calculate_pressure_profile(set_layers, gwt_depth)
# #                 depths = [p[0] for p in pressures]
# #                 sigmas = [p[1] for p in pressures]

# #                 ax.plot(sigmas, depths, marker='o', label=title)
# #                 ax.set_title(f"{title} Pressure Distribution")
# #                 ax.set_xlabel("Pressure (kPa)")
# #                 ax.set_ylabel("Depth (m)")
# #                 ax.invert_yaxis()
# #                 ax.grid(True)

# #                 if gwt_depth is not None:
# #                     ax.axhline(y=gwt_depth, color='blue', linestyle='--', label='GWT')

# #                 ax.legend()

# #             st.pyplot(fig)

# #     except Exception as e:
# #         st.error(f"Error processing file: {e}")





# # 1st Updated code


# # import streamlit as st
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import math
# # import itertools
# # import numpy as np

# # # Set page configuration
# # st.set_page_config(
# #     page_title="Soil Layer Optimizer",
# #     page_icon="🧱",
# #     layout="wide"
# # )

# # # Custom CSS for better styling
# # st.markdown("""
# # <style>
# #     .main-header {
# #         font-size: 2.5rem;
# #         color: #1E3A8A;
# #         text-align: center;
# #         margin-bottom: 1rem;
# #     }
# #     .sub-header {
# #         font-size: 1.5rem;
# #         color: #2563EB;
# #         margin-top: 1.5rem;
# #         margin-bottom: 0.5rem;
# #     }
# #     .info-box {
# #         background-color: #EFF6FF;
# #         padding: 1rem;
# #         border-radius: 0.5rem;
# #         border-left: 4px solid #3B82F6;
# #         margin-bottom: 1rem;
# #     }
# #     .result-box {
# #         background-color: #ECFDF5;
# #         padding: 1rem;
# #         border-radius: 0.5rem;
# #         border-left: 4px solid #10B981;
# #         margin-top: 1rem;
# #         margin-bottom: 1rem;
# #     }
# #     .theory-box {
# #         background-color: #FEF3C7;
# #         padding: 1.5rem;
# #         border-radius: 0.5rem;
# #         border-left: 4px solid #F59E0B;
# #         margin-top: 1rem;
# #         margin-bottom: 1rem;
# #     }
# #     .stTabs [data-baseweb="tab-list"] {
# #         gap: 10px;
# #     }
# #     .stTabs [data-baseweb="tab"] {
# #         height: 50px;
# #         white-space: pre-wrap;
# #         background-color: #F3F4F6;
# #         border-radius: 4px 4px 0px 0px;
# #         gap: 1px;
# #         padding-top: 10px;
# #         padding-bottom: 10px;
# #     }
# #     .stTabs [aria-selected="true"] {
# #         background-color: #DBEAFE;
# #         border-bottom: 2px solid #3B82F6;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ------------------- Soil Layer Class -------------------
# # class SoilLayer:
# #     def __init__(self, phi, gamma, thickness, name="Layer"):
# #         self.phi = phi
# #         self.gamma = gamma
# #         self.thickness = thickness
# #         self.name = name

# #     def ka(self):
# #         phi_rad = math.radians(self.phi)
# #         return (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))

# # # ------------------- Pressure Calculation Functions -------------------
# # def calculate_pressure_profile(layers, gwt_depth):
# #     pressures = []
# #     depth = 0
# #     gamma_w = 9.81

# #     for layer in layers:
# #         ka = layer.ka()
# #         top = depth
# #         bottom = depth + layer.thickness

# #         # Calculate effective unit weight based on GWT
# #         if gwt_depth is None:
# #             gamma_eff = layer.gamma
# #         else:
# #             if top >= gwt_depth:
# #                 # Below GWT
# #                 gamma_eff = layer.gamma - gamma_w
# #             elif bottom <= gwt_depth:
# #                 # Above GWT
# #                 gamma_eff = layer.gamma
# #             else:
# #                 # Layer intersects GWT
# #                 # For the part above GWT
# #                 pressures.append((top, ka * layer.gamma * top))
# #                 # At GWT
# #                 pressures.append((gwt_depth, ka * layer.gamma * gwt_depth))
# #                 # For the part below GWT, continue with effective weight
# #                 gamma_eff = layer.gamma - gamma_w
# #                 top = gwt_depth

# #         pressures.append((top, ka * gamma_eff * top))
# #         pressures.append((bottom, ka * gamma_eff * bottom))

# #         depth = bottom

# #     # Remove duplicates and sort by depth
# #     unique_pressures = []
# #     seen_depths = set()
# #     for p in pressures:
# #         if p[0] not in seen_depths:
# #             unique_pressures.append(p)
# #             seen_depths.add(p[0])
    
# #     return sorted(unique_pressures, key=lambda x: x[0])

# # def total_force(layers, gwt_depth):
# #     pressures = calculate_pressure_profile(layers, gwt_depth)
# #     force = sum(0.5 * (p1 + p2) * (y2 - y1) for (y1, p1), (y2, p2) in zip(pressures[:-1], pressures[1:]))
# #     return force

# # def optimize_layers(layers, gwt_depth):
# #     best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
# #     return best_perm, total_force(best_perm, gwt_depth)

# # # ------------------- Streamlit App -------------------
# # st.markdown('<h1 class="main-header">🧱 Soil Layer Optimizer</h1>', unsafe_allow_html=True)

# # tabs = st.tabs(["📊 Optimizer", "📚 Theory", "ℹ️ Help"])

# # with tabs[0]:
# #     col1, col2 = st.columns([2, 1])
    
# #     with col1:
# #         st.markdown('<div class="info-box">', unsafe_allow_html=True)
# #         st.markdown("""
# #         Upload a CSV file with the following columns:
# #         - `phi`: Internal friction angle (degrees)
# #         - `gamma`: Unit weight (kN/m³)
# #         - `thickness`: Layer thickness (m)
# #         - `name`: Name of the layer
# #         """)
# #         st.markdown('</div>', unsafe_allow_html=True)
        
# #         uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
    
# #     with col2:
# #         st.markdown('<div class="info-box">', unsafe_allow_html=True)
# #         st.markdown("### Parameters")
# #         gwt_depth_input = st.text_input("🌊 Groundwater Table Depth (m):", value="")
# #         gwt_depth = float(gwt_depth_input) if gwt_depth_input.strip() else None
        
# #         if gwt_depth is not None:
# #             st.info(f"GWT set at {gwt_depth} m depth")
# #         else:
# #             st.info("No groundwater table defined")
# #         st.markdown('</div>', unsafe_allow_html=True)

# #     if uploaded_file is not None:
# #         try:
# #             df = pd.read_csv(uploaded_file)

# #             required_columns = ['phi', 'gamma', 'thickness', 'name']
# #             if not all(col in df.columns for col in required_columns):
# #                 st.error("CSV file must contain columns: phi, gamma, thickness, name")
# #             else:
# #                 layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]

# #                 original_force = total_force(layers, gwt_depth)
# #                 optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)
# #                 reduction_percentage = ((original_force - optimized_force) / original_force) * 100

# #                 def format_table(layers):
# #                     return pd.DataFrame({
# #                         'Name': [layer.name for layer in layers],
# #                         'φ (°)': [layer.phi for layer in layers],
# #                         'γ (kN/m³)': [layer.gamma for layer in layers],
# #                         'Thickness (m)': [layer.thickness for layer in layers],
# #                         'Ka': [round(layer.ka(), 4) for layer in layers]
# #                     })

# #                 col1, col2 = st.columns(2)
                
# #                 with col1:
# #                     st.markdown('<h3 class="sub-header">🔹 Original Layer Order</h3>', unsafe_allow_html=True)
# #                     st.dataframe(format_table(layers), use_container_width=True)
                
# #                 with col2:
# #                     st.markdown('<h3 class="sub-header">✅ Optimized Layer Order</h3>', unsafe_allow_html=True)
# #                     st.dataframe(format_table(optimized_layers), use_container_width=True)

# #                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
# #                 col1, col2, col3 = st.columns(3)
# #                 col1.metric("Original Force", f"{original_force:.2f} kN/m")
# #                 col2.metric("Optimized Force", f"{optimized_force:.2f} kN/m")
# #                 col3.metric("Reduction", f"{reduction_percentage:.2f}%", f"-{reduction_percentage:.2f}%")
# #                 st.markdown('</div>', unsafe_allow_html=True)

# #                 # Plot
# #                 fig, axs = plt.subplots(1, 2, figsize=(12, 8))
# #                 fig.suptitle("Earth Pressure Distribution", fontsize=16)

# #                 for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
# #                     pressures = calculate_pressure_profile(set_layers, gwt_depth)
# #                     depths = [p[0] for p in pressures]
# #                     sigmas = [p[1] for p in pressures]

# #                     # Fill the area under the pressure curve
# #                     ax.fill_betweenx(depths, 0, sigmas, alpha=0.3, color='skyblue')
# #                     ax.plot(sigmas, depths, marker='o', color='blue', linewidth=2)
                    
# #                     ax.set_title(f"{title} Pressure Distribution", fontsize=14)
# #                     ax.set_xlabel("Pressure (kPa)", fontsize=12)
# #                     ax.set_ylabel("Depth (m)", fontsize=12)
# #                     ax.invert_yaxis()
# #                     ax.grid(True, linestyle='--', alpha=0.7)
                    
# #                     # Add layer boundaries
# #                     depth = 0
# #                     for i, layer in enumerate(set_layers):
# #                         depth += layer.thickness
# #                         ax.axhline(y=depth, color='gray', linestyle='-', alpha=0.5)
# #                         # Add layer name
# #                         mid_depth = depth - layer.thickness/2
# #                         ax.text(max(sigmas)*0.05, mid_depth, layer.name, 
# #                                 verticalalignment='center', fontsize=10)

# #                     if gwt_depth is not None:
# #                         ax.axhline(y=gwt_depth, color='blue', linestyle='--', linewidth=2)
# #                         ax.text(max(sigmas)*0.8, gwt_depth, 'GWT', color='blue', 
# #                                 verticalalignment='bottom', fontsize=10)

# #                 plt.tight_layout(rect=[0, 0, 1, 0.95])
# #                 st.pyplot(fig)

# #         except Exception as e:
# #             st.error(f"Error processing file: {e}")

# # with tabs[1]:
# #     st.markdown('<div class="theory-box">', unsafe_allow_html=True)
# #     st.markdown("## Rankine's Active Earth Pressure Theory")
# #     st.markdown("""
# #     Rankine's theory assumes a uniform soil mass and ignores friction between the wall and soil. The key principles include:

# #     ### Assumptions
# #     1. Soil is **homogeneous and isotropic**.
# #     2. Soil mass is **semi-infinite**.
# #     3. The failure surface follows a **plane rupture**.
# #     4. The retaining wall is **smooth and vertical**.
# #     5. No wall friction is considered.
# #     6. Soil obeys **Mohr-Coulomb failure criterion**.
# #     7. The pressure acts parallel to the ground surface.

# #     ### Formula for Active Earth Pressure
# #     Rankine's active earth pressure coefficient (Ka) is given by:

# #     Ka = (1 - sin φ) / (1 + sin φ)

# #     Where:
# #     - Ka = Active earth pressure coefficient
# #     - φ = Angle of internal friction of soil

# #     The active earth pressure at depth h is:

# #     Pa = Ka × γ × h

# #     Where:
# #     - Pa = Lateral earth pressure per unit width
# #     - γ = Unit weight of soil
# #     - h = Depth of soil

# #     ### Total Active Force Acting on the Wall
# #     Fa = (1/2) × Ka × γ × H²

# #     Where:
# #     - Fa = Total active force
# #     - H = Height of the wall

# #     This force acts **at a height of H/3** from the base of the wall.
# #     """)
# #     st.markdown('</div>', unsafe_allow_html=True)

# # with tabs[2]:
# #     st.markdown('<div class="info-box">', unsafe_allow_html=True)
# #     st.markdown("## How to Use This Tool")
# #     st.markdown("""
# #     1. **Prepare your CSV file** with the following columns:
# #        - `phi`: Internal friction angle in degrees
# #        - `gamma`: Unit weight in kN/m³
# #        - `thickness`: Layer thickness in meters
# #        - `name`: Name of the soil layer
    
# #     2. **Upload the CSV file** using the file uploader.
    
# #     3. **Enter the groundwater table depth** (optional):
# #        - Leave blank if there is no groundwater
# #        - Enter the depth in meters from the top surface
    
# #     4. **View the results**:
# #        - Original vs. optimized layer arrangement
# #        - Force reduction achieved by optimization
# #        - Pressure distribution graphs
    
# #     ### Sample CSV Format:
# #     ```
# #     name,phi,gamma,thickness
# #     Sand,30,18,2
# #     Clay,20,19,3
# #     Gravel,35,20,2.5
# #     ```
# #     """)
# #     st.markdown('</div>', unsafe_allow_html=True)
    
# #     st.markdown('<div class="info-box">', unsafe_allow_html=True)
# #     st.markdown("## About the Optimization")
# #     st.markdown("""
# #     This tool optimizes the arrangement of soil layers to minimize the lateral earth pressure on a retaining wall.
    
# #     The optimization works by:
# #     1. Calculating the active earth pressure for each possible arrangement of layers
# #     2. Finding the arrangement that produces the minimum total force
# #     3. Comparing the original and optimized arrangements
    
# #     **Note**: The optimization considers all possible permutations of layers, so it may take longer for a large number of layers.
# #     """)
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # Add footer
# # st.markdown("""
# # ---
# # <p style="text-align: center; color: gray; font-size: 0.8rem;">
# # Soil Layer Optimizer | Built with Streamlit | © 2025
# # </p>
# # """, unsafe_allow_html=True)

# Trial 1 - Updating code

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import math
# import itertools
# import numpy as np

# # Set page configuration
# st.set_page_config(
#     page_title="Soil Layer Optimizer",
#     page_icon="🧱",
#     layout="wide"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #1E3A8A;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         color: #2563EB;
#         margin-top: 1.5rem;
#         margin-bottom: 0.5rem;
#     }
#     .info-box {
#         background-color: #EFF6FF;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #3B82F6;
#         margin-bottom: 1rem;
#     }
#     .result-box {
#         background-color: #ECFDF5;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #10B981;
#         margin-top: 1rem;
#         margin-bottom: 1rem;
#     }
#     .theory-box {
#         background-color: #FEF3C7;
#         padding: 1.5rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #F59E0B;
#         margin-top: 1rem;
#         margin-bottom: 1rem;
#     }
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 10px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px;
#         white-space: pre-wrap;
#         background-color: #F3F4F6;
#         border-radius: 4px 4px 0px 0px;
#         gap: 1px;
#         padding-top: 10px;
#         padding-bottom: 10px;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: #DBEAFE;
#         border-bottom: 2px solid #3B82F6;
#     }
# </style>
# """, unsafe_allow_html=True)

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
    
#     # Track cumulative vertical stress
#     sigma_v = 0
    
#     for i, layer in enumerate(layers):
#         ka = layer.ka()
#         top_depth = depth
#         bottom_depth = depth + layer.thickness
        
#         # Calculate effective unit weight based on GWT
#         if gwt_depth is None:
#             gamma_eff = layer.gamma
#         else:
#             if top_depth >= gwt_depth:
#                 # Fully below GWT
#                 gamma_eff = layer.gamma - gamma_w
#             elif bottom_depth <= gwt_depth:
#                 # Fully above GWT
#                 gamma_eff = layer.gamma
#             else:
#                 # Layer intersects GWT
#                 # For the part above GWT
#                 sigma_v_at_gwt = sigma_v + layer.gamma * (gwt_depth - top_depth)
#                 pressures.append((top_depth, ka * sigma_v))
#                 pressures.append((gwt_depth, ka * sigma_v_at_gwt))
                
#                 # Update sigma_v at GWT
#                 sigma_v = sigma_v_at_gwt
                
#                 # For the part below GWT, continue with effective weight
#                 gamma_eff = layer.gamma - gamma_w
#                 top_depth = gwt_depth
        
#         # Add pressure at top of layer (using previous layer's Ka if not the first layer)
#         if i > 0 and len(pressures) > 0 and abs(top_depth - pressures[-1][0]) < 1e-6:
#             # We're at a layer boundary, add pressure point with new Ka
#             pressures.append((top_depth, ka * sigma_v))
#         else:
#             # Regular point
#             pressures.append((top_depth, ka * sigma_v))
        
#         # Update sigma_v at bottom of layer
#         sigma_v += gamma_eff * layer.thickness
        
#         # Add pressure at bottom of layer
#         pressures.append((bottom_depth, ka * sigma_v))
        
#         # Update current depth
#         depth = bottom_depth
    
#     # Add hydrostatic pressure if GWT exists
#     if gwt_depth is not None:
#         hydrostatic_pressures = []
#         for depth, pressure in pressures:
#             if depth > gwt_depth:
#                 hydrostatic_pressures.append((depth, pressure + gamma_w * (depth - gwt_depth)))
#             else:
#                 hydrostatic_pressures.append((depth, pressure))
#         pressures = hydrostatic_pressures
    
#     return pressures

# def total_force(layers, gwt_depth):
#     pressures = calculate_pressure_profile(layers, gwt_depth)
#     force = 0
    
#     for i in range(len(pressures) - 1):
#         depth1, pressure1 = pressures[i]
#         depth2, pressure2 = pressures[i + 1]
        
#         # Calculate area of the trapezoid
#         force += 0.5 * (pressure1 + pressure2) * (depth2 - depth1)
    
#     return force

# def optimize_layers(layers, gwt_depth):
#     best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
#     return best_perm, total_force(best_perm, gwt_depth)

# # ------------------- Streamlit App -------------------
# st.markdown('<h1 class="main-header">🧱 Soil Layer Optimizer</h1>', unsafe_allow_html=True)

# tabs = st.tabs(["📊 Optimizer", "📚 Theory", "ℹ️ Help"])

# with tabs[0]:
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown('<div class="info-box">', unsafe_allow_html=True)
#         st.markdown("""
#         Upload a CSV file with the following columns:
#         - `phi`: Internal friction angle (degrees)
#         - `gamma`: Unit weight (kN/m³)
#         - `thickness`: Layer thickness (m)
#         - `name`: Name of the layer
#         """)
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
    
#     with col2:
#         st.markdown('<div class="info-box">', unsafe_allow_html=True)
#         st.markdown("### Parameters")
#         gwt_depth_input = st.text_input("🌊 Groundwater Table Depth (m):", value="")
#         gwt_depth = float(gwt_depth_input) if gwt_depth_input.strip() else None
        
#         if gwt_depth is not None:
#             st.info(f"GWT set at {gwt_depth} m depth")
#         else:
#             st.info("No groundwater table defined")
#         st.markdown('</div>', unsafe_allow_html=True)

#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file)

#             required_columns = ['phi', 'gamma', 'thickness', 'name']
#             if not all(col in df.columns for col in required_columns):
#                 st.error("CSV file must contain columns: phi, gamma, thickness, name")
#             else:
#                 layers = [SoilLayer(row['phi'], row['gamma'], row['thickness'], row['name']) for _, row in df.iterrows()]

#                 original_force = total_force(layers, gwt_depth)
#                 optimized_layers, optimized_force = optimize_layers(layers, gwt_depth)
#                 reduction_percentage = ((original_force - optimized_force) / original_force) * 100

#                 def format_table(layers):
#                     return pd.DataFrame({
#                         'Name': [layer.name for layer in layers],
#                         'φ (°)': [layer.phi for layer in layers],
#                         'γ (kN/m³)': [layer.gamma for layer in layers],
#                         'Thickness (m)': [layer.thickness for layer in layers],
#                         'Ka': [round(layer.ka(), 4) for layer in layers]
#                     })

#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.markdown('<h3 class="sub-header">🔹 Original Layer Order</h3>', unsafe_allow_html=True)
#                     st.dataframe(format_table(layers), use_container_width=True)
                
#                 with col2:
#                     st.markdown('<h3 class="sub-header">✅ Optimized Layer Order</h3>', unsafe_allow_html=True)
#                     st.dataframe(format_table(optimized_layers), use_container_width=True)

#                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                 col1, col2, col3 = st.columns(3)
#                 col1.metric("Original Force", f"{original_force:.2f} kN/m")
#                 col2.metric("Optimized Force", f"{optimized_force:.2f} kN/m")
#                 col3.metric("Reduction", f"{reduction_percentage:.2f}%", f"-{reduction_percentage:.2f}%")
#                 st.markdown('</div>', unsafe_allow_html=True)

#                 # Plot
#                 fig, axs = plt.subplots(1, 2, figsize=(12, 8))
#                 fig.suptitle("Earth Pressure Distribution", fontsize=16)

#                 for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
#                     pressures = calculate_pressure_profile(set_layers, gwt_depth)
#                     depths = [p[0] for p in pressures]
#                     sigmas = [p[1] for p in pressures]

#                     # Fill the area under the pressure curve
#                     ax.fill_betweenx(depths, 0, sigmas, alpha=0.3, color='skyblue')
#                     ax.plot(sigmas, depths, marker='o', color='blue', linewidth=2)
                    
#                     # Add layer boundaries with different colors
#                     depth = 0
#                     colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
                    
#                     for i, layer in enumerate(set_layers):
#                         # Add shaded region for each layer
#                         layer_top = depth
#                         layer_bottom = depth + layer.thickness
#                         ax.axhspan(layer_top, layer_bottom, alpha=0.1, color=colors[i % len(colors)])
                        
#                         # Add horizontal line at layer boundary
#                         depth += layer.thickness
#                         ax.axhline(y=depth, color='gray', linestyle='-', alpha=0.5)
                        
#                         # Add layer name
#                         mid_depth = depth - layer.thickness/2
#                         ax.text(max(sigmas)*0.05, mid_depth, layer.name, 
#                                 verticalalignment='center', fontsize=10)
                        
#                         # Add Ka value
#                         ax.text(max(sigmas)*0.7, mid_depth, f"Ka={layer.ka():.4f}", 
#                                 verticalalignment='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
                    
#                     # Add groundwater table if exists
#                     if gwt_depth is not None:
#                         ax.axhline(y=gwt_depth, color='blue', linestyle='--', linewidth=2)
#                         ax.text(max(sigmas)*0.8, gwt_depth, 'GWT', color='blue', 
#                                 verticalalignment='bottom', fontsize=10)
                    
#                     ax.set_title(f"{title} Pressure Distribution", fontsize=14)
#                     ax.set_xlabel("Pressure (kPa)", fontsize=12)
#                     ax.set_ylabel("Depth (m)", fontsize=12)
#                     ax.invert_yaxis()
#                     ax.grid(True, linestyle='--', alpha=0.7)

#                 plt.tight_layout(rect=[0, 0, 1, 0.95])
#                 st.pyplot(fig)

#         except Exception as e:
#             st.error(f"Error processing file: {e}")

# with tabs[1]:
#     st.markdown('<div class="theory-box">', unsafe_allow_html=True)
#     st.markdown("## Rankine's Active Earth Pressure Theory")
#     st.markdown("""
#     Rankine's theory assumes a uniform soil mass and ignores friction between the wall and soil. The key principles include:

#     ### Assumptions
#     1. Soil is **homogeneous and isotropic**.
#     2. Soil mass is **semi-infinite**.
#     3. The failure surface follows a **plane rupture**.
#     4. The retaining wall is **smooth and vertical**.
#     5. No wall friction is considered.
#     6. Soil obeys **Mohr-Coulomb failure criterion**.
#     7. The pressure acts parallel to the ground surface.

#     ### Formula for Active Earth Pressure
#     Rankine's active earth pressure coefficient (Ka) is given by:

#     Ka = (1 - sin φ) / (1 + sin φ)

#     Where:
#     - Ka = Active earth pressure coefficient
#     - φ = Angle of internal friction of soil

#     The active earth pressure at depth h is:

#     Pa = Ka × γ × h

#     Where:
#     - Pa = Lateral earth pressure per unit width
#     - γ = Unit weight of soil
#     - h = Depth of soil

#     ### Total Active Force Acting on the Wall
#     Fa = (1/2) × Ka × γ × H²

#     Where:
#     - Fa = Total active force
#     - H = Height of the wall

#     This force acts **at a height of H/3** from the base of the wall.
    
#     ### Layered Soil Profile
#     For a layered soil profile, the pressure distribution changes at each layer boundary due to:
#     1. Different friction angles (φ) resulting in different Ka values
#     2. Different unit weights (γ)
    
#     The pressure at any depth is calculated as:
#     Pa = Ka × σv
    
#     Where σv is the vertical stress at that depth.
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)

# with tabs[2]:
#     st.markdown('<div class="info-box">', unsafe_allow_html=True)
#     st.markdown("## How to Use This Tool")
#     st.markdown("""
#     1. **Prepare your CSV file** with the following columns:
#        - `phi`: Internal friction angle in degrees
#        - `gamma`: Unit weight in kN/m³
#        - `thickness`: Layer thickness in meters
#        - `name`: Name of the soil layer
    
#     2. **Upload the CSV file** using the file uploader.
    
#     3. **Enter the groundwater table depth** (optional):
#        - Leave blank if there is no groundwater
#        - Enter the depth in meters from the top surface
    
#     4. **View the results**:
#        - Original vs. optimized layer arrangement
#        - Force reduction achieved by optimization
#        - Pressure distribution graphs
    
#     ### Sample CSV Format:
#     ```
#     name,phi,gamma,thickness
#     Dense Sand,30,18,2
#     Silty Sand,25,17,1.5
#     Soft Clay,20,16,1
#     Coarse Sand,35,19,2.5
#     Loamy Soil,18,16.5,1.8
#     ```
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="info-box">', unsafe_allow_html=True)
#     st.markdown("## About the Optimization")
#     st.markdown("""
#     This tool optimizes the arrangement of soil layers to minimize the lateral earth pressure on a retaining wall.
    
#     The optimization works by:
#     1. Calculating the active earth pressure for each possible arrangement of layers
#     2. Finding the arrangement that produces the minimum total force
#     3. Comparing the original and optimized arrangements
    
#     **Note**: The optimization considers all possible permutations of layers, so it may take longer for a large number of layers.
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)

# # Add footer
# st.markdown("""
# ---
# <p style="text-align: center; color: gray; font-size: 0.8rem;">
# Soil Layer Optimizer | Built with Streamlit | © 2025
# </p>
# """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import itertools
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Soil Layer Optimizer",
    page_icon="🧱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #ECFDF5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .theory-box {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F59E0B;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #DBEAFE;
        border-bottom: 2px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- Soil Layer Class -------------------
class SoilLayer:
    def __init__(self, phi, gamma, thickness, name="Layer"):
        self.phi = phi
        self.gamma = gamma
        self.thickness = thickness
        self.name = name

    def ka(self):
        phi_rad = math.radians(self.phi)
        return math.tan(math.radians(45 - self.phi/2))**2

# ------------------- Pressure Calculation Functions -------------------
def calculate_pressure_profile(layers, gwt_depth):
    gamma_w = 9.81  # Unit weight of water in kN/m³
    
    # Create detailed pressure profile for plotting
    depths = []
    pressures = []
    
    cumulative_depth = 0
    cumulative_vertical_stress = 0
    
    for i, layer in enumerate(layers):
        ka = layer.ka()
        layer_top = cumulative_depth
        layer_bottom = cumulative_depth + layer.thickness
        
        # Add point at the top of the layer
        if i > 0 and len(depths) > 0:
            # Add a point with the new Ka at the layer boundary
            depths.append(layer_top)
            pressures.append(ka * cumulative_vertical_stress)
        else:
            depths.append(layer_top)
            pressures.append(ka * cumulative_vertical_stress)
        
        # Calculate points within the layer
        if gwt_depth is not None and layer_top < gwt_depth < layer_bottom:
            # Layer intersects with GWT
            
            # Points above GWT
            z_above = np.linspace(layer_top, gwt_depth, 50)
            for z in z_above:
                local_depth = z - layer_top
                vertical_stress = cumulative_vertical_stress + layer.gamma * local_depth
                depths.append(z)
                pressures.append(ka * vertical_stress)
            
            # Points below GWT
            z_below = np.linspace(gwt_depth, layer_bottom, 50)
            for z in z_below:
                local_depth_above_gwt = gwt_depth - layer_top
                local_depth_below_gwt = z - gwt_depth
                vertical_stress = (cumulative_vertical_stress + 
                                  layer.gamma * local_depth_above_gwt + 
                                  (layer.gamma - gamma_w) * local_depth_below_gwt)
                depths.append(z)
                pressures.append(ka * vertical_stress)
        else:
            # Layer doesn't intersect GWT
            z_values = np.linspace(layer_top, layer_bottom, 100)
            for z in z_values:
                local_depth = z - layer_top
                if gwt_depth is not None and z > gwt_depth:
                    # Below GWT
                    if layer_top >= gwt_depth:
                        # Entire layer is below GWT
                        vertical_stress = cumulative_vertical_stress + (layer.gamma - gamma_w) * local_depth
                    else:
                        # Should not reach here as this case is handled above
                        pass
                else:
                    # Above GWT
                    vertical_stress = cumulative_vertical_stress + layer.gamma * local_depth
                
                depths.append(z)
                pressures.append(ka * vertical_stress)
        
        # Update cumulative values for next layer
        if gwt_depth is not None and layer_bottom > gwt_depth:
            if layer_top >= gwt_depth:
                # Entire layer is below GWT
                cumulative_vertical_stress += (layer.gamma - gamma_w) * layer.thickness
            else:
                # Layer intersects GWT
                above_gwt = gwt_depth - layer_top
                below_gwt = layer_bottom - gwt_depth
                cumulative_vertical_stress += (layer.gamma * above_gwt + 
                                             (layer.gamma - gamma_w) * below_gwt)
        else:
            cumulative_vertical_stress += layer.gamma * layer.thickness
        
        cumulative_depth = layer_bottom
    
    return list(zip(depths, pressures))

def total_force(layers, gwt_depth):
    pressure_profile = calculate_pressure_profile(layers, gwt_depth)
    depths = [p[0] for p in pressure_profile]
    pressures = [p[1] for p in pressure_profile]
    
    force = 0
    for i in range(len(depths) - 1):
        h = depths[i+1] - depths[i]
        avg_pressure = (pressures[i] + pressures[i+1]) / 2
        force += avg_pressure * h
    
    return force

def optimize_layers(layers, gwt_depth):
    best_perm = min(itertools.permutations(layers), key=lambda perm: total_force(perm, gwt_depth))
    return best_perm, total_force(best_perm, gwt_depth)

# ------------------- Streamlit App -------------------
st.markdown('<h1 class="main-header">🧱 Soil Layer Optimizer</h1>', unsafe_allow_html=True)

tabs = st.tabs(["📊 Optimizer", "📚 Theory", "ℹ️ Help"])

with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        Upload a CSV file with the following columns:
        - `phi`: Internal friction angle (degrees)
        - `gamma`: Unit weight (kN/m³)
        - `thickness`: Layer thickness (m)
        - `name`: Name of the layer
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### Parameters")
        gwt_depth_input = st.text_input("🌊 Groundwater Table Depth (m):", value="")
        gwt_depth = float(gwt_depth_input) if gwt_depth_input.strip() else None
        
        if gwt_depth is not None:
            st.info(f"GWT set at {gwt_depth} m depth")
        else:
            st.info("No groundwater table defined")
        st.markdown('</div>', unsafe_allow_html=True)

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
                reduction_percentage = ((original_force - optimized_force) / original_force) * 100

                def format_table(layers):
                    return pd.DataFrame({
                        'Name': [layer.name for layer in layers],
                        'φ (°)': [layer.phi for layer in layers],
                        'γ (kN/m³)': [layer.gamma for layer in layers],
                        'Thickness (m)': [layer.thickness for layer in layers],
                        'Ka': [round(layer.ka(), 4) for layer in layers]
                    })

                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<h3 class="sub-header">🔹 Original Layer Order</h3>', unsafe_allow_html=True)
                    st.dataframe(format_table(layers), use_container_width=True)
                
                with col2:
                    st.markdown('<h3 class="sub-header">✅ Optimized Layer Order</h3>', unsafe_allow_html=True)
                    st.dataframe(format_table(optimized_layers), use_container_width=True)

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Force", f"{original_force:.2f} kN/m")
                col2.metric("Optimized Force", f"{optimized_force:.2f} kN/m")
                col3.metric("Reduction", f"{reduction_percentage:.2f}%", f"-{reduction_percentage:.2f}%")
                st.markdown('</div>', unsafe_allow_html=True)

                # Plot
                fig, axs = plt.subplots(1, 2, figsize=(12, 10))
                fig.suptitle("Rankine Active Earth Pressure with Groundwater Table", fontsize=16)

                for ax, set_layers, title in zip(axs, [layers, optimized_layers], ["Original", "Optimized"]):
                    colors = ['blue', 'green', 'red', 'purple', 'orange']
                    
                    cumulative_depth = 0
                    cumulative_vertical_stress = 0
                    sigma_prev = 0
                    
                    mid_x = -5  # Where to draw vertical thickness annotations
                    gamma_w = 9.81  # Unit weight of water
                    
                    # Set x-limits to include the mid_x for annotations
                    ax.set_xlim(mid_x - 5, None)
                    
                    for i, layer in enumerate(set_layers):
                        h = layer.thickness
                        gamma = layer.gamma
                        phi = layer.phi
                        name = layer.name
                        
                        Ka = layer.ka()
                        
                        # Calculate points for this layer
                        z_local = np.linspace(0, h, 100)
                        z_absolute = cumulative_depth + z_local
                        
                        vertical_stress = np.zeros_like(z_local)
                        for j, depth in enumerate(z_absolute):
                            if gwt_depth is None or depth <= gwt_depth:
                                vertical_stress[j] = gamma * z_local[j] + cumulative_vertical_stress
                            else:
                                # Below groundwater table, use submerged unit weight
                                if cumulative_depth >= gwt_depth:
                                    # Layer entirely below GWT
                                    vertical_stress[j] = (gamma - gamma_w) * z_local[j] + cumulative_vertical_stress
                                else:
                                    # Layer intersects GWT
                                    above_gwt = gwt_depth - cumulative_depth
                                    below_gwt = z_local[j] - above_gwt
                                    
                                    if below_gwt <= 0:
                                        # This point is above GWT
                                        vertical_stress[j] = gamma * z_local[j] + cumulative_vertical_stress
                                    else:
                                        # This point is below GWT
                                        vertical_stress[j] = (gamma * above_gwt + 
                                                            (gamma - gamma_w) * below_gwt + 
                                                            cumulative_vertical_stress)
                        
                        sigma_a = Ka * vertical_stress
                        
                        # Plot the lateral pressure curve
                        ax.plot(sigma_a, z_absolute, color=colors[i % len(colors)], 
                               label=f"{name} (ϕ={phi}°, γ={gamma} kN/m³)")
                        
                        # Horizontal dashed connector at layer boundary
                        if i > 0:
                            ax.hlines(cumulative_depth, sigma_prev, sigma_a[0], 
                                    colors='black', linestyles='dashed', linewidth=1)
                        
                        # Horizontal extension to show pressure value
                        sigma_end = sigma_a[-1]
                        z_end = z_absolute[-1]
                        ax.hlines(z_end, 0, sigma_end, colors='gray', linestyles='dotted', linewidth=1)
                        
                        # Horizontal stress label
                        ax.text(sigma_end / 2, z_end + 0.2, f"{sigma_end:.1f} kPa", 
                               fontsize=10, ha='center', color=colors[i % len(colors)])
                        
                        # Vertical depth marker (thickness label)
                        z_mid = cumulative_depth + h / 2
                        ax.vlines(mid_x, cumulative_depth, cumulative_depth + h, 
                                colors='black', linestyles='solid')
                        ax.text(mid_x - 1, z_mid, f"{h} m", va='center', ha='center', 
                               fontsize=10, rotation=90, 
                               bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round'))
                        
                        # Update values for next layer
                        sigma_prev = sigma_end
                        if gwt_depth is not None and z_end > gwt_depth:
                            if cumulative_depth >= gwt_depth:
                                # Entire layer below GWT
                                cumulative_vertical_stress += (gamma - gamma_w) * h
                            else:
                                # Layer intersects GWT
                                above_gwt = gwt_depth - cumulative_depth
                                below_gwt = h - above_gwt
                                cumulative_vertical_stress += (gamma * above_gwt + 
                                                             (gamma - gamma_w) * below_gwt)
                        else:
                            cumulative_vertical_stress += gamma * h
                        
                        cumulative_depth += h
                    
                    # Add groundwater table if exists
                    if gwt_depth is not None:
                        ax.axhline(y=gwt_depth, color='cyan', linestyle='--', 
                                  linewidth=2, label='Groundwater Table')
                        # Add GWT label
                        ax.text(mid_x - 1, gwt_depth, "GWT", va='bottom', ha='center',
                               color='cyan', fontsize=10,
                               bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
                    
                    # Plot settings
                    ax.invert_yaxis()
                    ax.set_xlabel('Lateral Earth Pressure σₐ (kPa)', fontsize=12)
                    ax.set_ylabel('Depth (m)', fontsize=12)
                    ax.set_title(f"{title} Layer Arrangement", fontsize=14)
                    ax.grid(True)
                    ax.legend(loc='upper right')

                plt.tight_layout(rect=[0, 0, 1, 0.95])
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.error(f"Details: {str(e)}")

with tabs[1]:
    st.markdown('<div class="theory-box">', unsafe_allow_html=True)
    st.markdown("## Rankine's Active Earth Pressure Theory")
    st.markdown("""
    Rankine's theory assumes a uniform soil mass and ignores friction between the wall and soil. The key principles include:

    ### Assumptions
    1. Soil is **homogeneous and isotropic**.
    2. Soil mass is **semi-infinite**.
    3. The failure surface follows a **plane rupture**.
    4. The retaining wall is **smooth and vertical**.
    5. No wall friction is considered.
    6. Soil obeys **Mohr-Coulomb failure criterion**.
    7. The pressure acts parallel to the ground surface.

    ### Formula for Active Earth Pressure
    Rankine's active earth pressure coefficient (Ka) is given by:

    Ka = tan²(45 - φ/2)

    Where:
    - Ka = Active earth pressure coefficient
    - φ = Angle of internal friction of soil

    The active earth pressure at depth h is:

    Pa = Ka × γ × h

    Where:
    - Pa = Lateral earth pressure per unit width
    - γ = Unit weight of soil
    - h = Depth of soil

    ### Total Active Force Acting on the Wall
    Fa = (1/2) × Ka × γ × H²

    Where:
    - Fa = Total active force
    - H = Height of the wall

    This force acts **at a height of H/3** from the base of the wall.
    
    ### Layered Soil Profile
    For a layered soil profile, the pressure distribution changes at each layer boundary due to:
    1. Different friction angles (φ) resulting in different Ka values
    2. Different unit weights (γ)
    
    The pressure at any depth is calculated as:
    Pa = Ka × σv
    
    Where σv is the vertical stress at that depth.
    
    ### Effect of Groundwater Table
    When a groundwater table is present:
    1. Above the water table, use the total unit weight (γ)
    2. Below the water table, use the submerged unit weight (γ' = γ - γw)
    3. Water pressure must be added separately if considering total pressure
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("## How to Use This Tool")
    st.markdown("""
    1. **Prepare your CSV file** with the following columns:
       - `phi`: Internal friction angle in degrees
       - `gamma`: Unit weight in kN/m³
       - `thickness`: Layer thickness in meters
       - `name`: Name of the soil layer
    
    2. **Upload the CSV file** using the file uploader.
    
    3. **Enter the groundwater table depth** (optional):
       - Leave blank if there is no groundwater
       - Enter the depth in meters from the top surface
    
    4. **View the results**:
       - Original vs. optimized layer arrangement
       - Force reduction achieved by optimization
       - Pressure distribution graphs
    
    ### Sample CSV Format:
    ```
    name,phi,gamma,thickness
    Dense Sand,30,18,2
    Silty Sand,25,17,1.5
    Soft Clay,20,16,1
    Coarse Sand,35,19,2.5
    Loamy Soil,28,16.5,1.8
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("## About the Optimization")
    st.markdown("""
    This tool optimizes the arrangement of soil layers to minimize the lateral earth pressure on a retaining wall.
    
    The optimization works by:
    1. Calculating the active earth pressure for each possible arrangement of layers
    2. Finding the arrangement that produces the minimum total force
    3. Comparing the original and optimized arrangements
    
    **Note**: The optimization considers all possible permutations of layers, so it may take longer for a large number of layers.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("""
---
<p style="text-align: center; color: gray; font-size: 0.8rem;">
Soil Layer Optimizer | Built with Streamlit | © 2025
</p>
""", unsafe_allow_html=True)
