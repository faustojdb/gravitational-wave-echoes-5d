import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parámetros de la simulación (basados en Klein) - VERSIÓN PREVIEW
R_5D = 1.0  # Escala Klein (normalizada)
f_0 = 5.68  # Frecuencia fundamental (Hz)
gamma = 0.1  # Amortiguación viscoso
g_topo = 0.05  # "Gravedad" topológica
kappa = 0.2  # Coupling excitación
par_impar = 1  # Modo par (constructivo)
beta = 0.1  # Velocidad peculiar (for Doppler)
t_steps = 50  # Pasos temporales (MUY reducido para preview)
dt = 0.1  # Delta t (mayor para más velocidad)

# Grid para la membrana (2D -> 3D surface) - baja resolución
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x, y)

# Posiciones iniciales pelotas (3 pelotas)
pelotas_pos = np.array([[0.0,0.0,0.0], [2.0,0.0,0.0], [-2.0,0.0,0.0]], dtype=np.float64)  # (x,y,h)
pelotas_vel = np.zeros(3, dtype=np.float64)  # Velocidad inicial h_dot

# Función excitación E(t) (sinusoidal con Doppler)
def E_t(t):
    doppler_factor = np.sqrt((1 - beta) / (1 + beta)) if par_impar == 1 else np.sqrt((1 + beta) / (1 - beta))
    return kappa * np.sin(2 * np.pi * f_0 * t * doppler_factor) * par_impar

# Membrana deformación (onda radial + Doppler shift)
def membrane_z(X, Y, t):
    r = np.sqrt(X**2 + Y**2)
    wave = 0.5 * np.sin(2 * np.pi * (r - f_0 * t)) * np.exp(-r / 5)  # Onda propagando
    doppler_wave = wave * np.sqrt((1 - beta) / (1 + beta))  # Redshift
    return doppler_wave

# Update function for animation
def update(frame):
    t = frame * dt
    
    # Update pelotas elevación (ecuación segundo orden)
    global pelotas_vel
    h = pelotas_pos[:, 2]
    acceleration = E_t(t) - g_topo * h - gamma * pelotas_vel  # d²h/dt² = E - g h - γ dh/dt
    pelotas_vel += acceleration * dt
    pelotas_pos[:, 2] += pelotas_vel * dt
    
    # Update membrana
    Z = membrane_z(X, Y, t)
    
    # Clear plot
    ax.cla()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-2, 2)
    ax.set_title(f'Klein Analogía - Tiempo: {t:.2f}s | Elevación: {np.mean(h):.2f}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Elevación (h)')
    
    # Plot membrana
    ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.6, rstride=1, cstride=1)
    
    # Plot pelotas as spheres (simplificado)
    for px, py, pz in pelotas_pos:
        u = np.linspace(0, 2 * np.pi, 10)
        v = np.linspace(0, np.pi, 10)
        x_ball = 0.2 * np.outer(np.cos(u), np.sin(v)) + px
        y_ball = 0.2 * np.outer(np.sin(u), np.sin(v)) + py
        z_ball = 0.2 * np.outer(np.ones(np.size(u)), np.cos(v)) + pz
        ax.plot_surface(x_ball, y_ball, z_ball, color='red', alpha=0.8)
    
    # Medio viscoso (semi-transparent plane)
    ax.plot_surface(X, Y, np.full_like(Z, -1.5), color='blue', alpha=0.2)

# Setup figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

print("🎥 PREVIEW MODE: Klein Theory Visualization")
print("⚡ Versión rápida solo para visualización (no guarda archivo)")
print("🔴 Las pelotas rojas representan partículas siguiendo topología Klein")
print("🌊 La superficie ondulante muestra deformación Klein con Doppler")

# Animación (solo mostrar, no guardar)
ani = FuncAnimation(fig, update, frames=t_steps, interval=100)

plt.show()
print("✅ Preview completado")