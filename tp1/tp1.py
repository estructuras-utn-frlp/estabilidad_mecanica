import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc


def ejercicio1():
    fuerzas = [(4, 90, 'F1'), (4, 120, 'F2'), (10, 40, 'F3'),
               (8, 300, 'F4'), (6, 180, 'F5'), (5, 240, 'F6')]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)

    # Define different radii for each arc, e.g., based on index or magnitude
    radii = [2 + i * 0.5 for i in range(len(fuerzas))]  # Incremental radii starting from 2

    for i, (mag, ang, label) in enumerate(fuerzas):
        rad = np.radians(ang)
        dx, dy = mag * np.cos(rad), mag * np.sin(rad)
        ax.quiver(0, 0, dx, dy, angles='xy', scale_units='xy', scale=1,
                  color='blue', alpha=0.8)
        # Calculate the acute angle to the nearest axis (x or y)
        angle_to_nearest_axis = min(ang % 90, 90 - (ang % 90))
        ax.text(dx*1.1, dy*1.1, f"{label}\n({mag}TN)\n{angle_to_nearest_axis:.1f}°", fontsize=9, ha='center')

        # Find the nearest axis (0, 90, 180, 270)
        axes = [0, 90, 180, 270]
        diffs = [min((ang - a) % 360, (a - ang) % 360) for a in axes]
        axis_ang = axes[diffs.index(min(diffs))]

        # Draw the short arc from nearest axis to the force direction
        delta = (ang - axis_ang) % 360
        radius = radii[i]
        if delta > 180:
            arc = Arc((0, 0), radius, radius, theta1=ang, theta2=axis_ang, color='red', linewidth=1)
        else:
            arc = Arc((0, 0), radius, radius, theta1=axis_ang, theta2=ang, color='red', linewidth=1)
        ax.add_patch(arc)

    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal')
    plt.savefig('img/fuerzas.png', dpi=300, bbox_inches='tight')


def ejercicio2():
    # 1. Definición de direcciones y puntos
    ang_a_deg = 30
    ang_b_deg = 140
    xA, yA = -4, 1
    xB, yB = 2, 3

    # 2. Configuración del gráfico
    fig, ax = plt.subplots(figsize=(8, 8))

    # Ejes cartesianos principales (X-Y)
    ax.axhline(0, color='black', linewidth=1.5, label='Eje X')
    ax.axvline(0, color='black', linewidth=1.5, label='Eje Y')

    # 3. Marcado de Direcciones de Descomposición (Rectas de acción)
    x_extremos = np.array([-15, 15])

    # Dirección a (30°)
    y_a = np.tan(np.radians(ang_a_deg)) * x_extremos
    ax.plot(x_extremos, y_a, color='darkblue', linestyle='--', linewidth=1,
            label=f'Dirección a ({ang_a_deg}°)')

    # Dirección b (150°)
    y_b = np.tan(np.radians(ang_b_deg)) * x_extremos
    ax.plot(x_extremos, y_b, color='darkgreen', linestyle='--', linewidth=1,
            label=f'Dirección b ({ang_b_deg}°)')

    # 4. Marcado del Punto de Traslación A
    ax.plot(xA, yA, 'ro', markersize=8, label=f'Punto A ({xA}, {yA})')
    ax.plot(xA, yA, 'ro', markersize=8, label=f'Punto A ({xA}, {yA})')
    ax.annotate(f'A ({xA}, {yA})', (xA, yA), textcoords="offset points",
                xytext=(10, 10), ha='center', fontweight='bold', color='red')

    # 5. Estética y grilla
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.grid(True, which='both', linestyle=':', alpha=0.5)
#    ax.legend(loc='upper right')

    plt.title("Croquis de Referencia: Direcciones de Descomposición y Punto de Traslación",
              fontsize=12, pad=20)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")

    plt.savefig('img/croquis_referencia.png', dpi=300, bbox_inches='tight')




ejercicio1()
ejercicio2()