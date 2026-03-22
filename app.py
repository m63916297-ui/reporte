import streamlit as st
import database as db
import graphrag as grag
import predictive_agents as agents
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import uuid
import os

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
.incident-item { background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #61A0AF; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.incident-item.critica { border-left-color: #FF6B6B; }
.incident-item.alta { border-left-color: #FF8C00; }
.incident-item.media { border-left-color: #FFD700; }
.incident-item.baja { border-left-color: #4CAF50; }
.contact-card { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; border-left: 4px solid #61A0AF; }
.plot-container { background: white; border-radius: 16px; padding: 1rem; margin: 1rem 0; }
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
    if "security_settings" not in st.session_state:
        st.session_state.security_settings = {
            "anonymize": False,
            "location": False,
            "notifications": True,
        }
    if "emergency_contacts" not in st.session_state:
        st.session_state.emergency_contacts = []
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None


def plot_bar(df, x_col, y_col, title, orientation="v", color="#0A2463"):
    if df is None or df.empty or x_col not in df.columns or y_col not in df.columns:
        return None
    try:
        if orientation == "h":
            fig = px.bar(
                df,
                y=x_col,
                x=y_col,
                orientation="h",
                title=title,
                color=y_col,
                color_continuous_scale="Blues",
            )
        else:
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                orientation="v",
                title=title,
                color=x_col,
                color_continuous_sequence=["#0A2463"],
            )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
            height=350,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=False,
        )
        return fig
    except Exception as e:
        st.error(f"Error en gráfico: {e}")
        return None


def plot_pie(df, values, names, title):
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
        fig.update_layout(
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
            height=350,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        return fig
    except Exception as e:
        st.error(f"Error en gráfico: {e}")
        return None


def plot_gauge(value, max_val, title, color="#FF6B6B"):
    try:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": title, "font": {"color": "#0A2463"}},
                gauge={
                    "axis": {"range": [0, max_val], "tickcolor": "#0A2463"},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [0, max_val / 3], "color": "#4CAF50"},
                        {"range": [max_val / 3, 2 * max_val / 3], "color": "#FFD700"},
                        {"range": [2 * max_val / 3, max_val], "color": "#FF6B6B"},
                    ],
                    "threshold": {
                        "line": {"color": "#FF6B6B", "width": 4},
                        "value": value,
                    },
                },
            )
        )
        fig.update_layout(
            paper_bgcolor="white", height=250, margin=dict(l=30, r=30, t=50, b=30)
        )
        return fig
    except Exception as e:
        st.error(f"Error en gauge: {e}")
        return None


