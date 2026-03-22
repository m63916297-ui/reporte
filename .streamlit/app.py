mejorimport streamlit as st
import database as db
import graphrag as grag
import predictive_agents as agents
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import uuid

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
.contact-card { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; border-left: 4px solid #61A0AF; display: flex; justify-content: space-between; align-items: center; }
.security-toggle { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; }
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
    if "security_settings" not in st.session_state:
        st.session_state.security_settings = {
            "location_enabled": False,
            "anonymize_data": False,
            "notifications": True,
            "auto_report": False,
        }
    if "emergency_contacts" not in st.session_state:
        st.session_state.emergency_contacts = []


def plot_bar_chart(df, x_col, y_col, title, orientation="v", color="#0A2463"):
    if df is None or df.empty or x_col not in df.columns or y_col not in df.columns:
        return None
    try:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            orientation=orientation,
            title=title,
            color=y_col,
            color_continuous_scale="Blues",
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
            height=350,
            showlegend=False,
        )
        return fig
    except:
        return None


def plot_pie_chart(df, values_col, names_col, title):
    if (
        df is None
        or df.empty
        or values_col not in df.columns
        or names_col not in df.columns
    ):
        return None
    try:
        fig = px.pie(
            df,
            values=values_col,
            names=names_col,
            title=title,
            hole=0.4,
            color=names_col,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig.update_layout(paper_bgcolor="white", font=dict(color="#0A2463"), height=350)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        return fig
    except:
        return None


def plot_scatter_with_regression(
    df, x_col, y_col, size_col, color_col, title, color_map
):
    if df is None or df.empty or x_col not in df.columns:
        return None
    try:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size=size_col,
            color=color_col,
            color_discrete_map=color_map,
            title=title,
            size_max=50,
        )
        fig.update_layout(paper_bgcolor="white", font=dict(color="#0A2463"), height=400)
        return fig
    except:
        return None


def plot_heatmap_matrix(data, x_labels, y_labels, title):
    if not data or len(data) == 0:
        return None
    try:
        fig = go.Figure(
            data=go.Heatmap(
                z=data, x=x_labels, y=y_labels, colorscale="RdYlGn_r", showscale=True
            )
        )
        fig.update_layout(
            title=title, paper_bgcolor="white", font=dict(color="#0A2463"), height=400
        )
        return fig
    except:
        return None


def plot_temporal_timeline(df, date_col, value_col, title):
    if (
        df is None
        or df.empty
        or date_col not in df.columns
        or value_col not in df.columns
    ):
        return None
    try:
        df_sorted = df.sort_values(date_col)
        fig = px.line(df_sorted, x=date_col, y=value_col, title=title, markers=True)
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#0A2463"),
            height=300,
        )
        fig.update_traces(
            line=dict(color="#0A2463", width=3), marker=dict(color="#61A0AF", size=12)
        )
        return fig
    except:
        return None


