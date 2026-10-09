# Conclusiones (versión 2, 9 oct 2026) — en tres niveles

Reescrito según `CLAUDE.md`: cada afirmación se etiqueta como **teorema**, **supuesto de modelo** o **dato**. La versión 1 mezclaba niveles y hacía referencia a trabajos previos del repositorio; ambas cosas se eliminaron.

## Pregunta 1: ¿qué topografías pueden anular los modos pares de un lado y los impares del otro?

- **Teorema.** En una dimensión extra con una reflexión como simetría, un campo par satisface Neumann y uno impar Dirichlet en el punto fijo; el impar vale cero ahí. Para que un mismo tipo de modo (los impares) se anule en un extremo y no en el otro hacen falta **dos puntos fijos de reflexiones independientes**. En una dimensión eso es el orbifold $S^1/(Z_2\times Z_2')$, que según la clasificación exhaustiva de Nilse (2006) es el intervalo $S^1/Z_2$ con fase de Scherk–Schwarz $-1$. Sus sectores $(+,-)$ y $(-,+)$ son las dos familias espejo de modos impares; $(+,+)$ son los pares, presentes en ambos extremos. No hay otra opción en 1D: no es una elección entre candidatas.
- **Teorema.** Topografías sin puntos fijos (círculo, botella de Klein, $RP^2$, Möbius) no tienen "lado". La botella de Klein filtra $k$ par o impar según la paridad del campo (Nilse 2006, ec. 3.69), no según la posición.
- **Aclaración de lenguaje.** El punto fijo es una limitación dimensional sobre las configuraciones del campo, no un objeto. Nada interactúa con él.

## Pregunta 2: ¿qué características debe tener?

- **Teorema:** dos extremos distinguidos y reflexiones independientes en cada uno.
- **Supuesto de modelo:** para que las frecuencias de los modos masivos caigan en 10–5000 Hz, la geometría debe estar warped, y el warping necesita una fuente física (brana con tensión y constante cosmológica del bulk, como en Randall–Sundrum). Con warping, $m_n=(z_n/\ell)e^{-d/\ell}$ y, con $\ell\le0.1$ mm, $d/\ell\approx19$–$26$ pone $f_1$ en banda. Si además se modela el agujero negro como cuerda negra, la estabilidad exige $f_1>0.43\,c^3/(2\pi GM)$: 460 Hz para 30 M☉, 220 Hz para 62 M☉, 98 Hz para 142 M☉.
- **Dato:** con topografía plana (sin brana física) el radio permitido por Lee et al. (2020) es $<38.6\ \mu$m, lo que pone $f_1>10^{12}$ Hz. **Con paredes puramente dimensionales el efecto no es observable con LVK.** Ésta es la conclusión más importante de la revisión y hay que decidir qué versión de la hipótesis se sostiene.

## Pregunta 3: ¿existen en la bibliografía seria?

- **Dato bibliográfico.** $S^1/(Z_2\times Z_2')$: Kawamura 2001 (*Prog. Theor. Phys.* 105, 999), Barbieri–Hall–Nomura 2001 (*Phys. Rev. D* 63, 105007), Nilse 2006. Warping con dos branas y predicción de ondas gravitacionales: Seahra–Clarkson–Maartens 2005 (*PRL* 94, 121302), Clarkson–Seahra 2007 (*CQG* 24, F33). Ecos en branas gruesas: Zhu et al. 2025 y Tan et al. 2025 (*JHEP*). Botella de Klein con "paredes de paridad": Greene–Kabat–Levin–Porrati 2025 (arXiv:2510.05270).
- **Laguna.** No existe cálculo de la señal de una fusión en un $S^1/(Z_2\times Z_2')$ warped con los cuatro sectores de paridad.

## Qué es sintético y qué no en esta carpeta

- Sintético, sólo ilustrativo: la simulación 1+1 (fig6) y las figuras de funciones de modo (fig1–fig4). No son evidencia de nada; muestran un teorema.
- Cálculo con fórmulas publicadas y cotas publicadas: fig5, fig7 y las tablas. Dependen del supuesto de modelo indicado.
- Datos reales: ninguno hasta esta versión. El análisis con strain de GWOSC está en `5_Datos_Reales/`, con protocolo fijado antes de mirar los datos.

## Predicción mínima y resultado sobre datos reales

Lo único que todas las variantes comparten es una línea tardía a frecuencia fija, común a todos los eventos, que no escala con la masa del remanente. Se buscó eso, a ciegas, en strain público de GWOSC para 18 fusiones BBH de GWTC-3 (SNR ≥ 10, FAR ≤ 1/año), con protocolo fijado antes de mirar los datos y nula construida por el mismo pipeline sobre ventanas fuera de los eventos (`5_Datos_Reales/PROTOCOLO.md`).

- **Dato:** resultado **negativo**. Máximo del estadístico apilado Z = 41.9 (W1, 95 Hz) y 40.6 (W2, 1011 Hz), con p = 0.98 y 0.73; en ambas ventanas el observado está por debajo de la mediana de la nula. El cuerpo de la distribución de potencia posfusión es indistinguible del ruido fuera de los eventos. Un exploratorio post hoc con recorte de glitches (no confirmatorio) da p ≥ 0.16 en todos los casos. Detalle en `5_Datos_Reales/resultados/REPORTE.md`.
- **Modelo:** quedan desfavorecidas las variantes que predicen modos masivos en 20–1800 Hz con potencia relativa ≳ 2 MAD por evento. Las variantes con frecuencias fuera de banda (toda compactificación plana permitida por los tests de laboratorio) no se ven afectadas.
- **Teorema:** el resultado matemático de selección de paridad por lado no cambia; lo que falla es su versión observable en la banda de LIGO con esta sensibilidad.

## Qué haría falta para ir más lejos (sin violar `CLAUDE.md`)

1. Veto de glitches definido a priori (banderas de calidad de datos de GWOSC) en una nueva versión del protocolo, fechada antes de correrla.
2. Incluir Virgo y ventanas más largas para modos de decaimiento lento.
3. Inyecciones de eficiencia para convertir la sensibilidad en límite de amplitud de strain, reportadas como calibración y no como evidencia.
4. Cálculo teórico pendiente: señal de una fusión en $S^1/(Z_2\times Z_2')$ warped con los cuatro sectores de paridad, para saber qué amplitud relativa predice y si queda por encima o por debajo de la sensibilidad alcanzada.
