import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax_plano = axes[0]
ax_poli = axes[1]

# ── Datos ──
ang_P = 40 * np.pi / 180
ang_a = 55 * np.pi / 180
Pmag = 12
Px, Py = Pmag * np.cos(ang_P), Pmag * np.sin(ang_P)
t55 = np.tan(ang_a)
t40 = np.tan(ang_P)
xQ = 2 / (t40 - t55)
yQ = t40 * xQ
xD, yD = 0.0, 0.0

# Estimaciones para el polígono
ang_QD = np.arctan2(yD - yQ, xD - xQ)
Fa_est, Raux_est = 5.2, 8.8
Fb_est, Fc_est = -7.1, -5.0

PASOS = [
    "Sistema inicial: P y las tres rectas de accion a, b, c",
    "Paso 1: Q = punto donde P corta la direccion a",
    "Paso 2: D = b interseccion c = (0,0)",
    "Paso 3: Recta auxiliar de Cullman (Q -> D)",
    "Paso 4: Descomponer P en Fa y R_aux",
    "Paso 5: Descomponer R_aux en Fb y Fc. Sistema resuelto.",
]


def setup(ax, title):
    ax.cla()
    ax.axhline(0, color='#ccc', lw=1)
    ax.axvline(0, color='#ccc', lw=1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_title(title, fontsize=10)


def ext_line(ax, angle, px, py, color, label):
    ex, ey = np.cos(angle), np.sin(angle)
    for t in [-7, 7]:
        pass
    ax.plot([px - 7*ex, px + 7*ex],
            [py - 7*ey, py + 7*ey],
            '--', color=color, lw=1.4, alpha=0.7)
    ax.text(px + 7*ex + 0.1, py + 7*ey,
            label, color=color, fontsize=12, fontweight='bold')


def draw_arrow(ax, x1, y1, x2, y2, color):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))


def base_plano(ax):
    setup(ax, "Plano de fuerzas")
    ax.set_xlim(-6, 7)
    ax.set_ylim(-6, 6)
    ext_line(ax, ang_a, 0, 2,  '#2c7bb6', 'a')
    ext_line(ax, 0,    -4, 0,  '#1a9641', 'b')
    ax.axvline(0, color='#d7191c', lw=1.4, ls='--', alpha=0.7)
    ax.text(0.1, 5.5, 'c', color='#d7191c', fontsize=12, fontweight='bold')
    draw_arrow(ax, 0, 0, Px/Pmag*2.5, Py/Pmag*2.5, '#8b008b')
    ax.text(Px/Pmag*2.5 + 0.1, Py/Pmag*2.5, 'P=12kN',
            color='#8b008b', fontsize=10)
    ax.plot(0, 0, 'ko', ms=4)


def base_poli(ax):
    setup(ax, "Poligono de fuerzas")
    ax.set_xlim(-10, 14)
    ax.set_ylim(-8, 12)
    ax.axhline(0, color='#ddd', lw=1)
    ax.axvline(0, color='#ddd', lw=1)


def poly_arrow(ax, x1, y1, x2, y2, color, label):
    draw_arrow(ax, x1, y1, x2, y2, color)
    ax.text(x2 + 0.3, y2, label, color=color, fontsize=10, fontweight='bold')