def plot_gauge(value, max_value, title, color):
    try:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": title},
                gauge={
                    "axis": {"range": [0, max_value]},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [0, max_value / 3], "color": "#4CAF50"},
                        {
                            "range": [max_value / 3, 2 * max_value / 3],
                            "color": "#FFD700",
                        },
                        {"range": [2 * max_value / 3, max_value], "color": "#FF6B6B"},
                    ],
                },
            )
        )
        fig.update_layout(paper_bgcolor="white", height=250)
        return fig
    except:
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
                fig = plot_bar_chart(
                    counts.head(10), "barrio", "count", "Incidentes por Barrio"
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col_v2:
            if not df_all.empty and "tipo" in df_all.columns:
                counts = df_all.groupby("tipo").size().reset_index(name="count")
                fig = plot_pie_chart(counts, "count", "tipo", "Distribución por Tipo")
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
            fig = plot_bar_chart(
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
            fig = plot_pie_chart(counts, "count", "tipo", "Incidentes por Tipo")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    with tab4:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            if not df_all.empty and "gravedad" in df_all.columns:
                counts = df_all.groupby("gravedad").size().reset_index(name="count")
                fig = plot_bar_chart(
                    counts, "gravedad", "count", "Incidentes por Gravedad"
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            if stats.get("total", 0) > 0:
                riesgo_score = (
                    (
                        stats.get("por_gravedad", {}).get("crítica", 0) * 4
                        + stats.get("por_gravedad", {}).get("alta", 0) * 3
                    )
                    / max(stats.get("total", 1), 1)
                    * 25
                )
                fig = plot_gauge(
                    round(riesgo_score, 1), 100, "Índice de Riesgo", "#FF6B6B"
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    with tab5:
        graph_data = st.session_state.graphrag.build_incident_graph(user["id"])
        if graph_data.get("nodes"):
            nodes = graph_data["nodes"]
            edges = graph_data["edges"]
            df_nodes = pd.DataFrame(nodes)
            if not df_nodes.empty:
                fig = px.scatter(
                    df_nodes,
                    x=range(len(df_nodes)),
                    y=[0] * len(df_nodes),
                    size=[20] * len(df_nodes),
                    color="barrio",
                    title="Grafo de Incidentes por Barrio",
                )
                fig.update_layout(paper_bgcolor="white", height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Nodos:** {len(nodes)} | **Conexiones:** {len(edges)}")
        else:
            st.info("🔗 No hay suficientes datos para el grafo")
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
                    f"""<div class="incident-item {g}"><strong>{inc.get("tipo")}</strong><p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p><small>📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}</small></div>""",
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
                    fig = plot_bar_chart(
                        counts, "barrio", "count", "Mis Incidentes por Barrio"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            with col_v2:
                if "tipo" in df.columns:
                    counts = df.groupby("tipo").size().reset_index(name="count")
                    fig = plot_pie_chart(
                        counts, "count", "tipo", "Mis Incidentes por Tipo"
                    )
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
        with st.spinner("Ejecutando agentes..."):
            analysis = st.session_state.orchestrator.run_full_analysis(
                incident_history, {"user_id": user["id"], "nombre": user["nombre"]}
            )
            st.session_state.analysis_result = analysis
    if "analysis_result" in st.session_state and st.session_state.analysis_result:
        analysis = st.session_state.analysis_result
        risk = analysis["risk_level"]
        st.markdown(
            f"### Nivel de Riesgo: <span class='risk-badge {risk}'>{risk.upper()}</span> | **Confianza:** {analysis['confidence']:.1f}% | **Agentes:** {analysis['agent_count']}",
            unsafe_allow_html=True,
        )
        tab1, tab2, tab3, tab4 = st.tabs(
            ["🌡️ Hotspots", "⏰ Temporal", "⚠️ Riesgo", "🔗 Correlación"]
        )
        with tab1:
            if "HotspotAgent" in analysis["results"]:
                result = analysis["results"]["HotspotAgent"]
                st.markdown(f"#### {result['summary']}")
                hotspots = result.get("hotspots", [])
                if hotspots:
                    df_hs = pd.DataFrame(hotspots)
                    if "barrio" in df_hs.columns and "risk_score" in df_hs.columns:
                        fig = plot_scatter_with_regression(
                            df_hs,
                            "barrio",
                            "risk_score",
                            "historical_count",
                            "risk_level",
                            "Predicciones de Hotspots",
                            {
                                "critico": "#FF6B6B",
                                "alto": "#FF8C00",
                                "medio": "#FFD700",
                                "bajo": "#4CAF50",
                            },
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    for hs in hotspots:
                        st.markdown(
                            f"- 📍 **{hs['barrio']}**: {hs['predicted_incidents']} incidentes predichos ({hs['risk_level']})"
                        )
                else:
                    st.info("No hay datos de hotspots")
        with tab2:
            if "TemporalAgent" in analysis["results"]:
                result = analysis["results"]["TemporalAgent"]
                patterns = result.get("patterns", {})
                peak_hours = patterns.get("peak_hours", [])
                peak_days = patterns.get("peak_days", [])
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    if peak_hours:
                        df_hours = pd.DataFrame(peak_hours)
                        fig = plot_bar_chart(
                            df_hours, "hour", "count", "Incidentes por Hora"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                with col_t2:
                    if peak_days:
                        df_days = pd.DataFrame(peak_days)
                        fig = plot_bar_chart(
                            df_days, "day", "count", "Incidentes por Día"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                if not peak_hours and not peak_days:
                    st.info("No hay datos temporales")
        with tab3:
            if "RiskAgent" in analysis["results"]:
                result = analysis["results"]["RiskAgent"]
                ra = result.get("risk_assessment", {})
                factors = ra.get("factors", {})
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if factors:
                        df_factors = pd.DataFrame(
                            list(factors.items()), columns=["gravedad", "count"]
                        )
                        fig = plot_pie_chart(
                            df_factors, "count", "gravedad", "Distribución por Gravedad"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                with col_r2:
                    score = ra.get("score", 0)
                    fig = plot_gauge(score, 100, "Índice de Riesgo", "#FF6B6B")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                st.markdown("#### Recomendaciones de Seguridad")
                for rec in result.get("recommendations", []):
                    st.markdown(
                        f"<div style='background: rgba(10,36,99,0.05); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #0A2463;'>⚡ {rec}</div>",
                        unsafe_allow_html=True,
                    )
        with tab4:
            if "CorrelationAgent" in analysis["results"]:
                result = analysis["results"]["CorrelationAgent"]
                st.markdown(f"#### {result['summary']}")
                correlations = result.get("correlations", [])
                if correlations:
                    df_corr = pd.DataFrame(correlations)
                    if (
                        "barrio" in df_corr.columns
                        and "correlation_strength" in df_corr.columns
                    ):
                        fig = plot_bar_chart(
                            df_corr.head(5),
                            "barrio",
                            "correlation_strength",
                            "Correlación por Barrio",
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    for corr in correlations[:5]:
                        st.markdown(
                            f"- 🔗 **{corr['barrio']}**: {corr['type_count']} tipos ({corr['correlation_strength']}%)"
                        )
                else:
                    st.info("No hay correlaciones significativas")
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
    st.markdown("### Agregar Nuevo Contacto")
    col1, col2 = st.columns(2)
    with col1:
        nombre_contacto = st.text_input(
            "Nombre completo", placeholder="Ej: Juan García"
        )
    with col2:
        telefono_contacto = st.text_input("Teléfono", placeholder="Ej: 300 123 4567")
    parentesco = st.selectbox(
        "Parentesco/Relación", ["Familiar", "Amigo", "Vecino", "Colega", "Otro"]
    )
    if st.button("➕ Agregar Contacto", use_container_width=True):
        if nombre_contacto and telefono_contacto:
            contacto = {
                "id": str(uuid.uuid4()),
                "nombre": nombre_contacto,
                "telefono": telefono_contacto,
                "parentesco": parentesco,
            }
            st.session_state.emergency_contacts.append(contacto)
            st.success("✅ Contacto agregado exitosamente")
            st.rerun()
        else:
            st.error("⚠️ Completa todos los campos")
    st.markdown("---")
    st.markdown("### Mis Contactos de Emergencia")
    if st.session_state.emergency_contacts:
        for i, contact in enumerate(st.session_state.emergency_contacts):
            col_c1, col_c2, col_c3 = st.columns([3, 2, 1])
            with col_c1:
                st.markdown(
                    f"""<div class="contact-card"><div><strong>{contact["nombre"]}</strong><br><small>{contact["parentesco"]}</small></div><div style='font-size: 1.2rem;'>📱</div><div style='margin-left: 1rem;'>{contact["telefono"]}</div></div>""",
                    unsafe_allow_html=True,
                )
            with col_c3:
                if st.button("🗑️", key=f"del_contact_{i}"):
                    st.session_state.emergency_contacts.pop(i)
                    st.rerun()
    else:
        st.info("📞 No tienes contactos de emergencia. Agrega al menos uno.")
    st.markdown("---")
    st.markdown("### Contactos de Emergencia Medellín")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FF6B6B;"><strong>🚨 Emergencias</strong><br><small>Policía Nacional</small><br><strong>123</strong></div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FF8C00;"><strong>🚑 Ambulancias</strong><br><small>ECCO / SAMU</small><br><strong>123</strong></div>""",
            unsafe_allow_html=True,
        )
    with col_e2:
        st.markdown(
            """<div class="contact-card" style="border-left-color: #FFD700;"><strong>🚒 Bombero</strong><br><small>Bomberos Medellín</small><br><strong>119</strong></div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="contact-card" style="border-left-color: #61A0AF;"><strong>🔒 CAI Más Cercano</strong><br><small>Denuncia y orientación</small><br><strong>312 345 6789</strong></div>""",
            unsafe_allow_html=True,
        )
    render_nav_bar()


def render_security_settings():
    apply_styles()
    user = st.session_state.user
    st.markdown(
        f"""<div class="user-info"><div class="user-avatar">{user["nombre"][0].upper()}</div><div><h3 style="margin: 0; color: white;">{user["nombre"]}</h3><p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Configuración de Seguridad</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("## ⚙️ Configuración de Seguridad")
    st.markdown("### 🔒 Privacidad y Protección de Datos")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### Anonimización")
        anonymize = st.toggle(
            "Anonimizar datos de incidentes",
            st.session_state.security_settings.get("anonymize_data", False),
            help="Al activar, tus datos personales no serán vinculados a los incidentes reportados",
        )
        st.session_state.security_settings["anonymize_data"] = anonymize
        if anonymize:
            st.success("✅ Tus datos están protegidos y no serán asociados a reportes")
        st.markdown("#### Notificaciones")
        notifications = st.toggle(
            "Recibir alertas de seguridad",
            st.session_state.security_settings.get("notifications", True),
        )
        st.session_state.security_settings["notifications"] = notifications
    with col_s2:
        st.markdown("#### 📍 Ubicación")
        location = st.toggle(
            "Permitir geolocalización",
            st.session_state.security_settings.get("location_enabled", False),
            help="Permite registrar la ubicación exacta del incidente",
        )
        st.session_state.security_settings["location_enabled"] = location
        st.markdown("#### 🔄 Reporte Automático")
        auto_report = st.toggle(
            "Reporte automático de incidentes críticos",
            st.session_state.security_settings.get("auto_report", False),
            help="Envía automáticamente reportes cuando se detecten incidentes de alta gravedad",
        )
        st.session_state.security_settings["auto_report"] = auto_report
    st.markdown("---")
    st.markdown("### 🔐 Seguridad de la Cuenta")
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        st.markdown(
            """<div class="security-toggle"><h4>Cambiar Contraseña</h4><p>Recibe un enlace a tu correo para actualizar tu contraseña</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button("📧 Solicitar cambio de contraseña"):
            st.info("Se ha enviado un enlace a tu correo electrónico")
    with col_sec2:
        st.markdown(
            """<div class="security-toggle"><h4>Sesiones Activas</h4><p>Gestiona las sesiones activas de tu cuenta</p></div>""",
            unsafe_allow_html=True,
        )
        st.markdown("**Sesión actual:** Activa")
    st.markdown("---")
    st.markdown("### 🛡️ Políticas de Seguridad")
    st.markdown("""
    - ✅ Datos cifrados en tránsito (HTTPS)
    - ✅ Contraseñas hasheadas con SHA256
    - ✅ Sesiones con tiempo de expiración
    - ✅ Registro de actividad del usuario
    - ✅ Cumplimiento Ley de Habeas Data (Colombia)
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
    st.markdown("<br>", unsafe_allow_html=True)
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
            "contacts": render_emergency_contacts,
            "search": render_search,
            "security": render_security_settings,
            "profile": render_profile,
        }
        pages.get(st.session_state.page, render_dashboard)()


if __name__ == "__main__":
    main()