def plot_graph_network(nodes, edges):
    if not nodes or len(nodes) == 0:
        return None
    try:
        fig = go.Figure()
        colors = px.colors.qualitative.Set2
        barrio_colors = {}
        color_idx = 0

        for node in nodes:
            barrio = node.get("barrio", "unknown")
            if barrio not in barrio_colors:
                barrio_colors[barrio] = colors[color_idx % len(colors)]
                color_idx += 1

        node_x, node_y, node_colors, node_text, node_sizes = [], [], [], [], []

        for i, node in enumerate(nodes):
            angle = 2 * 3.14159 * i / len(nodes)
            radius = 2
            x = radius * (1 if i % 2 == 0 else -1) * (0.5 + (i % 3) * 0.2)
            y = radius * ((i // 2) % 3 - 1) * (0.5 + (i % 2) * 0.3)
            node_x.append(x)
            node_y.append(y)
            barrio = node.get("barrio", "unknown")
            node_colors.append(barrio_colors.get(barrio, "#61A0AF"))
            gravedad = node.get("gravedad", "baja")
            size = (
                20
                if gravedad == "baja"
                else 25
                if gravedad == "media"
                else 30
                if gravedad == "alta"
                else 35
            )
            node_sizes.append(size)
            node_text.append(f"{node.get('tipo', '')}<br>{barrio}<br>{gravedad}")

        for edge in edges[: len(nodes) * 2]:
            try:
                src = (
                    int(edge.get("source", "node_0").split("_")[1])
                    if "_" in str(edge.get("source", "node_0"))
                    else 0
                )
                tgt = (
                    int(edge.get("target", "node_0").split("_")[1])
                    if "_" in str(edge.get("target", "node_0"))
                    else 0
                )
                if src < len(node_x) and tgt < len(node_x):
                    fig.add_trace(
                        go.Scatter(
                            x=[node_x[src], node_x[tgt]],
                            y=[node_y[src], node_y[tgt]],
                            mode="lines",
                            line=dict(color="rgba(97,160,175,0.4)", width=2),
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
                text=[f"N{i + 1}" for i in range(len(nodes))],
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
            plot_bgcolor="#F8F9FA",
            font=dict(color="#0A2463"),
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
        )

        legend_items = [
            {"name": barrio, "color": color} for barrio, color in barrio_colors.items()
        ]
        for item in legend_items:
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    marker=dict(size=12, color=item["color"]),
                    name=item["name"],
                )
            )

        return fig
    except Exception as e:
        st.error(f"Error en grafo: {e}")
        return None


def render_login_register():
    apply_styles()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            """<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; padding: 2rem; background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 50%, #61A0AF 100%); color: white; text-align: center;"><div style="font-size: 5rem; margin-bottom: 1rem;">🛡️</div><h1 style="font-size: 3rem; margin-bottom: 0.5rem;">SAFE</h1><p style="font-size: 1.2rem; opacity: 0.9;">Seguridad Inteligente y Siempre Activa</p><p style="margin-top: 3rem; opacity: 0.7; font-size: 0.95rem;">GraphRAG + Agentes Predictivos<br>Medellín, Colombia</p></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse"])
        with tab1:
            st.markdown(
                "<h2 style='text-align: center; margin-top: 2rem;'>Bienvenido</h2><p style='text-align: center; color: #61A0AF; margin-bottom: 2rem;'>Ingresa tus credenciales</p>",
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
                else:
                    st.warning("⚠️ Completa todos los campos")
        with tab2:
            st.markdown(
                "<h2 style='text-align: center; margin-top: 2rem;'>Crear Cuenta</h2><p style='text-align: center; color: #61A0AF; margin-bottom: 2rem;'>Regístrate para reportar incidentes</p>",
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
                                st.session_state.page = "incidents"
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

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]} • {user["telefono"]}</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🛡️ Dashboard SAFE - Medellín")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{stats.get('total', 0)}</div><div class='metric-label'>Total Incidentes</div></div>",
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
            "<div class='metric-card'><div class='metric-value'>🛡️</div><div class='metric-label'>SAFE Activo</div></div>",
            unsafe_allow_html=True,
        )

    if not st.session_state.graphrag.is_available():
        st.warning(
            "⚠️ GraphRAG no disponible. Configure ZEP_API_KEY en variables de entorno."
        )

    all_incidents = db.get_incidents()
    df_all = pd.DataFrame(all_incidents) if all_incidents else pd.DataFrame()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Resumen", "📍 Barrios", "🏷️ Tipos", "⚠️ Gravedad", "🔗 Grafo"]
    )

    with tab1:
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if not df_all.empty and "barrio" in df_all.columns:
                counts = df_all.groupby("barrio").size().reset_index(name="count")
                fig = plot_bar(counts, "barrio", "count", "Incidentes por Barrio")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col_v2:
            if not df_all.empty and "tipo" in df_all.columns:
                counts = df_all.groupby("tipo").size().reset_index(name="count")
                fig = plot_pie(counts, "count", "tipo", "Distribución por Tipo")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if not df_all.empty and "barrio" in df_all.columns:
            counts = (
                df_all.groupby("barrio")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=True)
            )
            fig = plot_bar(
                counts.tail(10),
                "barrio",
                "count",
                "Top 10 Barrios con Más Incidentes",
                "h",
            )
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if not df_all.empty and "tipo" in df_all.columns:
            counts = df_all.groupby("tipo").size().reset_index(name="count")
            fig = plot_pie(counts, "count", "tipo", "Incidentes por Tipo")
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            if not df_all.empty and "gravedad" in df_all.columns:
                counts = df_all.groupby("gravedad").size().reset_index(name="count")
                fig = plot_bar(counts, "gravedad", "count", "Incidentes por Gravedad")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            riesgo = min(
                100,
                (
                    stats.get("por_gravedad", {}).get("crítica", 0) * 4
                    + stats.get("por_gravedad", {}).get("alta", 0) * 3
                )
                / max(stats.get("total", 1), 1)
                * 25,
            )
            fig = plot_gauge(round(riesgo, 1), 100, "Índice de Riesgo")
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.markdown("### 🔗 Grafo de Correlación (GraphRAG)")
        if st.session_state.graphrag.is_available():
            with st.spinner("Construyendo grafo con GraphRAG..."):
                graph_data = st.session_state.graphrag.build_incident_graph(user["id"])
                if graph_data and graph_data.get("nodes"):
                    fig = plot_graph_network(graph_data["nodes"], graph_data["edges"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    st.markdown(
                        f"**Nodos:** {len(graph_data['nodes'])} | **Conexiones:** {len(graph_data['edges'])}"
                    )
                else:
                    st.info(
                        "📊 Reporta incidentes para construir el grafo de correlación"
                    )
        else:
            st.warning("GraphRAG no disponible. Configure ZEP_API_KEY.")

    render_nav_bar()


def render_incidents():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]} • {user["telefono"]}</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🚨 Reporte de Incidentes - Medellín")

    tab1, tab2, tab3 = st.tabs(
        ["➕ Nuevo Reporte", "📋 Mis Reportes", "📊 Estadísticas"]
    )

    with tab1:
        st.markdown("### Datos del Reportante")
        col_user1, col_user2 = st.columns(2)
        with col_user1:
            st.text_input("Nombre", value=user["nombre"], disabled=True)
        with col_user2:
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
            barrio = st.text_input("Barrio", placeholder="Ej: El Poblado")

        if st.button("💾 Reportar Incidente", use_container_width=True, type="primary"):
            if descripcion and ubicacion and barrio:
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
                st.error("⚠️ Completa todos los campos obligatorios")

    with tab2:
        incidents = db.get_incidents(user["id"])
        if incidents:
            for inc in incidents:
                g = inc.get("gravedad", "baja").lower()
                fecha = inc.get("fecha", "N/A")[:10] if inc.get("fecha") else "N/A"
                st.markdown(
                    f"""<div class="incident-item {g}"><div style="display: flex; justify-content: space-between;"><strong>{inc.get("tipo", "N/A")}</strong><span style="background: {"#FF6B6B" if g == "crítica" else "#FF8C00" if g == "alta" else "#FFD700" if g == "media" else "#4CAF50"}; color: {"white" if g != "media" else "black"}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem;">{g.upper()}</span></div><p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p><small>📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}<br>📅 {fecha}</small></div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("📋 No has reportado incidentes aún")

    with tab3:
        df = pd.DataFrame(incidents) if incidents else pd.DataFrame()
        if not df.empty:
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if "barrio" in df.columns:
                    counts = df.groupby("barrio").size().reset_index(name="count")
                    fig = plot_bar(
                        counts, "barrio", "count", "Mis Incidentes por Barrio"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            with col_v2:
                if "tipo" in df.columns:
                    counts = df.groupby("tipo").size().reset_index(name="count")
                    fig = plot_pie(counts, "count", "tipo", "Mis Incidentes por Tipo")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Reporta incidentes para ver estadísticas")

    render_nav_bar()


def render_predictive():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Sistema de Agentes Predictivos</p></div></div>""",
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

        col_r, col_c = st.columns([1, 2])
        with col_r:
            fig = plot_gauge(analysis["confidence"], 100, "Confianza del Análisis")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        with col_c:
            st.markdown(f"### Nivel de Riesgo: **{risk.upper()}**")
            st.markdown(f"**Agentes activos:** {analysis['agent_count']}")
            st.markdown(
                f"**Recomendaciones:** {len(analysis.get('consolidated_recommendations', []))}"
            )

        tab1, tab2, tab3, tab4 = st.tabs(
            ["🌡️ Hotspots", "⏰ Temporal", "⚠️ Riesgo", "🔗 Correlación"]
        )

        with tab1:
            if "HotspotAgent" in analysis["results"]:
                result = analysis["results"]["HotspotAgent"]
                hotspots = result.get("hotspots", [])
                if hotspots:
                    df_hs = pd.DataFrame(hotspots)
                    if "barrio" in df_hs.columns and "risk_score" in df_hs.columns:
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
                            f"- 📍 **{hs.get('barrio', '')}**: {hs.get('predicted_incidents', 0)} incidentes ({hs.get('risk_level', '')})"
                        )

        with tab2:
            if "TemporalAgent" in analysis["results"]:
                result = analysis["results"]["TemporalAgent"]
                patterns = result.get("patterns", {})
                peak_hours = patterns.get("peak_hours", [])
                if peak_hours:
                    df_h = pd.DataFrame(peak_hours)
                    fig = plot_bar(df_h, "hour", "count", "Incidentes por Hora")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

        with tab3:
            if "RiskAgent" in analysis["results"]:
                result = analysis["results"]["RiskAgent"]
                ra = result.get("risk_assessment", {})
                factors = ra.get("factors", {})
                if factors:
                    df_f = pd.DataFrame(
                        list(factors.items()), columns=["gravedad", "count"]
                    )
                    fig = plot_pie(
                        df_f, "count", "gravedad", "Distribución por Gravedad"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                st.markdown("#### Recomendaciones")
                for rec in result.get("recommendations", []):
                    st.markdown(f"- ⚡ {rec}")

        with tab4:
            if "CorrelationAgent" in analysis["results"]:
                result = analysis["results"]["CorrelationAgent"]
                correlations = result.get("correlations", [])
                if correlations:
                    df_c = pd.DataFrame(correlations)
                    if (
                        "barrio" in df_c.columns
                        and "correlation_strength" in df_c.columns
                    ):
                        fig = plot_bar(
                            df_c,
                            "barrio",
                            "correlation_strength",
                            "Correlación por Barrio",
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Ejecuta el análisis para ver predicciones")

    render_nav_bar()


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
    if st.session_state.emergency_contacts:
        for i, c in enumerate(st.session_state.emergency_contacts):
            col_c1, col_c2 = st.columns([4, 1])
            with col_c1:
                st.markdown(
                    f"""<div class="contact-card"><strong>{c["nombre"]}</strong> - {c["telefono"]}<br><small>{c["parentesco"]}</small></div>""",
                    unsafe_allow_html=True,
                )
            with col_c2:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.emergency_contacts.pop(i)
                    st.rerun()

    st.markdown("---")
    st.markdown("### Emergency Medellín")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FF6B6B;"><strong>🚨 Policía</strong><br>123</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FF8C00;"><strong>🚑 Ambulancia</strong><br>123</div>""",
            unsafe_allow_html=True,
        )
    with col_e2:
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FFD700;"><strong>🚒 Bomberos</strong><br>119</div>""",
            unsafe_allow_html=True,
        )

    render_nav_bar()


