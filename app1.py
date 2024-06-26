# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:58:28 2024

@author: jperezr
"""

import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mplcursors  # Importar mplcursors para mostrar detalles al pasar el cursor por el gráfico

# Documentación y ayuda contextual
st.sidebar.markdown("### Ayuda y Documentación")
st.sidebar.markdown("""
    Simulación de la cuenta individual:
    
    **Instrucciones:**
    
    1. La simulación comienza cuando se proporciona un saldo inicial válido y se especifica la duración de la simulación en meses.
    2. En cada iteración mensual:
    3. Se genera un rendimiento mensual y una aportación voluntaria más solidaria aleatorios.
    4. Se calcula la fecha actual basada en el tiempo transcurrido desde el inicio de la simulación.
    5. Se actualizan los datos en el DataFrame con el saldo actual, rendimiento mensual, aportación voluntaria más solidaria y cálculos relacionados.
    6. Se actualizan los gráficos (saldo, rendimiento mensual, aportaciones voluntarias más solidarias).
    7. Los gráficos se muestran en los contenedores definidos en Streamlit.
    8. Se muestra el DataFrame actualizado con los datos formateados.


    I) Con una cuenta individual en una AFORE, tu saldo tiene el potencial de crecer mes a mes gracias al rendimiento
    generado por las inversiones y las aportaciones voluntarias que realices. Este crecimiento constante te ayuda
    a construir un patrimonio sólido para alcanzar tus metas financieras a largo plazo.

    II) A medida que realizas aportaciones voluntarias y se generan rendimientos mensuales, tu saldo en la cuenta individual
    aumenta gradualmente. Este saldo acumulado se puede utilizar para tu retiro futuro u otros objetivos financieros,
    proporcionándote seguridad y tranquilidad financiera.

    III) Después de un período de tiempo determinado, podrías ver cómo tu saldo ha crecido significativamente,
    proporcionándote una base financiera más sólida y la capacidad de tomar decisiones financieras más informadas y seguras.
    ¡Imagina el potencial de crecimiento que tiene tu cuenta individual en una AFORE!
    
    