def animate(i):
    base_plano(ax_plano)
    base_poli(ax_poli)

    # ── Paso 0: base ──
    ax_poli.plot(0, 0, 'ko', ms=4)
    ax_poli.text(0.3, 0, 'O', fontsize=10, color='#8b008b')
    poly_arrow(ax_poli, 0, 0, Px, Py, '#8b008b', 'P')

    if i >= 1:
        ax_plano.plot(xQ, yQ, 'o', color='#e67e00', ms=7)
        ax_plano.text(xQ + 0.1, yQ + 0.2,
                      f'Q ({xQ:.1f},{yQ:.1f})', color='#e67e00', fontsize=9)

    if i >= 2:
        ax_plano.plot(xD, yD, 'o', color='#c0392b', ms=7)
        ax_plano.text(xD + 0.1, yD - 0.4, 'D (0,0)',
                      color='#c0392b', fontsize=9)
        ax_poli.plot(Px, Py, 'o', color='#c0392b', ms=6)
        ax_poli.text(Px + 0.3, Py, 'D', color='#c0392b', fontsize=10)

    if i >= 3:
        ax_plano.plot([xQ, xD], [yQ, yD],
                      '-', color='#8e44ad', lw=2.5)
        ax_plano.text((xQ + xD)/2 + 0.1, (yQ + yD)/2 + 0.2,
                      'Auxiliar', color='#8e44ad', fontsize=9)
        # Auxiliar en polígono como referencia
        ax_poli.plot([0, Px], [0, Py],
                     '--', color='#8e44ad', lw=1.5, alpha=0.5)

    if i >= 4:
        # Fa sobre dirección a desde Q
        fax = xQ + np.cos(ang_a + np.pi) * 1.8
        fay = yQ + np.sin(ang_a + np.pi) * 1.8
        draw_arrow(ax_plano, xQ, yQ, fax, fay, '#2c7bb6')
        ax_plano.text(fax - 0.4, fay - 0.3, 'Fa',
                      color='#2c7bb6', fontsize=11, fontweight='bold')
        # R_aux de Q a D
        draw_arrow(ax_plano, xQ, yQ, xD, yD, '#8e44ad')
        ax_plano.text((xQ+xD)/2 - 0.8, (yQ+yD)/2 + 0.3,
                      'R_aux', color='#8e44ad', fontsize=10)
        # Polígono: Fa + R_aux = P
        Fa_vx = Fa_est * np.cos(ang_a)
        Fa_vy = Fa_est * np.sin(ang_a)
        poly_arrow(ax_poli, 0, 0, Fa_vx, Fa_vy, '#2c7bb6', 'Fa')
        Rv_x = Raux_est * np.cos(ang_QD)
        Rv_y = Raux_est * np.sin(ang_QD)
        poly_arrow(ax_poli, Fa_vx, Fa_vy,
                   Fa_vx + Rv_x, Fa_vy + Rv_y, '#8e44ad', 'R_aux')

    if i >= 5:
        draw_arrow(ax_plano, xD, yD, xD - 2.5, yD, '#1a9641')
        ax_plano.text(xD - 2.8, yD - 0.4, 'Fb',
                      color='#1a9641', fontsize=11, fontweight='bold')
        draw_arrow(ax_plano, xD, yD, xD, yD - 2, '#d7191c')
        ax_plano.text(xD + 0.1, yD - 2.2, 'Fc',
                      color='#d7191c', fontsize=11, fontweight='bold')
        # Polígono completo
        Fa_vx = Fa_est * np.cos(ang_a)
        Fa_vy = Fa_est * np.sin(ang_a)
        poly_arrow(ax_poli, 0, 0, Fa_vx, Fa_vy, '#2c7bb6', 'Fa')
        poly_arrow(ax_poli, Fa_vx, Fa_vy,
                   Fa_vx + Fb_est, Fa_vy, '#1a9641', 'Fb')
        poly_arrow(ax_poli, Fa_vx + Fb_est, Fa_vy,
                   Fa_vx + Fb_est, Fa_vy + Fc_est, '#d7191c', 'Fc')
        # Cierre
        cx2 = Fa_vx + Fb_est
        cy2 = Fa_vy + Fc_est
        ax_poli.plot([cx2, 0], [cy2, 0], '--', color='#8b008b', lw=1.5)
        ax_poli.text(cx2/2 + 0.3, cy2/2, 'cierra P',
                     color='#8b008b', fontsize=9)

    # Título del paso
    fig.suptitle(PASOS[i], fontsize=11, y=0.02,
                 bbox=dict(boxstyle='round', fc='#f0f0f0', ec='#ccc'))


anim = FuncAnimation(fig, animate, frames=len(PASOS),
                     interval=2500, repeat=True)

plt.tight_layout()
anim.save('tp2/img/tp/cullman_animacion.gif', writer='pillow', dpi=120)
plt.close()
print("cullman_animacion.gif generado")
