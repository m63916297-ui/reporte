import streamlit as st
import database as db
import graphrag as grag
import predictive_agents as agents

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
.agent-card { background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border: 2px solid #61A0AF; }
.agent-card.active { border-color: #0A2463; background: rgba(10,36,99,0.03); }
.graph-node { background: #61A0AF; border-radius: 50%; padding: 0.5rem 1rem; display: inline-block; color: white; font-weight: 600; margin: 0.25rem; }
.graph-edge { border-left: 2px dashed #888; margin-left: 1rem; padding-left: 0.5rem; }
.hotspot-badge { background: #FF6B6B; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; }
.risk-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.risk-badge.critico { background: #FF6B6B; color: white; }
.risk-badge.alto { background: #FF8C00; color: white; }
.risk-badge.medio { background: #FFD700; color: #333; }
.risk-badge.bajo { background: #4CAF50; color: white; }
.recommendation-item { background: linear-gradient(90deg, rgba(10,36,99,0.05) 0%, transparent 100%); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #0A2463; }
.status-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.status-badge.pendiente { background: #FFF3CD; color: #856404; }
.status-badge.procesando { background: #D1ECF1; color: #0C5460; }
.status-badge.resuelto { background: #D4EDDA; color: #155724; }
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
                else:
                    st.warning("⚠️ Completa todos los campos")

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

    if st.button("🔮 Ejecutar Análisis Predictivo", use_container_width=True):
        st.session_state.page = "predictive"
        st.rerun()

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Resumen", "🔥 Hotspots", "🔗 Grafo", "📋 Por Tipo"]
    )

    with tab1:
        st.markdown("### Últimos Incidentes")
        user_incidents = db.get_incidents(user["id"])[:5]
        if user_incidents:
            for inc in user_incidents:
                g = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-item {g}">
                        <strong style="color: #0A2463;">{inc.get("tipo")}</strong>
                        <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p>
                        <small style="color: #888;">📍 {inc.get("barrio", "N/A")} • {inc.get("gravedad", "N/A")}</small>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No tienes incidentes reportados")

    with tab2:
        st.markdown("### 🔥 Zonas Calientes (Hotspots)")
        if st.session_state.graphrag.is_available():
            hotspots = st.session_state.graphrag.get_hotspots()
            if hotspots:
                for i, hs in enumerate(hotspots[:5]):
                    st.markdown(
                        f"""
                        <div class="incident-item">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: #0A2463;">📍 {hs["barrio"]}</strong>
                                    <p style="margin: 0.25rem 0 0 0; color: #888;">{hs["count"]} incidentes</p>
                                </div>
                                <span class="hotspot-badge">#{i + 1}</span>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No hay datos de hotspots disponibles")
        else:
            st.warning("GraphRAG no disponible. Configure ZEP_API_KEY.")

    with tab3:
        st.markdown("### 🔗 Grafo de Correlación")
        st.markdown("*Visualización de relaciones entre incidentes*")

        graph_data = st.session_state.graphrag.build_incident_graph(user["id"])

        if graph_data.get("nodes"):
            st.markdown(
                f"**Nodos:** {len(graph_data['nodes'])} | **Conexiones:** {len(graph_data['edges'])}"
            )

            clusters = graph_data.get("clusters", {})
            barrio_clusters = clusters.get("por_barrio", {})

            if barrio_clusters:
                st.markdown("#### Clusters por Barrio")
                for barrio, node_ids in list(barrio_clusters.items())[:5]:
                    if len(node_ids) > 1:
                        st.markdown(
                            f"""
                            <div style="background: rgba(97,160,175,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                                <strong style="color: #0A2463;">📍 {barrio}</strong>
                                <div style="margin-top: 0.5rem;">
                                    {"".join([f'<span class="graph-node">{n}</span>' for n in node_ids[:5]])}
                                </div>
                                <small style="color: #888;">{len(node_ids)} nodos conectados</small>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
        else:
            st.info(
                "No hay suficientes datos para generar el grafo. Reporta más incidentes."
            )

    with tab4:
        st.markdown("### Incidentes por Tipo")
        por_tipo = stats.get("por_tipo", {})
        if por_tipo:
            for tipo, count in por_tipo.items():
                st.markdown(
                    f"""
                    <div class="incident-item">
                        <div style="display: flex; justify-content: space-between;">
                            <span>{tipo}</span>
                            <span style="background: #61A0AF; color: white; padding: 0.25rem 1rem; border-radius: 20px; font-weight: 600;">{count}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

    alertas = stats.get("por_gravedad", {}).get("crítica", 0) + stats.get(
        "por_gravedad", {}
    ).get("alta", 0)
    if alertas > 0:
        st.error(f"🔔 {alertas} alertas activas requieren atención")

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

    tab1, tab2 = st.tabs(["➕ Nuevo Reporte", "📋 Mis Reportes"])

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
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>{inc.get("tipo")}</strong>
                                <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "N/A")}</p>
                                <small>📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}</small>
                            </div>
                            <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado", "pendiente")}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No has reportado incidentes aún")

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
    st.markdown(
        "*Sistema multi-agente para predicción de incidentes y evaluación de riesgo*"
    )

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

        st.markdown(
            f"**Nivel de Riesgo:** <span class='risk-badge {analysis['risk_level']}'>{analysis['risk_level'].upper()}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**Confianza del análisis:** {analysis['confidence']:.1f}%")
        st.markdown(f"**Agentes activos:** {analysis['agent_count']}")

        st.markdown("---")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["🌡️ Hotspot", "⏰ Temporal", "⚠️ Riesgo", "🔗 Correlación"]
        )

        with tab1:
            if "HotspotAgent" in analysis["results"]:
                result = analysis["results"]["HotspotAgent"]
                st.markdown(f"### {result['summary']}")

                if result.get("hotspots"):
                    for hs in result["hotspots"]:
                        st.markdown(
                            f"""
                            <div class="incident-item">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong>📍 {hs["barrio"]}</strong>
                                        <p style="margin: 0.25rem 0; color: #888;">Tipo probable: {hs["likely_type"]}</p>
                                        <p style="margin: 0; color: #888;">Incidentes predichos: {hs["predicted_incidents"]}</p>
                                    </div>
                                    <span class="risk-badge {hs["risk_level"]}">{hs["risk_level"].upper()}</span>
                                </div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

        with tab2:
            if "TemporalAgent" in analysis["results"]:
                result = analysis["results"]["TemporalAgent"]
                st.markdown(f"### {result['summary']}")

                patterns = result.get("patterns", {})
                if patterns.get("peak_hours"):
                    st.markdown("#### Horarios Pico")
                    for ph in patterns["peak_hours"][:3]:
                        st.markdown(f"- **{ph['hour']}:00** - {ph['count']} incidentes")

                if patterns.get("peak_days"):
                    st.markdown("#### Días Pico")
                    for pd in patterns["peak_days"]:
                        st.markdown(f"- **{pd['day']}** - {pd['count']} incidentes")

        with tab3:
            if "RiskAgent" in analysis["results"]:
                result = analysis["results"]["RiskAgent"]
                st.markdown(f"### {result['summary']}")

                ra = result.get("risk_assessment", {})
                st.markdown(f"**Score de riesgo:** {ra.get('score', 0)}%")

                if ra.get("factors"):
                    st.markdown("#### Distribución por Gravedad")
                    for g, count in ra["factors"].items():
                        if count > 0:
                            st.markdown(f"- **{g}:** {count}")

                st.markdown("#### Recomendaciones de Seguridad")
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
                        f"""
                        <div class="incident-item">
                            <strong>📍 {corr["barrio"]}</strong>
                            <p style="margin: 0.5rem 0; color: #555;">Tipos correlacionados: {", ".join(corr["incident_types"])}</p>
                            <small style="color: #61A0AF;">Fuerza de correlación: {corr["correlation_strength"]}%</small>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

        st.markdown("---")
        st.markdown("### 📋 Recomendaciones Consolidadas")

        for rec in analysis.get("consolidated_recommendations", [])[:5]:
            priority_emoji = (
                "🔴" if rec["priority"] >= 3 else "🟡" if rec["priority"] >= 2 else "🟢"
            )
            st.markdown(
                f"{priority_emoji} **{rec['text']}** <small>({rec['source']})</small>"
            )
    else:
        st.info("👆 Ejecuta el análisis predictivo para ver los resultados")
        st.markdown("""
            **Agentes disponibles:**
            - 🌡️ **HotspotAgent**: Predice zonas calientes
            - ⏰ **TemporalAgent**: Analiza patrones temporales
            - ⚠️ **RiskAgent**: Evalúa nivel de riesgo
            - 🔗 **CorrelationAgent**: Encuentra correlaciones
        """)

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
        "Buscar incidentes",
        placeholder="Ej: hurtos en El Poblado, accidentes en Laureles...",
    )

    if st.button("🔍 Buscar", use_container_width=True, type="primary"):
        if query:
            if st.session_state.graphrag.is_available():
                with st.spinner("Buscando..."):
                    results = st.session_state.graphrag.search_incidents(query)
                    if results:
                        st.success(f"✅ {len(results)} resultados encontrados")
                        for r in results:
                            metadata = r.get("metadata", {})
                            st.markdown(
                                f"""
                                <div class="incident-item">
                                    <p>{r.get("content", "")}</p>
                                    <small>📍 {metadata.get("barrio", "N/A")} | 🏷️ {metadata.get("tipo", "N/A")} | 📊 {r.get("score", 0):.2f}</small>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No se encontraron resultados")
            else:
                st.warning("GraphRAG no disponible. Configure ZEP_API_KEY.")

    st.markdown("### 💡 Sugerencias")
    suggestions = [
        "hurtos en El Poblado",
        "accidentes en Laureles",
        "vandalismo en centro",
    ]
    for sug in suggestions:
        if st.button(sug):
            st.session_state.query = sug
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
            "Critical", sum(1 for i in user_incidents if i.get("gravedad") == "crítica")
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