def render_security_settings():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Configuración</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## ⚙️ Configuración de Seguridad")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("### 🔒 Privacidad")
        anonymize = st.toggle(
            "Anonimizar datos",
            st.session_state.security_settings.get("anonymize", False),
        )
        st.session_state.security_settings["anonymize"] = anonymize

        st.markdown("### 📍 Ubicación")
        location = st.toggle(
            "Permitir geolocalización",
            st.session_state.security_settings.get("location", False),
        )
        st.session_state.security_settings["location"] = location

        st.markdown("### 🔔 Notificaciones")
        notifications = st.toggle(
            "Alertas de seguridad",
            st.session_state.security_settings.get("notifications", True),
        )
        st.session_state.security_settings["notifications"] = notifications

    with col_s2:
        st.markdown("### 🛡️ Políticas de Seguridad")
        st.markdown("""
        - ✅ Datos cifrados en tránsito
        - ✅ Contraseñas hasheadas SHA256
        - ✅ Cumplimiento Ley Habeas Data
        - ✅ Sesiones con expiración
        """)

    if st.button("💾 Guardar", use_container_width=True):
        st.success("✅ Configuración guardada")

    render_nav_bar()


def render_search():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">GraphRAG powered by Zep</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## 🔍 Búsqueda GraphRAG")

    query = st.text_input(
        "Buscar incidentes", placeholder="Ej: hurtos en El Poblado..."
    )

    if st.button("🔍 Buscar", use_container_width=True):
        if query and st.session_state.graphrag.is_available():
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
        elif not st.session_state.graphrag.is_available():
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
    st.markdown(
        "<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E0E0E0;'>",
        unsafe_allow_html=True,
    )
    col_nav = st.columns(6)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
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
            "contacts": render_emergency_contacts,
            "search": render_search,
            "security": render_security_settings,
            "profile": render_profile,
        }
        pages.get(st.session_state.page, render_dashboard)()


if __name__ == "__main__":
    main()
