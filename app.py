import streamlit as st
import database as db
import graphrag as grag
import predictive_agents as agents
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="SAFE - Seguridad Inteligente", page_icon="🛡️", layout="wide"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
* { font-family: 'Open Sans', sans-serif; }
h1,h2,h3,h4 { font-family: 'Montserrat', sans-serif; font-weight: 700; color: #0A2463; }
.stApp { background: #F8F9FA; }
.stButton > button { background-color: #0A2463 !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important; min-height: 48px !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div { border-radius: 10px !important; border: 2px solid #E0E0E0 !important; padding: 0.75rem !important; min-height: 48px !important; }
.card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(10,36,99,0.08); margin-bottom: 1rem; }
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
.risk-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.risk-badge.critico { background: #FF6B6B; color: white; }
.risk-badge.alto { background: #FF8C00; color: white; }
.risk-badge.medio { background: #FFD700; color: #333; }
.risk-badge.bajo { background: #4CAF50; color: white; }
.recommendation-item { background: linear-gradient(90deg, rgba(10,36,99,0.05) 0%, transparent 100%); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #0A2463; }
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
        st.session_state.graphrag = grag.create_graphrag_service()
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = agents.create_agent_orchestrator()


def plot_incidents_by_barrio(df):
    if df.empty:
        return None

    counts = df.groupby("barrio").size().reset_index(name="count")
    counts = counts.sort_values("count", ascending=True).tail(10)

    fig = px.bar(
        counts,
        y="barrio",
        x="count",
        orientation="h",
        title="Incidentes por Barrio",
        color="count",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=18, color="#0A2463"),
        showlegend=False,
        height=400,
    )
    fig.update_traces(marker=dict(line=dict(color="#0A2463", width=1)))
    return fig


def plot_incidents_by_tipo(df):
    if df.empty:
        return None

    counts = df.groupby("tipo").size().reset_index(name="count")

    fig = px.pie(
        counts,
        values="count",
        names="tipo",
        title="Distribución por Tipo de Incidente",
        hole=0.4,
        color="tipo",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=18, color="#0A2463"),
        height=400,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def plot_incidents_by_gravedad(df):
    if df.empty:
        return None

    counts = df.groupby("gravedad").size().reset_index(name="count")
    order = ["baja", "media", "alta", "crítica"]
    counts["gravedad"] = pd.Categorical(
        counts["gravedad"], categories=order, ordered=True
    )
    counts = counts.sort_values("gravedad")

    colors = {
        "baja": "#4CAF50",
        "media": "#FFD700",
        "alta": "#FF8C00",
        "crítica": "#FF6B6B",
    }
    count_colors = [colors.get(g, "#61A0AF") for g in counts["gravedad"]]

    fig = px.bar(
        counts,
        x="gravedad",
        y="count",
        title="Incidentes por Nivel de Gravedad",
        color="gravedad",
        color_discrete_map=colors,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=18, color="#0A2463"),
        showlegend=False,
        height=400,
    )
    return fig


def plot_timeline(incidents):
    if not incidents:
        return None

    df = pd.DataFrame(incidents)
    if "fecha" not in df.columns or df.empty:
        return None

    try:
        df["fecha_dt"] = pd.to_datetime(df["fecha"], errors="coerce")
        df = df.dropna(subset=["fecha_dt"])
        df["date"] = df["fecha_dt"].dt.date
        daily = df.groupby("date").size().reset_index(name="count")

        fig = px.line(
            daily,
            x="date",
            y="count",
            title="Tendencia de Incidentes en el Tiempo",
            markers=True,
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
            title_font=dict(size=18, color="#0A2463"),
            height=300,
        )
        fig.update_traces(
            line=dict(color="#0A2463", width=3), marker=dict(color="#61A0AF", size=10)
        )
        return fig
    except:
        return None


def plot_risk_heatmap(incidents):
    if not incidents:
        return None

    df = pd.DataFrame(incidents)
    if "barrio" not in df.columns or "gravedad" not in df.columns:
        return None

    gravedad_map = {"baja": 1, "media": 2, "alta": 3, "crítica": 4}
    df["risk_score"] = df["gravedad"].map(gravedad_map).fillna(1)

    heatmap_data = (
        df.groupby(["barrio", "tipo"])["risk_score"].mean().unstack(fill_value=0)
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale="RdYlGn_r",
            name="Riesgo",
        )
    )
    fig.update_layout(
        title="Mapa de Calor: Riesgo por Barrio y Tipo",
        paper_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=16, color="#0A2463"),
        height=400,
    )
    return fig


def plot_correlation_graph(nodes, edges):
    if not nodes:
        return None

    fig = go.Figure()

    barrio_groups = {}
    for i, node in enumerate(nodes):
        barrio = node.get("barrio", "unknown")
        if barrio not in barrio_groups:
            barrio_groups[barrio] = []
        barrio_groups[barrio].append(i)

    colors = px.colors.qualitative.Set2
    color_map = {
        barrio: colors[i % len(colors)] for i, barrio in enumerate(barrio_groups.keys())
    }

    node_x = []
    node_y = []
    node_colors = []
    node_text = []

    for i, node in enumerate(nodes):
        angle = 2 * 3.14159 * i / len(nodes)
        radius = 1 + (i % 3) * 0.3
        x = (
            radius
            * (0.5 + 0.5 * (i / len(nodes)))
            * (1 if i % 2 == 0 else -1)
            * abs(0.5 - (i % 10) / 20)
        )
        y = radius * ((i % 5) / 5 - 0.4)

        x = (i % 10) / 5 - 1
        y = (i // 10) / 3 - 0.5

        node_x.append(x)
        node_y.append(y)
        node_colors.append(color_map.get(node.get("barrio", "unknown"), "#61A0AF"))
        node_text.append(f"{node.get('tipo', '')}<br>{node.get('barrio', '')}")

    for edge in edges[:50]:
        try:
            src_idx = int(edge.get("source", "node_0").split("_")[1])
            tgt_idx = int(edge.get("target", "node_0").split("_")[1])
            if src_idx < len(node_x) and tgt_idx < len(node_x):
                fig.add_trace(
                    go.Scatter(
                        x=[node_x[src_idx], node_x[tgt_idx]],
                        y=[node_y[src_idx], node_y[tgt_idx]],
                        mode="lines",
                        line=dict(color="rgba(97,160,175,0.3)", width=1),
                        hoverinfo="none",
                    )
                )
        except:
            pass

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(size=20, color=node_colors, line=dict(color="white", width=2)),
            text=[f"N{i + 1}" for i in range(len(nodes))],
            textposition="middle center",
            textfont=dict(color="white", size=10),
            hovertext=node_text,
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title="Grafo de Correlación de Incidentes",
        showlegend=True,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=18, color="#0A2463"),
        height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    return fig


def plot_predictions(hotspots):
    if not hotspots:
        return None

    df = pd.DataFrame(hotspots)

    fig = px.scatter(
        df,
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
        title="Predicciones de Hotspots",
        size_max=40,
    )
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(color="#0A2463"),
        title_font=dict(size=18, color="#0A2463"),
        height=400,
    )
    return fig


def render_login_register():
    apply_styles()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; padding: 2rem; background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 50%, #61A0AF 100%); color: white; text-align: center;">
                <div style="font-size: 5rem; margin-bottom: 1rem;">🛡️</div>
                <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">SAFE</h1>
                <p style="font-size: 1.2rem; opacity: 0.9;">Seguridad Inteligente y Siempre Activa</p>
                <p style="margin-top: 3rem; opacity: 0.7; font-size: 0.95rem;">GraphRAG + Agentes Predictivos<br>Medellín, Colombia</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse"])

        with tab1:
            st.markdown(
                "<h2 style='text-align: center; margin-top: 2rem;'>Bienvenido</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='text-align: center; color: #61A0AF; margin-bottom: 2rem;'>Ingresa tus credenciales</p>",
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
                "<h2 style='text-align: center; margin-top: 2rem;'>Crear Cuenta</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='text-align: center; color: #61A0AF; margin-bottom: 2rem;'>Regístrate para reportar incidentes</p>",
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
        f"""
        <div class="user-info">
            <div class="user-avatar">{user["nombre"][0].upper()}</div>
            <div>
                <h3 style="margin: 0; color: white;">{user["nombre"]}</h3>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]} • {user["telefono"]}</p>
            </div>
        </div>
    """,
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
        criticos = stats.get("por_gravedad", {}).get("crítica", 0)
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #FF6B6B;'>{criticos}</div><div class='metric-label'>Casos Críticos</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        altos = stats.get("por_gravedad", {}).get("alta", 0)
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #FF8C00;'>{altos}</div><div class='metric-label'>Casos Altos</div></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            "<div class='metric-card'><div class='metric-value'>🛡️</div><div class='metric-label'>SAFE Activo</div></div>",
            unsafe_allow_html=True,
        )

    user_incidents = db.get_incidents(user["id"])
    all_incidents = db.get_incidents()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Resumen", "📍 Barrios", "🏷️ Tipos", "⚠️ Gravedad", "🔗 Grafo"]
    )

    with tab1:
        st.markdown("### Visualización General")

        df_user = pd.DataFrame(user_incidents) if user_incidents else pd.DataFrame()
        df_all = pd.DataFrame(all_incidents) if all_incidents else pd.DataFrame()

        col_v1, col_v2 = st.columns(2)

        with col_v1:
            if not df_all.empty and "barrio" in df_all.columns:
                fig = plot_incidents_by_barrio(df_all)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para visualizar")

        with col_v2:
            if not df_all.empty and "tipo" in df_all.columns:
                fig = plot_incidents_by_tipo(df_all)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Incidentes por Barrio")
        if not df_all.empty and "barrio" in df_all.columns:
            fig = plot_incidents_by_barrio(df_all)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de barrios")

    with tab3:
        st.markdown("### Distribución por Tipo")
        if not df_all.empty and "tipo" in df_all.columns:
            fig = plot_incidents_by_tipo(df_all)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de tipos")

    with tab4:
        st.markdown("### Gravedad de Incidentes")
        if not df_all.empty and "gravedad" in df_all.columns:
            fig1 = plot_incidents_by_gravedad(df_all)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)

            fig2 = plot_risk_heatmap(all_incidents)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay datos de gravedad")

    with tab5:
        st.markdown("### 🔗 Grafo de Correlación")
        graph_data = st.session_state.graphrag.build_incident_graph(user["id"])

        if graph_data.get("nodes"):
            fig = plot_correlation_graph(graph_data["nodes"], graph_data["edges"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Clusters identificados:")
            clusters = graph_data.get("clusters", {}).get("por_barrio", {})
            for barrio, nodes in list(clusters.items())[:5]:
                st.markdown(f"- 📍 **{barrio}**: {len(nodes)} incidentes conectados")
        else:
            st.info("No hay suficientes datos para generar el grafo")

    col_nav = st.columns(5)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, use_container_width=True):
                st.session_state.page = page
                st.rerun()


def render_incidents():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div class="user-avatar">{user["nombre"][0].upper()}</div>
            <div>
                <h3 style="margin: 0; color: white;">{user["nombre"]}</h3>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]} • {user["telefono"]}</p>
            </div>
        </div>
    """,
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
                st.session_state.graphrag.add_incident_context(
                    user["id"], incident_data
                )
                st.success("✅ Incidente reportado exitosamente")
                st.rerun()
            else:
                st.error("⚠️ Completa todos los campos")

    with tab2:
        incidents = db.get_incidents(user["id"])
        if incidents:
            for inc in incidents:
                g = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-item {g}">
                        <strong>{inc.get("tipo")}</strong>
                        <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p>
                        <small>📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}</small>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No has reportado incidentes aún")

    with tab3:
        st.markdown("### 📊 Estadísticas de Mis Incidentes")
        df = pd.DataFrame(incidents) if incidents else pd.DataFrame()

        if not df.empty:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                if "barrio" in df.columns:
                    fig = plot_incidents_by_barrio(df)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

            with col_v2:
                if "tipo" in df.columns:
                    fig = plot_incidents_by_tipo(df)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

            fig_timeline = plot_timeline(incidents)
            if fig_timeline:
                st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("Reporta incidentes para ver estadísticas")

    col_nav = st.columns(5)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, use_container_width=True):
                st.session_state.page = page
                st.rerun()


def render_predictive():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div class="user-avatar">{user["nombre"][0].upper()}</div>
            <div>
                <h3 style="margin: 0; color: white;">{user["nombre"]}</h3>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Sistema de Agentes Predictivos</p>
            </div>
        </div>
    """,
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

    if "analysis_result" in st.session_state and st.session_state.analysis_result:
        analysis = st.session_state.analysis_result

        risk = analysis["risk_level"]
        risk_color = {
            "critico": "#FF6B6B",
            "alto": "#FF8C00",
            "medio": "#FFD700",
            "bajo": "#4CAF50",
        }

        st.markdown(
            f"### Nivel de Riesgo: <span class='risk-badge {risk}'>{risk.upper()}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Confianza:** {analysis['confidence']:.1f}% | **Agentes:** {analysis['agent_count']}"
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            ["🌡️ Hotspots", "⏰ Temporal", "⚠️ Riesgo", "🔗 Correlación"]
        )

        with tab1:
            if "HotspotAgent" in analysis["results"]:
                result = analysis["results"]["HotspotAgent"]
                st.markdown(f"### {result['summary']}")

                if result.get("hotspots"):
                    fig = plot_predictions(result["hotspots"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                    for hs in result["hotspots"]:
                        st.markdown(
                            f"- 📍 **{hs['barrio']}**: {hs['predicted_incidents']} incidentes predichos ({hs['risk_level']})"
                        )

        with tab2:
            if "TemporalAgent" in analysis["results"]:
                result = analysis["results"]["TemporalAgent"]
                patterns = result.get("patterns", {})

                if patterns.get("peak_hours"):
                    df_hours = pd.DataFrame(patterns["peak_hours"])
                    fig = px.bar(
                        df_hours, x="hour", y="count", title="Incidentes por Hora"
                    )
                    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
                    fig.update_traces(marker_color="#0A2463")
                    st.plotly_chart(fig, use_container_width=True)

                if patterns.get("peak_days"):
                    st.markdown("#### Días Pico")
                    for pd in patterns["peak_days"]:
                        st.markdown(f"- 📅 **{pd['day']}**: {pd['count']} incidentes")

        with tab3:
            if "RiskAgent" in analysis["results"]:
                result = analysis["results"]["RiskAgent"]
                ra = result.get("risk_assessment", {})

                df_factors = pd.DataFrame([ra.get("factors", {})]).T.reset_index()
                df_factors.columns = ["gravedad", "count"]

                colors = {
                    "baja": "#4CAF50",
                    "media": "#FFD700",
                    "alta": "#FF8C00",
                    "crítica": "#FF6B6B",
                }

                fig = px.pie(
                    df_factors,
                    values="count",
                    names="gravedad",
                    title="Distribución por Gravedad",
                    color="gravedad",
                    color_discrete_map=colors,
                )
                fig.update_layout(paper_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("#### Recomendaciones")
                for rec in result.get("recommendations", []):
                    st.markdown(
                        f"<div class='recommendation-item'>⚡ {rec}</div>",
                        unsafe_allow_html=True,
                    )

        with tab4:
            if "CorrelationAgent" in analysis["results"]:
                result = analysis["results"]["CorrelationAgent"]
                st.markdown(f"### {result['summary']}")

                for corr in result.get("correlations", [])[:5]:
                    st.markdown(
                        f"- 🔗 **{corr['barrio']}**: {corr['type_count']} tipos ({corr['correlation_strength']}%)"
                    )

    col_nav = st.columns(5)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, use_container_width=True):
                st.session_state.page = page
                st.rerun()


def render_search():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div class="user-avatar">{user["nombre"][0].upper()}</div>
            <div>
                <h3 style="margin: 0; color: white;">{user["nombre"]}</h3>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">GraphRAG powered by Zep</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("## 🔍 Búsqueda Semántica GraphRAG")

    query = st.text_input(
        "Buscar incidentes", placeholder="Ej: hurtos en El Poblado..."
    )

    if st.button("🔍 Buscar", use_container_width=True, type="primary"):
        if query:
            if st.session_state.graphrag.is_available():
                with st.spinner("Buscando..."):
                    results = st.session_state.graphrag.search_incidents(query)
                    if results:
                        st.success(f"✅ {len(results)} resultados")
                        for r in results:
                            metadata = r.get("metadata", {})
                            st.markdown(
                                f"- 📍 {metadata.get('barrio', 'N/A')} | {metadata.get('tipo', 'N/A')}"
                            )
                    else:
                        st.info("Sin resultados")
            else:
                st.warning("GraphRAG no disponible")

    col_nav = st.columns(5)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, use_container_width=True):
                st.session_state.page = page
                st.rerun()


def render_profile():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div class="user-avatar" style="width: 80px; height: 80px; font-size: 2rem;">{user["nombre"][0].upper()}</div>
            <div>
                <h2 style="margin: 0; color: white;">{user["nombre"]}</h2>
                <p style="margin: 0; opacity: 0.8;">{user["email"]}</p>
            </div>
        </div>
    """,
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
    st.markdown(f"**Nombre:** {user['nombre']}")
    st.markdown(f"**Email:** {user['email']}")
    st.markdown(f"**Teléfono:** {user['telefono']}")

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    col_nav = st.columns(5)
    pages = [
        ("🏠", "dashboard"),
        ("📊", "incidents"),
        ("🔮", "predictive"),
        ("🔍", "search"),
        ("👤", "profile"),
    ]
    for i, (icon, page) in enumerate(pages):
        with col_nav[i]:
            if st.button(icon, use_container_width=True):
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
            "search": render_search,
            "profile": render_profile,
        }

        if st.session_state.page in pages:
            pages[st.session_state.page]()
        else:
            render_dashboard()


if __name__ == "__main__":
    main()
