import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def setup_ax(ax, xlim, ylim, title):
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title(title, fontsize=11, pad=10)


def draw_force(ax, x, y, angle_deg, mag, label, color='blue', scale=0.4):
    """Dibuja una flecha de fuerza desde el punto (x,y)."""
    rad = np.radians(angle_deg)
    dx = mag * np.cos(rad) * scale
    dy = mag * np.sin(rad) * scale
    ax.annotate('', xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
    offset_x = 0.15 * np.sign(dx) if abs(dx) > 0.1 else 0.2
    offset_y = 0.15 * np.sign(dy) if abs(dy) > 0.1 else 0.2
    ax.text(x + dx + offset_x, y + dy + offset_y,
            f'{label}\n{mag} kN', fontsize=8, color=color, ha='center')
    ax.plot(x, y, 'o', color=color, markersize=4)
    ax.text(x - 0.2, y + 0.2, f'({x},{y})', fontsize=7, color='gray')


def draw_angle_arc(ax, x, y, angle_deg, radius=0.5, color='red'):
    """Dibuja arco de ángulo desde eje X hasta la dirección de la fuerza."""
    arc = mpatches.Arc((x, y), radius * 2, radius * 2,
                       angle=0, theta1=0, theta2=angle_deg,
                       color=color, linewidth=1)
    ax.add_patch(arc)
    mid = np.radians(angle_deg / 2)
    ax.text(x + (radius + 0.1) * np.cos(mid),
            y + (radius + 0.1) * np.sin(mid),
            f'{angle_deg}°', fontsize=7, color=color)


# ─────────────────────────────────────────
# EJERCICIO 1
# ─────────────────────────────────────────
def ejercicio1():
    fig, ax = plt.subplots(figsize=(7, 7))
    setup_ax(ax, (-6, 7), (-7, 6),
             'Ejercicio 1 — Sistema de fuerzas no concurrentes')

    fuerzas = [
        (3,  2,  60,  10, 'F₁'),
        (1,  0, 270,   8, 'F₂'),
        (0, -4, 180,   6, 'F₃'),
        (-3, 1, 225,   9, 'F₄'),
    ]

    colors = ['steelblue', 'darkorange', 'seagreen', 'firebrick']

    for (x, y, ang, mag, lbl), col in zip(fuerzas, colors):
        draw_force(ax, x, y, ang, mag, lbl, color=col)
        draw_angle_arc(ax, x, y, ang % 360, radius=0.6, color=col)

    plt.tight_layout()
    plt.savefig('tp2/img/tp/tp2_ej1.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp2_ej1.png generado')


# ─────────────────────────────────────────
# EJERCICIO 2 y 3 (misma figura)
# ─────────────────────────────────────────
def ejercicio2():
    fig, ax = plt.subplots(figsize=(8, 8))
    setup_ax(ax, (-7, 8), (-6, 7),
             'Ejercicios 2 y 3 — Direcciones de descomposición')

    # Fuerza P
    draw_force(ax, 0, 0, 40, 12, 'P', color='red', scale=0.45)
    draw_angle_arc(ax, 0, 0, 40, radius=0.7, color='red')

    # Rectas de acción (extendidas)
    x_range = np.linspace(-6, 7, 200)

    # Dirección a: 55°, pasa por (0, 2)
    slope_a = np.tan(np.radians(60))
    y_a = slope_a * (x_range - 0) + 2
    mask_a = (y_a >= -6) & (y_a <= 7)
    ax.plot(x_range[mask_a], y_a[mask_a],
            '--', color='steelblue', linewidth=1.2, label='Dirección a (55°)')
    ax.plot(0, 2, 'o', color='steelblue', markersize=5)
    ax.text(0.2, 2.2, '(0, 2)', fontsize=7, color='steelblue')

    # Dirección b: 0° (horizontal), pasa por (-4, 0)
    ax.axhline(-2, color='seagreen', linewidth=1.2, linestyle='--', label='Dirección b (0°)')
    ax.plot(0, -2, 'o', color='seagreen', markersize=5)
    #ax.text(-0.2, -1.2, '(0, -1)', fontsize=7, color='seagreen')

    # Dirección c: 270° (vertical), pasa por (0, -3)
    ax.axvline(2, color='firebrick', linewidth=1.2, linestyle='--', label='Dirección c (270°)')
    ax.plot(2, 0, 'o', color='firebrick', markersize=5)
    #ax.text(1.2, -0.2, '(1, 0)', fontsize=7, color='firebrick')

    # Intersecciones (puntos D, E, F para Ritter)
    # D = b ∩ c = (-4,0) ∩ x=0 → no se cortan (paralelas en este caso)
    # Intersección a ∩ b: y=0 → x = (0-2)/slope_a = -2/tan55
    x_ab = (0 - 4) / slope_a
    ax.plot(x_ab, -2, 's', color='black', markersize=6, zorder=5)
    ax.text(x_ab - 1.0, -1.8, f'D:({x_ab:.1f}; -2)', fontsize=7, color='black')

    # Intersección a ∩ c: x=0 → y=2 (punto de paso de a)
    y_ac = 2 * slope_a +2
    ax.plot(2, y_ac, 's', color='black', markersize=6, zorder=5)
    ax.text(2.2, y_ac, f'E:(2; {x_ab:.1f})', fontsize=7, color='black')

    # Intersección b ∩ c: x=0, y=0
    ax.plot(2, -2, 's', color='black', markersize=6, zorder=5)
    ax.text(2.2, -2.5, 'F:(2, -2)', fontsize=7, color='black')

    ax.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.savefig('tp2/img/tp/tp2_ej2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp2_ej2.png generado')


# ─────────────────────────────────────────
# EJERCICIO 4 — fuerzas paralelas
# ─────────────────────────────────────────
def ejercicio4():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.set_xlim(-5, 8)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_xlabel('x [m]')
    ax.set_title('Ejercicio 4 — Sistema de fuerzas paralelas',
                 fontsize=11, pad=10)

    fuerzas = [
        (-3,  1, ' 6 kN', 'F₁', 'firebrick'),
        (0, -1, '10 kN', 'F₂', 'firebrick'),
        (2,  1, ' 4 kN', 'F₃', 'firebrick'),
        (5, -1, ' 7 kN', 'F₄', 'firebrick'),
    ]

    scale = 0.25
    for (x, sentido, lbl_mag, lbl_f, col) in fuerzas:
        dy = scale * (6 if sentido > 0 else -10)
        # sentido codificado por posición y en la tupla
        dy = scale * abs(float(lbl_mag.strip().split()[0]))
        if sentido < 0:
            dy = -dy
        ax.annotate('', xy=(x, dy), xytext=(x, 0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2))
        ax.plot(x, 0, 'o', color=col, markersize=5)
        ax.text(x, dy + 0.15 * np.sign(dy), f'{lbl_f}\n{lbl_mag}',
                fontsize=8, color=col, ha='center')
        ax.text(x, -0.35, f'x={x}m', fontsize=7, color='gray', ha='center')

    plt.tight_layout()
    plt.savefig('tp2/img/tp/tp2_ej4.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp2_ej4.png generado')


# ─────────────────────────────────────────
# EJERCICIO 5 — cupla resultante
# ─────────────────────────────────────────
def ejercicio5():
    fig, ax = plt.subplots(figsize=(7, 7))
    setup_ax(ax, (-5, 6), (-5, 5), 'Ejercicio 5 — Sistema con cupla resultante')

    fuerzas = [
        (-2,  0,  90, 8, 'F₁'),
        (3,  0, 270, 8, 'F₂'),
        (0,  2,   0, 5, 'F₃'),
        (0, -2, 180, 5, 'F₄'),
    ]

    colors = ['steelblue', 'firebrick', 'seagreen', 'darkorange']

    for (x, y, ang, mag, lbl), col in zip(fuerzas, colors):
        draw_force(ax, x, y, ang, mag, lbl, color=col, scale=0.35)

    plt.tight_layout()
    plt.savefig('tp2/img/tp/tp2_ej5.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('tp2_ej5.png generado')


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
os.makedirs('tp2/img/tp', exist_ok=True)

ejercicio1()
ejercicio2()
ejercicio4()
ejercicio5()
