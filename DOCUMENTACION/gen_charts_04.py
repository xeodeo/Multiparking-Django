"""Genera los PNG de pastel (pie) de las 12 gráficas de la sección 04."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__),
                   "Secciones", "Seccion_04_Elicitacion_Requisitos", "charts")
os.makedirs(OUT, exist_ok=True)

COLORS = ['#2E6DA4', '#5B9BD5', '#8FAADC', '#BDD7EE', '#9DC3E6', '#70A0C8', '#C6D9F1']

def pie(cats, vals, titulo, fname):
    pairs = [(c, v) for c, v in zip(cats, vals) if v > 0]
    if not pairs:
        return
    cats_f, vals_f = zip(*pairs)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    wedges, texts, autotexts = ax.pie(
        vals_f,
        labels=cats_f,
        autopct='%1.1f%%',
        colors=COLORS[:len(cats_f)],
        startangle=90,
        textprops={'fontsize': 7},
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')
        at.set_color('white')
    ax.set_title(titulo, fontsize=10, pad=10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, fname), format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)

# ── Figura 2 ── Frecuencia de uso
pie(
    ["Todos los días", "Varias veces\na la semana", "Ocasionalmente", "Casi nunca"],
    [4, 3, 3, 3],
    "Frecuencia de uso de parqueaderos (n=13)", "fig02.png"
)
# ── Figura 3 ── Medio de pago actual
pie(
    ["Efectivo", "Tarjeta débito/crédito", "App o sistema digital"],
    [11, 1, 1],
    "Medio de pago actual en parqueaderos (n=13)", "fig03.png"
)
# ── Figura 4 ── Aspecto más molesto
pie(
    ["Pago solo en efectivo", "Largos tiempos\nde espera",
     "Tarifas poco claras", "Filas entrar/salir",
     "Falta de espacios", "Pérdida de tiquetes"],
    [4, 2, 2, 2, 2, 1],
    "Aspecto más molesto al usar el parqueadero (n=13)", "fig04.png"
)
# ── Figura 5 ── Disposición QR
pie(
    ["Sí", "Tal vez", "No"],
    [5, 8, 0],
    "Disposición para ingreso con código QR (n=13)", "fig05.png"
)
# ── Figura 6 ── Costo en tiempo real
pie(
    ["Sí, muy útil", "Me es indiferente", "No lo necesito"],
    [12, 0, 1],
    "Utilidad de ver costo en tiempo real (n=13)", "fig06.png"
)
# ── Figura 7 ── Reserva anticipada
pie(
    ["Sí", "Tal vez", "No"],
    [8, 4, 1],
    "Disposición para reserva anticipada (n=13)", "fig07.png"
)
# ── Figura 8 ── Método de pago preferido
pie(
    ["Transferencia/billetera", "Tarjeta débito/crédito", "Efectivo", "Código QR"],
    [4, 4, 3, 2],
    "Método de pago de preferencia para el sistema (n=13)", "fig08.png"
)
# ── Figura 9 ── Fidelización
pie(
    ["Me gustaría mucho", "Es algo interesante", "No me interesa"],
    [6, 5, 2],
    "Interés en fidelización por historial (n=13)", "fig09.png"
)
# ── Figura 10 ── Salida autónoma
pie(
    ["Moderadamente\nimportante", "Muy importante", "No es importante"],
    [6, 5, 2],
    "Importancia de la salida autónoma (n=13)", "fig10.png"
)
# ── Figura 11 ── Sistema automatizado
pie(
    ["Muy dispuesto", "Algo dispuesto", "No dispuesto"],
    [7, 6, 0],
    "Disposición para usar sistema automatizado (n=13)", "fig11.png"
)
# ── Figura 12 ── Disposición de pago
pie(
    ["Solo si precio igual", "Sí", "No"],
    [7, 6, 0],
    "Disposición de pago por sistema automatizado (n=13)", "fig12.png"
)
# ── Figura 13 ── Funcionalidades deseadas
pie(
    ["Poder reservar", "Pagar al ingresar", "Garantizar seguridad",
     "Notif. vencimiento", "Parqueadero más amplio"],
    [3, 2, 3, 3, 2],
    "Funcionalidades deseadas — parqueadero automatizado (n=13)", "fig13.png"
)

print("OK — 12 gráficas de pastel generadas en:", OUT)
