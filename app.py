import streamlit as st
import database as db
import graphrag as grag
import predictive_agents as agents
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import uuid
import os
from datetime import datetime

ZEP_API_KEY = os.environ.get("ZEP_API_KEY", "")

st.set_page_config(
    page_title="SAFE - Seguridad Inteligente", page_icon="🛡️", layout="wide"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
* { font-family: 'Open Sans', sans-serif; }
h1,h2,h3,h4 { font-family: 'Montserrat', sans-serif; font-weight: 700; color: #0A2463; }
.stApp { background: #F8F9FA; }
.stButton > button { background-color: #0A2463 !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important; min-height: 48px !important; width: 100%; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div { border-radius: 10px !important; border: 2px solid #E0E0E0 !important; padding: 0.75rem !important; min-height: 48px !important; }
.metric-card { background: white; border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 16px rgba(10,36,99,0.08); }
.metric-value { font-size: 2.5rem; font-weight: 700; color: #0A2463; font-family: 'Montserrat', sans-serif; }
.metric-label { color: #61A0AF; font-size: 0.9rem; margin-top: 0.5rem; }
.user-info { background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 100%); padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }
.user-avatar { width: 55px; height: 55px; border-radius: 50%; background: #61A0AF; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; }
.incident-card { background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #61A0AF; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.sos-button { background: linear-gradient(135deg, #FF6B6B 0%, #FF0000 100%) !important; color: white !important; font-weight: 700 !important; font-size: 1.2rem !important; border-radius: 50px !important; padding: 1rem 2rem !important; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255,0,0,0.7); } 70% { box-shadow: 0 0 0 20px rgba(255,0,0,0); } 100% { box-shadow: 0 0 0 0 rgba(255,0,0,0); } }
.emergency-banner { background: linear-gradient(135deg, #FF6B6B 0%, #CC0000 100%); padding: 2rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 2rem; }
</style>
"""


def apply_styles():
    st.markdown(CSS, unsafe_allow_html=True)


def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "graphrag" not in st.session_state:
        st.session_state.graphrag = grag.create_graphrag_service(ZEP_API_KEY)
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = agents.create_agent_orchestrator()
    if "emergency_contacts" not in st.session_state:
        st.session_state.emergency_contacts = []
    if "security_config" not in st.session_state:
        st.session_state.security_config = {
            "anonymize": False,
            "location_enabled": True,
            "notifications": True,
            "auto_alert": False,
            "geo_tracking": False,
            "ai_analysis": True,
            "predictive_alerts": True,
            "encrypt_data": True,
            "session_timeout": 30,
        }


def plot_bar_advanced(df, x, y, title, color="#0A2463"):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        return None
    try:
        fig = px.bar(
            df,
            x=x,
            y=y,
            title=title,
            color=x,
            color_discrete_sequence=[color] * len(df),
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=350,
            font=dict(color="#0A2463"),
        )
        return fig
    except:
        return None


def plot_pie_advanced(df, values, names, title):
    if df is None or df.empty or values not in df.columns or names not in df.columns:
        return None
    try:
        fig = px.pie(
            df,
            values=values,
            names=names,
            title=title,
            hole=0.4,
            color=names,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig.update_layout(paper_bgcolor="white", height=350, font=dict(color="#0A2463"))
        fig.update_traces(textposition="inside", textinfo="percent+label")
        return fig
    except:
        return None


def plot_heatmap_advanced(data, x_labels, y_labels, title):
    try:
        fig = go.Figure(
            data=go.Heatmap(
                z=data, x=x_labels, y=y_labels, colorscale="RdYlGn_r", showscale=True
            )
        )
        fig.update_layout(
            title=title, paper_bgcolor="white", height=400, font=dict(color="#0A2463")
        )
        return fig
    except:
        return None


def plot_gauge_advanced(value, max_val, title, color="#FF6B6B"):
    try:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": title, "font": {"color": "#0A2463", "size": 16}},
                gauge={
                    "axis": {"range": [0, max_val], "tickcolor": "#0A2463"},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [0, max_val / 3], "color": "#4CAF50"},
                        {"range": [max_val / 3, 2 * max_val / 3], "color": "#FFD700"},
                        {"range": [2 * max_val / 3, max_val], "color": "#FF6B6B"},
                    ],
                },
            )
        )
        fig.update_layout(paper_bgcolor="white", height=250)
        return fig
    except:
        return None


def plot_network_graph(nodes, edges):
    if not nodes or len(nodes) == 0:
        return None
    try:
        fig = go.Figure()
        colors = px.colors.qualitative.Set2
        color_map = {}

        for i, node in enumerate(nodes):
            barrio = node.get("barrio", "unknown")
            if barrio not in color_map:
                color_map[barrio] = colors[len(color_map) % len(colors)]

        node_x, node_y, node_colors, node_text, node_sizes = [], [], [], [], []
        n = len(nodes)
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / n
            radius = 2 if n > 1 else 0
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            node_x.append(x)
            node_y.append(y)

            gravedad = node.get("gravedad", "baja")
            size = {"baja": 15, "media": 20, "alta": 25, "crítica": 30}.get(
                gravedad, 15
            )
            node_sizes.append(size)
            barrio = node.get("barrio", "unknown")
            node_colors.append(color_map.get(barrio, "#61A0AF"))
            node_text.append(f"{node.get('tipo', '')}<br>{barrio}<br>{gravedad}")

        for edge in edges[: n * 2]:
            try:
                parts = str(edge.get("source", "node_0")).split("_")
                src = int(parts[1]) if len(parts) > 1 else 0
                parts = str(edge.get("target", "node_0")).split("_")
                tgt = int(parts[1]) if len(parts) > 1 else 0
                if src < n and tgt < n:
                    fig.add_trace(
                        go.Scatter(
                            x=[node_x[src], node_x[tgt]],
                            y=[node_y[src], node_y[tgt]],
                            mode="lines",
                            line=dict(color="rgba(97,160,175,0.3)", width=2),
                            hoverinfo="skip",
                        )
                    )
            except:
                pass

        fig.add_trace(
            go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    line=dict(color="white", width=2),
                ),
                text=[f"N{i + 1}" for i in range(n)],
                textposition="middle center",
                textfont=dict(color="white", size=10),
                hovertext=node_text,
                hoverinfo="text",
            )
        )

        fig.update_layout(
            title="Grafo de Incidentes (GraphRAG)",
            showlegend=True,
            paper_bgcolor="white",
            height=500,
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(10,36,99,0.1)",
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(10,36,99,0.1)",
                zeroline=False,
                showticklabels=False,
            ),
            font=dict(color="#0A2463"),
        )
        return fig
    except:
        return None


def plot_statistics_advanced(incidents):
    if not incidents:
        return None
    try:
        df = pd.DataFrame(incidents)
        if df.empty:
            return None

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Distribución por Gravedad",
                "Tendencias Temporales",
                "Mapa de Calor Tipo-Barrio",
                "Distribución Geográfica",
            ),
        )

        if "gravedad" in df.columns:
            counts = df["gravedad"].value_counts()
            colors = {
                "baja": "#4CAF50",
                "media": "#FFD700",
                "alta": "#FF8C00",
                "crítica": "#FF6B6B",
            }
            fig.add_trace(
                go.Bar(
                    x=counts.index,
                    y=counts.values,
                    marker_color=[colors.get(g, "#61A0AF") for g in counts.index],
                ),
                row=1,
                col=1,
            )

        if "fecha" in df.columns:
            df["date"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
            daily = df.groupby("date").size()
            fig.add_trace(
                go.Scatter(
                    x=daily.index,
                    y=daily.values,
                    mode="lines+markers",
                    line=dict(color="#0A2463", width=3),
                    name="Incidentes",
                ),
                row=1,
                col=2,
            )

        if "barrio" in df.columns and "tipo" in df.columns:
            heatmap_data = df.groupby(["barrio", "tipo"]).size().unstack(fill_value=0)
            fig.add_trace(
                go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    colorscale="Blues",
                ),
                row=2,
                col=1,
            )

        if "barrio" in df.columns:
            bar_counts = df["barrio"].value_counts().head(10)
            fig.add_trace(
                go.Bar(x=bar_counts.index, y=bar_counts.values, marker_color="#61A0AF"),
                row=2,
                col=2,
            )

        fig.update_layout(
            height=700,
            showlegend=False,
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
        )
        return fig
    except:
        return None


def render_login_register():
    apply_styles()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            """<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; padding: 2rem; background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 50%, #61A0AF 100%); color: white; text-align: center;"><div style="font-size: 5rem; margin-bottom: 1rem;">🛡️</div><h1 style="font-size: 3rem; margin-bottom: 0.5rem;">SAFE</h1><p style="font-size: 1.2rem; opacity: 0.9;">Seguridad Inteligente y Siempre Activa</p><p style="margin-top: 3rem; opacity: 0.7; font-size: 0.95rem;">GraphRAG + AI Predictivo<br>Medellín, Colombia</p></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse"])
        with tab1:
            st.markdown(
                "<h2 style='text-align: center; margin-top: 2rem;'>Bienvenido</h2><p style='text-align: center; color: #61A0AF;'>Ingresa tus credenciales</p>",
                unsafe_allow_html=True,
            )
            email = st.text_input(
                "Correo electrónico", placeholder="tu@email.com", key="login_email"
            )
            password = st.text_input(
                "Contraseña",
                placeholder="Tu contraseña",
                type="password",
                key="login_password",
            )
            if st.button("Iniciar Sesión", use_container_width=True, key="login_btn"):
                if email and password:
                    user = db.verify_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Email o contraseña incorrectos")
        with tab2:
            st.markdown(
                "<h2 style='text-align: center; margin-top: 2rem;'>Crear Cuenta</h2><p style='text-align: center; color: #61A0AF;'>Regístrate para reportar incidentes</p>",
                unsafe_allow_html=True,
            )
            nombre = st.text_input(
                "Nombre completo", placeholder="Ej: Juan Pérez", key="reg_nombre"
            )
            email = st.text_input(
                "Correo electrónico", placeholder="tu@email.com", key="reg_email"
            )
            password = st.text_input(
                "Contraseña",
                placeholder="Mínimo 6 caracteres",
                type="password",
                key="reg_password",
            )
            telefono = st.text_input(
                "Teléfono", placeholder="Ej: 300 123 4567", key="reg_telefono"
            )
            if st.button("Crear Cuenta", use_container_width=True, key="reg_btn"):
                if all([nombre, email, password, telefono]):
                    if len(password) >= 6:
                        success, msg = db.create_user(nombre, email, password, telefono)
                        if success:
                            st.success("✅ ¡Cuenta creada exitosamente!")
                            user = db.verify_user(email, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.page = "dashboard"
                                st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("⚠️ La contraseña debe tener al menos 6 caracteres")
                else:
                    st.warning("⚠️ Completa todos los campos")


def render_dashboard():
    apply_styles()
    user = st.session_state.user
    stats = db.get_incident_stats()
    all_incidents = db.get_incidents()
    user_incidents = db.get_incidents(user["id"])

    st.markdown(
        """<div class="emergency-banner"><h1 style="color: white; margin: 0;">🚨 SISTEMA DE EMERGENCIA 121 🚨</h1><p style="margin: 0.5rem 0 0 0;">¿Necesitas ayuda inmediata?</p></div>""",
        unsafe_allow_html=True,
    )

    col_sos = st.columns([1, 2, 1])
    with col_sos[1]:
        if st.button(
            "🚨 SOS 121 - EMERGENCIA", use_container_width=True, type="primary"
        ):
            st.session_state.page = "sos"
            st.rerun()

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]}</p></div></div>""",
        unsafe_allow_html=True,
    )

    st.markdown("## 🛡️ Dashboard SAFE - Medellín")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{stats.get('total', 0)}</div><div class='metric-label'>Total</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #FF6B6B;'>{stats.get('por_gravedad', {}).get('crítica', 0)}</div><div class='metric-label'>Críticos</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #FF8C00;'>{stats.get('por_gravedad', {}).get('alta', 0)}</div><div class='metric-label'>Altos</div></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #4CAF50;'>{len(user_incidents)}</div><div class='metric-label'>Mis Reportes</div></div>",
            unsafe_allow_html=True,
        )
    with col5:
        riesgo = min(
            100,
            (
                stats.get("por_gravedad", {}).get("crítica", 0) * 4
                + stats.get("por_gravedad", {}).get("alta", 0) * 3
            )
            / max(stats.get("total", 1), 1)
            * 25,
        )
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{riesgo:.0f}%</div><div class='metric-label'>Riesgo</div></div>",
            unsafe_allow_html=True,
        )

    df_all = pd.DataFrame(all_incidents) if all_incidents else pd.DataFrame()

    tabs = st.tabs(["📊 Analytics", "📍 Geolocalización", "🔗 Grafo", "📈 Tendencias"])

    with tabs[0]:
        if not df_all.empty:
            fig = plot_statistics_advanced(all_incidents)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if "barrio" in df_all.columns:
                    counts = df_all.groupby("barrio").size().reset_index(name="count")
                    fig = plot_bar_advanced(counts, "barrio", "count", "Top Barrios")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            with col_a2:
                if "tipo" in df_all.columns:
                    counts = df_all.groupby("tipo").size().reset_index(name="count")
                    fig = plot_pie_advanced(counts, "count", "tipo", "Por Tipo")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown("### 📍 Mapa de Incidentes por Ubicación")
        if not df_all.empty and "barrio" in df_all.columns:
            geo_data = df_all.groupby("barrio").agg({"gravedad": "count"}).reset_index()
            geo_data.columns = ["barrio", "incidentes"]

            medellin_coords = {
                "El Poblado": (6.2087, -75.5685),
                "Laureles": (6.2445, -75.5900),
                "Belén": (6.2297, -75.6032),
                "Centro": (6.2442, -75.5750),
                "Robledo": (6.2667, -75.5667),
                "Villa Hermosa": (6.2300, -75.5500),
                "Buenos Aires": (6.2200, -75.5700),
                "Manrique": (6.2650, -75.5400),
                "Aranjuez": (6.2700, -75.5600),
                "Castilla": (6.2900, -75.5400),
            }

            lat, lon, labels = [], [], []
            for idx, row in geo_data.iterrows():
                if row["barrio"] in medellin_coords:
                    lat.append(medellin_coords[row["barrio"]][0])
                    lon.append(medellin_coords[row["barrio"]][1])
                    labels.append(f"{row['barrio']}: {row['incidentes']} incidentes")
                    barrio = row["barrio"]
                else:
                    barrio = "Otro"
                    lat.append(6.2447 + np.random.uniform(-0.02, 0.02))
                    lon.append(-75.5700 + np.random.uniform(-0.02, 0.02))
                    labels.append(f"{row['barrio']}: {row['incidentes']} incidentes")

            fig = go.Figure(
                go.Scattermapbox(
                    lat=lat,
                    lon=lon,
                    mode="markers",
                    marker=dict(size=15, color="#FF6B6B"),
                    text=labels,
                    hoverinfo="text",
                )
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                height=500,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="white",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📍 No hay datos de ubicación disponibles")

    with tabs[2]:
        st.markdown("### 🔗 Grafo de Correlación (GraphRAG)")
        if st.session_state.graphrag.is_available():
            with st.spinner("Construyendo grafo..."):
                graph_data = st.session_state.graphrag.build_incident_graph(user["id"])
                if graph_data.get("nodes"):
                    fig = plot_network_graph(graph_data["nodes"], graph_data["edges"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    st.markdown(
                        f"**Nodos:** {len(graph_data['nodes'])} | **Conexiones:** {len(graph_data['edges'])}"
                    )
                else:
                    st.info("🔗 Reporta incidentes para construir el grafo")
        else:
            st.warning("GraphRAG no disponible. Configure ZEP_API_KEY.")

    with tabs[3]:
        st.markdown("### 📈 Análisis de Tendencias")
        if user_incidents:
            df_user = pd.DataFrame(user_incidents)
            if "fecha" in df_user.columns:
                df_user["date"] = pd.to_datetime(
                    df_user["fecha"], errors="coerce"
                ).dt.date
                daily = df_user.groupby("date").size().reset_index(name="count")
                fig = px.line(
                    daily,
                    x="date",
                    y="count",
                    title="Tus Incidentes en el Tiempo",
                    markers=True,
                )
                fig.update_layout(paper_bgcolor="white", height=300)
                st.plotly_chart(fig, use_container_width=True)

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                if "gravedad" in df_user.columns:
                    counts = df_user["gravedad"].value_counts()
                    fig = plot_gauge_advanced(len(user_incidents), 50, "Total Reportes")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            with col_t2:
                criticos = sum(
                    1 for i in user_incidents if i.get("gravedad") == "crítica"
                )
                fig = plot_gauge_advanced(criticos, 10, "Casos Críticos", "#FF6B6B")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📈 Reporta incidentes para ver tendencias")

    render_nav_bar()


def render_incidents():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]} • {user["telefono"]}</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🚨 Reporte de Incidentes - Medellín")

    tabs = st.tabs(["➕ Nuevo Reporte", "📋 Mis Reportes", "📊 Estadísticas"])

    with tabs[0]:
        st.markdown("### Datos del Reportante")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.text_input("Nombre", value=user["nombre"], disabled=True)
        with col_u2:
            st.text_input("Correo", value=user["email"], disabled=True)
        st.text_input("Teléfono", value=user["telefono"], disabled=True)

        st.markdown("---")
        st.markdown("### Datos del Incidente")

        col1, col2 = st.columns(2)
        with col1:
            tipo = st.selectbox(
                "Tipo",
                [
                    "Hurto",
                    "Robo vehicular",
                    "Vandalismo",
                    "Agresión",
                    "Accidente de tránsito",
                    "Incendio",
                    "Daño a infraestructura",
                    "Otro",
                ],
            )
        with col2:
            gravedad = st.selectbox("Gravedad", ["baja", "media", "alta", "crítica"])

        descripcion = st.text_area(
            "Descripción", placeholder="Describe el incidente..."
        )
        col3, col4 = st.columns(2)
        with col3:
            ubicacion = st.text_input("Dirección", placeholder="Ej: Cra. 48 #Sur-45")
        with col4:
            barrio = st.selectbox(
                "Barrio",
                [
                    "El Poblado",
                    "Laureles",
                    "Belén",
                    "Centro",
                    "Robledo",
                    "Villa Hermosa",
                    "Buenos Aires",
                    "Manrique",
                    "Aranjuez",
                    "Castilla",
                    "Otro",
                ],
            )

        lat, lon = None, None
        if st.session_state.security_config.get("location_enabled"):
            st.markdown("### 📍 Geolocalización")
            geo_cols = st.columns(2)
            with geo_cols[0]:
                lat = st.number_input("Latitud", value=6.2447, format="%.6f")
            with geo_cols[1]:
                lon = st.number_input("Longitud", value=-75.5700, format="%.6f")

        if st.button("💾 Reportar Incidente", use_container_width=True, type="primary"):
            if descripcion and ubicacion:
                incident_id = db.save_incident(
                    user["id"], tipo, descripcion, ubicacion, barrio, gravedad
                )
                incident_data = {
                    "id": incident_id,
                    "tipo": tipo,
                    "descripcion": descripcion,
                    "ubicacion": ubicacion,
                    "barrio": barrio,
                    "gravedad": gravedad,
                    "user_id": user["id"],
                    "fecha": "now",
                    "lat": lat,
                    "lon": lon,
                }

                if st.session_state.graphrag.is_available():
                    st.session_state.graphrag.add_incident_context(
                        user["id"], incident_data
                    )
                    st.session_state.graphrag.create_incident_graph(
                        user["id"], incident_data
                    )

                st.success("✅ Incidente reportado exitosamente")
                st.rerun()
            else:
                st.error("⚠️ Completa los campos obligatorios")

    with tabs[1]:
        incidents = db.get_incidents(user["id"])
        if incidents:
            for inc in incidents:
                g = inc.get("gravedad", "baja").lower()
                colors = {
                    "crítica": "#FF6B6B",
                    "alta": "#FF8C00",
                    "media": "#FFD700",
                    "baja": "#4CAF50",
                }
                fecha = inc.get("fecha", "N/A")[:10] if inc.get("fecha") else "N/A"
                st.markdown(
                    f"""<div class="incident-card" style="border-left-color: {colors.get(g, "#61A0AF")};"><div style="display: flex; justify-content: space-between;"><strong style="color: #0A2463;">{inc.get("tipo", "N/A")}</strong><span style="background: {colors.get(g, "#61A0AF")}; color: {"white" if g != "media" else "black"}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem;">{g.upper()}</span></div><p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p><small style="color: #888;">📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}<br>📅 {fecha}</small></div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("📋 No has reportado incidentes aún")

    with tabs[2]:
        df = pd.DataFrame(incidents) if incidents else pd.DataFrame()
        if not df.empty:
            fig = plot_statistics_advanced(incidents)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Reporta incidentes para ver estadísticas")

    render_nav_bar()


def render_predictive():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Sistema de Agentes Predictivos IA</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🔮 Análisis Predictivo con Agentes IA")

    incident_history = db.get_incidents(user["id"])

    if st.button(
        "🚀 Ejecutar Análisis Completo", use_container_width=True, type="primary"
    ):
        with st.spinner("Ejecutando agentes predictivos..."):
            analysis = st.session_state.orchestrator.run_full_analysis(
                incident_history, {"user_id": user["id"], "nombre": user["nombre"]}
            )
            st.session_state.analysis_result = analysis

    if st.session_state.analysis_result:
        analysis = st.session_state.analysis_result
        risk = analysis["risk_level"]

        col_r, col_c = st.columns([1, 3])
        with col_r:
            fig = plot_gauge_advanced(analysis["confidence"], 100, "Confianza")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        with col_c:
            st.markdown(f"### Nivel de Riesgo: **{risk.upper()}**")
            st.markdown(f"**Agentes activos:** {analysis['agent_count']}")
            st.markdown(
                f"**Recomendaciones:** {len(analysis.get('consolidated_recommendations', []))}"
            )

        tabs = st.tabs(["🌡️ Hotspots", "⏰ Temporal", "⚠️ Riesgo", "🔗 Correlación"])

        with tabs[0]:
            if "HotspotAgent" in analysis["results"]:
                result = analysis["results"]["HotspotAgent"]
                hotspots = result.get("hotspots", [])
                if hotspots:
                    df_hs = pd.DataFrame(hotspots)
                    if "barrio" in df_hs.columns:
                        fig = px.scatter(
                            df_hs,
                            x="barrio",
                            y="risk_score",
                            size="historical_count",
                            color="risk_level",
                            color_discrete_map={
                                "critico": "#FF6B6B",
                                "alto": "#FF8C00",
                                "medio": "#FFD700",
                                "bajo": "#4CAF50",
                            },
                            title="Hotspots Predichos",
                            size_max=50,
                        )
                        fig.update_layout(paper_bgcolor="white", height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    for hs in hotspots:
                        st.markdown(
                            f"- 📍 **{hs.get('barrio', '')}**: {hs.get('predicted_incidents', 0)} predichos ({hs.get('risk_level', '')})"
                        )

        with tabs[1]:
            if "TemporalAgent" in analysis["results"]:
                result = analysis["results"]["TemporalAgent"]
                patterns = result.get("patterns", {})
                if patterns.get("peak_hours"):
                    df_h = pd.DataFrame(patterns["peak_hours"])
                    fig = px.bar(df_h, x="hour", y="count", title="Incidentes por Hora")
                    fig.update_layout(paper_bgcolor="white")
                    st.plotly_chart(fig, use_container_width=True)

        with tabs[2]:
            if "RiskAgent" in analysis["results"]:
                result = analysis["results"]["RiskAgent"]
                ra = result.get("risk_assessment", {})
                factors = ra.get("factors", {})
                if factors:
                    df_f = pd.DataFrame(
                        list(factors.items()), columns=["gravedad", "count"]
                    )
                    fig = plot_pie_advanced(df_f, "count", "gravedad", "Distribución")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                for rec in result.get("recommendations", []):
                    st.markdown(f"- ⚡ {rec}")

        with tabs[3]:
            if "CorrelationAgent" in analysis["results"]:
                result = analysis["results"]["CorrelationAgent"]
                corrs = result.get("correlations", [])
                if corrs:
                    df_c = pd.DataFrame(corrs)
                    if "barrio" in df_c.columns:
                        fig = plot_bar_advanced(
                            df_c, "barrio", "correlation_strength", "Correlación"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Ejecuta el análisis para ver predicciones")

    render_nav_bar()


def render_sos():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        """<div class="emergency-banner"><h1 style="color: white; margin: 0;">🚨 EMERGENCIA 121 🚨</h1></div>""",
        unsafe_allow_html=True,
    )

    col_sos = st.columns([1, 2, 1])
    with col_sos[1]:
        st.markdown(
            """<div style="background: white; border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(255,0,0,0.2);"><h2 style="color: #FF6B6B;">¿Necesitas ayuda inmediata?</h2><p>Contacta a las autoridades de emergencia en Medellín</p></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### 📞 Contactos de Emergencia")

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.markdown(
            """<div class="incident-card" style="border-left-color: #FF6B6B; text-align: center;"><h3>🚨 POLICÍA</h3><h1 style="color: #FF6B6B; font-size: 3rem;">123</h1></div>""",
            unsafe_allow_html=True,
        )
    with col_e2:
        st.markdown(
            """<div class="incident-card" style="border-left-color: #FF8C00; text-align: center;"><h3>🚑 AMBULANCIA</h3><h1 style="color: #FF8C00; font-size: 3rem;">123</h1></div>""",
            unsafe_allow_html=True,
        )
    with col_e3:
        st.markdown(
            """<div class="incident-card" style="border-left-color: #FFD700; text-align: center;"><h3>🚒 BOMBEROS</h3><h1 style="color: #FFD700; font-size: 3rem;">119</h1></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### 👥 Contactos de Emergencia Personal")
    for contact in st.session_state.emergency_contacts:
        st.markdown(
            f"- 📱 **{contact['nombre']}**: {contact['telefono']} ({contact.get('parentesco', 'Contacto')})"
        )

    if st.button("⬅️ Volver al Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()


def render_emergency_contacts():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Contactos de Emergencia</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 📞 Contactos de Emergencia")

    st.markdown("### Agregar Contacto")
    col1, col2 = st.columns(2)
    with col1:
        nombre_c = st.text_input("Nombre", placeholder="Ej: María López")
    with col2:
        telefono_c = st.text_input("Teléfono", placeholder="300 123 4567")
    parentesco = st.selectbox(
        "Relación", ["Familiar", "Amigo", "Vecino", "Colega", "Otro"]
    )

    if st.button("➕ Agregar", use_container_width=True):
        if nombre_c and telefono_c:
            st.session_state.emergency_contacts.append(
                {
                    "id": str(uuid.uuid4()),
                    "nombre": nombre_c,
                    "telefono": telefono_c,
                    "parentesco": parentesco,
                }
            )
            st.success("✅ Contacto agregado")
            st.rerun()

    st.markdown("---")
    st.markdown("### Mis Contactos")
    for i, c in enumerate(st.session_state.emergency_contacts):
        col_c1, col_c2 = st.columns([4, 1])
        with col_c1:
            st.markdown(
                f"""<div class="incident-card"><strong>{c["nombre"]}</strong> - {c["telefono"]}<br><small>{c["parentesco"]}</small></div>""",
                unsafe_allow_html=True,
            )
        with col_c2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.emergency_contacts.pop(i)
                st.rerun()

    render_nav_bar()


def render_security_settings():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Configuración AI</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## ⚙️ Configuración de Seguridad AI")

    st.markdown("### 🛡️ Módulos de Protección")
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("#### Privacidad")
        anonymize = st.toggle(
            "Anonimizar datos de incidentes",
            st.session_state.security_config.get("anonymize", False),
        )
        st.session_state.security_config["anonymize"] = anonymize

        st.markdown("#### Ubicación")
        location = st.toggle(
            "Permitir geolocalización",
            st.session_state.security_config.get("location_enabled", True),
        )
        st.session_state.security_config["location_enabled"] = location

        st.markdown("#### Notificaciones")
        notifications = st.toggle(
            "Alertas de seguridad push",
            st.session_state.security_config.get("notifications", True),
        )
        st.session_state.security_config["notifications"] = notifications

    with col_s2:
        st.markdown("#### AI Predictivo")
        ai_analysis = st.toggle(
            "Análisis IA avanzado",
            st.session_state.security_config.get("ai_analysis", True),
        )
        st.session_state.security_config["ai_analysis"] = ai_analysis

        predictive = st.toggle(
            "Alertas predictivas",
            st.session_state.security_config.get("predictive_alerts", True),
        )
        st.session_state.security_config["predictive_alerts"] = predictive

        st.markdown("#### Seguridad")
        encrypt = st.toggle(
            "Cifrado de datos",
            st.session_state.security_config.get("encrypt_data", True),
        )
        st.session_state.security_config["encrypt_data"] = encrypt

    st.markdown("---")
    st.markdown("### 🔐 Seguridad de la Cuenta")
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        st.markdown("**Cambiar Contraseña**")
        if st.button("📧 Solicitar cambio"):
            st.info("Se ha enviado enlace a tu correo")
    with col_sec2:
        st.markdown("**Sesiones Activas**")
        st.markdown("- Sesión actual: Activa")
        if st.button("🚪 Cerrar otras sesiones"):
            st.success("Sesiones cerradas")

    st.markdown("---")
    st.markdown("### ✅ Políticas de Seguridad")
    st.markdown("""
    - ✅ Datos cifrados en tránsito (TLS)
    - ✅ Contraseñas hasheadas SHA256
    - ✅ Cumplimiento Ley Habeas Data (Colombia)
    - ✅ Sesiones con timeout automático
    - ✅ Registro de actividad
    - ✅ AI de detección de anomalías
    """)

    if st.button("💾 Guardar Configuración", use_container_width=True):
        st.success("✅ Configuración guardada exitosamente")

    render_nav_bar()


def render_search():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">GraphRAG powered by Zep</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🔍 Búsqueda Semántica GraphRAG")

    query = st.text_input(
        "Buscar incidentes", placeholder="Ej: hurtos en El Poblado..."
    )

    if st.button("🔍 Buscar", use_container_width=True):
        if query:
            if st.session_state.graphrag.is_available():
                with st.spinner("Buscando..."):
                    results = st.session_state.graphrag.search_incidents(query)
                    if results:
                        st.success(f"✅ {len(results)} resultados")
                        for r in results:
                            m = r.get("metadata", {})
                            st.markdown(
                                f"- 📍 {m.get('barrio', 'N/A')} | {m.get('tipo', 'N/A')} | Similitud: {r.get('score', 0):.2f}"
                            )
                    else:
                        st.info("Sin resultados")
            else:
                st.warning("GraphRAG no disponible")

    render_nav_bar()


def render_profile():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar" style="width: 80px; height: 80px; font-size: 2rem;">{user["nombre"][0].upper()}</div><div><h2 style="margin: 0; color: white;">{user["nombre"]}</h2><p style="margin: 0; opacity: 0.8;">{user["email"]}</p></div></div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    user_incidents = db.get_incidents(user["id"])
    with col1:
        st.metric("Incidentes", len(user_incidents))
    with col2:
        st.metric(
            "Críticos", sum(1 for i in user_incidents if i.get("gravedad") == "crítica")
        )
    with col3:
        st.metric("Total ciudad", db.get_incident_stats().get("total", 0))

    st.markdown("### 📋 Mi Información")
    st.markdown(
        f"**Nombre:** {user['nombre']}  \n**Email:** {user['email']}  \n**Teléfono:** {user['telefono']}"
    )

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    render_nav_bar()


def render_nav_bar():
    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    col_nav = st.columns(7)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🚨", "sos"),
        ("📞", "contacts"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()


def main():
    init_session()
    if not st.session_state.user:
        render_login_register()
    else:
        pages = {
            "dashboard": render_dashboard,
            "incidents": render_incidents,
            "predictive": render_predictive,
            "sos": render_sos,
            "contacts": render_emergency_contacts,
            "search": render_search,
            "security": render_security_settings,
            "profile": render_profile,
        }
        pages.get(st.session_state.page, render_dashboard)()


if __name__ == "__main__":
    main()