""")


# Configuración de la aplicación Streamlit
st.title('Monitoreo del saldo en una Cuenta Individual de una AFORE')

# Entrada para definir el tiempo de simulación
st.write("Puedes indicar el tiempo de simulación en meses")
meses_simulacion = st.number_input("Meses", min_value=1, max_value=36, value=12, key="meses_simulacion")

# Entrada para definir el Saldo en Cuenta Individual
saldo_inicial = st.number_input("Saldo en Cuenta Individual (MXN)", min_value=0.0)

# Controles deslizantes para definir los umbrales
umbral_rendimiento = st.slider("Umbral de Rendimiento (%)", min_value=0.0, max_value=5.0, value=2.0)
umbral_aportacion = st.slider("Umbral de Aportación Voluntaria (MXN)", min_value=0, max_value=10000, value=3000)

# Inicializar listas para almacenar datos
tiempos = []
saldos = []
rendimientos = []
aportaciones = []

# Contenedores para los gráficos y la tabla
grafico_saldo = st.empty()
grafico_rendimiento = st.empty()
grafico_aportacion = st.empty()
tabla_datos = st.empty()

# Inicializar el DataFrame
df = pd.DataFrame(columns=["Fecha", "Saldo Actual (MXN)", "Rendimiento Mensual (%)", "Aportación Voluntaria y Solidaria (MXN)", "SA + RM", "Saldo Final"])

# Variable para controlar la visualización de gráficos y el mensaje de detención
mostrar_graficos = False  # Iniciar en falso para esperar la entrada del usuario

# Tiempo de inicio
inicio_tiempo = time.time()

if saldo_inicial > 0 and st.session_state.meses_simulacion is not None:
    mostrar_graficos = True  # Habilitar la visualización de gráficos y la simulación

while mostrar_graficos and len(tiempos) < st.session_state.meses_simulacion:
    # Tiempo actual
    tiempo_actual = time.time()

    # Simular obtención de datos
    rendimiento_mensual = random.uniform(0.5, 2.5)  # Rendimiento en porcentaje mensual
    aportacion_voluntaria = random.uniform(500, 5000)  # Aportación voluntaria mensual

    # Obtener la fecha actual si hay fechas disponibles
    fecha_actual = datetime.now() + timedelta(days=30 * len(tiempos))
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

    # Guardar datos
    tiempos.append(fecha_actual_str)
    rendimientos.append(rendimiento_mensual)
    aportaciones.append(aportacion_voluntaria)

    # Calcular el saldo actual en la primera iteración o igualar al saldo final de la iteración anterior
    if len(saldos) == 0:
        saldo_actual = saldo_inicial
    else:
        saldo_actual = df.loc[len(df)-1, "Saldo Final"]

    saldos.append(saldo_actual)

    # Registrar los datos en el DataFrame
    nuevo_registro = pd.DataFrame({
        "Fecha": [fecha_actual_str],
        "Saldo Actual (MXN)": [saldo_actual],
        "Rendimiento Mensual (%)": [rendimiento_mensual],
        "Aportación Voluntaria y Solidaria (MXN)": [aportacion_voluntaria],
        "SA + RM": [saldo_actual * (1 + rendimiento_mensual / 100)],
        "Saldo Final": [saldo_actual * (1 + rendimiento_mensual / 100) + aportacion_voluntaria]
    })

    df = pd.concat([df, nuevo_registro], ignore_index=True)

    # Crear figuras de matplotlib para los gráficos
    fig_saldo, ax_saldo = plt.subplots()
    fig_rendimiento, ax_rendimiento = plt.subplots()
    fig_aportacion, ax_aportacion = plt.subplots()

    # Actualizar datos en el gráfico de saldo
    ax_saldo.plot(saldos, marker='o', linestyle='-', color='b')
    ax_saldo.set_title('Saldo en Cuenta Individual')
    ax_saldo.set_xlabel('Tiempo (meses)')
    ax_saldo.set_ylabel('Saldo (MXN)')

    # Actualizar datos en el gráfico de rendimiento
    ax_rendimiento.plot(rendimientos, marker='o', linestyle='-', color='g')
    ax_rendimiento.axhline(y=umbral_rendimiento, color='r', linestyle='--', label=f'Umbral Rendimiento ({umbral_rendimiento}%)')
    ax_rendimiento.set_title('Rendimiento Mensual')
    ax_rendimiento.set_xlabel('Tiempo (meses)')
    ax_rendimiento.set_ylabel('Rendimiento (%)')
    ax_rendimiento.legend()

    # Actualizar datos en el gráfico de aportaciones voluntarias y solidarias
    ax_aportacion.plot(aportaciones, marker='o', linestyle='-', color='m')
    ax_aportacion.axhline(y=umbral_aportacion, color='r', linestyle='--', label=f'Umbral Aportación ({umbral_aportacion} MXN)')
    ax_aportacion.set_title('Aportaciones Voluntarias y Solidarias')  # Modificado el título del gráfico
    ax_aportacion.set_xlabel('Tiempo (meses)')
    ax_aportacion.set_ylabel('Aportación (MXN)')
    ax_aportacion.legend()

    # Mostrar los gráficos en los contenedores de Streamlit si no se ha detenido la visualización
    if mostrar_graficos:
        with grafico_saldo:
            st.pyplot(fig_saldo)
        with grafico_rendimiento:
            st.pyplot(fig_rendimiento)
        with grafico_aportacion:
            st.pyplot(fig_aportacion)

    # Mostrar el DataFrame en un contenedor de Streamlit con separador de miles
    with tabla_datos:
        # Aplicar separador de miles a las columnas de saldo y aportación voluntaria
        styled_df = df.style.format({
            "Saldo Actual (MXN)": "{:,.2f}".format,
            "Aportación Voluntaria y Solidaria (MXN)": "{:,.2f}".format,
            "SA + RM": "{:,.2f}".format,
            "Saldo Final": "{:,.2f}".format
        })

        st.dataframe(styled_df)

    # Esperar antes de la próxima actualización
    time.sleep(1)

# Mostrar el DataFrame con los datos finales
st.write("Simulación completada.")
st.dataframe(df.copy())


# Créditos del creador
st.sidebar.markdown("---")
st.sidebar.text("Creado por:")
st.sidebar.markdown("<span style='color: orange;'>Javier Horacio Pérez Ricárdez</span>", unsafe_allow_html=True)
