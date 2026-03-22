import streamlit as st
import database as db
import graphrag as grag

st.set_page_config(
    page_title="SAFE - Seguridad Inteligente", page_icon="🛡️", layout="wide"
)

SAFE_COLORS = {
    "primary": "#0A2463",
    "secondary": "#61A0AF",
    "background": "#F8F9FA",
    "emphasis": "#FF6B6B",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
* { font-family: 'Open Sans', sans-serif; }
h1,h2,h3,h4 { font-family: 'Montserrat', sans-serif; font-weight: 700; color: #0A2463; }
.stApp { background: #F8F9FA; }
.stButton > button { background-color: #0A2463 !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important; min-height: 48px !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div { border-radius: 10px !important; border: 2px solid #E0E0E0 !important; padding: 0.75rem !important; min-height: 48px !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #61A0AF !important; box-shadow: 0 0 0 2px rgba(97,160,175,0.2) !important; }
.auth-container { display: flex; min-height: 100vh; }
.auth-left { flex: 1; background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 50%, #61A0AF 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 3rem; color: white; text-align: center; }
.auth-right { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 3rem; }
.auth-title { font-size: 2.5rem; margin-bottom: 0.5rem; }
.auth-subtitle { font-size: 1.1rem; opacity: 0.85; margin-bottom: 2rem; }
.auth-form { max-width: 400px; margin: 0 auto; }
.input-group { margin-bottom: 1.25rem; }
.input-label { font-weight: 600; color: #0A2463; margin-bottom: 0.5rem; display: block; }
.card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(10,36,99,0.08); margin-bottom: 1rem; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #E0E0E0; }
.metric-card { background: white; border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 16px rgba(10,36,99,0.08); }
.metric-value { font-size: 2.5rem; font-weight: 700; color: #0A2463; font-family: 'Montserrat', sans-serif; }
.metric-label { color: #61A0AF; font-size: 0.9rem; margin-top: 0.5rem; }
.incident-item { background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #61A0AF; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.incident-item.critica { border-left-color: #FF6B6B; }
.incident-item.alta { border-left-color: #FF8C00; }
.incident-item.media { border-left-color: #FFD700; }
.incident-item.baja { border-left-color: #4CAF50; }
.status-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.status-badge.pendiente { background: #FFF3CD; color: #856404; }
.status-badge.procesando { background: #D1ECF1; color: #0C5460; }
.status-badge.resuelto { background: #D4EDDA; color: #155724; }
.user-info { background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 100%); padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }
.user-avatar { width: 55px; height: 55px; border-radius: 50%; background: #61A0AF; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; }
.bottom-nav { display: flex; justify-content: space-around; background: white; padding: 1rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(10,36,99,0.1); margin-top: 2rem; }
.nav-btn { display: flex; flex-direction: column; align-items: center; padding: 0.75rem 1.5rem; border-radius: 12px; border: none; background: transparent; cursor: pointer; transition: all 0.3s; }
.nav-btn:hover { background: rgba(10,36,99,0.05); }
.nav-btn.active { background: rgba(10,36,99,0.1); }
.alert-banner { background: #FF6B6B; color: white; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.8; } }
.tab-content { padding: 1rem 0; }
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


def render_login_register():
    apply_styles()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; padding: 2rem; background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 50%, #61A0AF 100%); color: white; text-align: center;">
                <div style="font-size: 5rem; margin-bottom: 1rem;">🛡️</div>
                <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">SAFE</h1>
                <p style="font-size: 1.2rem; opacity: 0.9;">Seguridad Inteligente<br>y Siempre Activa</p>
                <p style="margin-top: 3rem; opacity: 0.7; font-size: 0.95rem;">Medellín, Colombia<br>GraphRAG powered by Zep</p>
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
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{user["email"]}</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{stats.get('total', 0)}</div><div class='metric-label'>Total Incidentes</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #FF6B6B;'>{stats.get('por_gravedad', {}).get('crítica', 0)}</div><div class='metric-label'>Casos Críticos</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value' style='color: #61A0AF;'>{len(stats.get('por_tipo', {}))}</div><div class='metric-label'>Tipos de Incidentes</div></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            "<div class='metric-card'><div class='metric-value'>🛡️</div><div class='metric-label'>SAFE Activo</div></div>",
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3 = st.tabs(["📊 Resumen", "📍 Por Barrio", "📋 Por Tipo"])

    with tab1:
        st.markdown("### Últimos Incidentes Reportados")
        user_incidents = db.get_incidents(user["id"])[:5]
        if user_incidents:
            for inc in user_incidents:
                g = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-item {g}">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <strong style="color: #0A2463;">{inc.get("tipo")}</strong>
                                <p style="margin: 0.5rem 0; color: #555; font-size: 0.95rem;">{inc.get("descripcion", "Sin descripción")}</p>
                                <small style="color: #888;">📍 {inc.get("barrio", "N/A")} • {inc.get("ubicacion", "N/A")}</small>
                            </div>
                            <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado", "pendiente")}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("📭 No tienes incidentes reportados aún")

        if st.button(
            "🚨 Reportar Nuevo Incidente", use_container_width=True, type="primary"
        ):
            st.session_state.page = "incidents"
            st.rerun()

    with tab2:
        st.markdown("### Incidentes por Barrio")
        top_barrios = stats.get("top_barrios", {})
        if top_barrios:
            for barrio, count in list(top_barrios.items())[:10]:
                st.markdown(
                    f"""
                    <div class="incident-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #0A2463;">📍 {barrio}</strong>
                            <span style="background: #0A2463; color: white; padding: 0.25rem 1rem; border-radius: 20px; font-weight: 600;">{count}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No hay datos de barrios")

    with tab3:
        st.markdown("### Incidentes por Tipo")
        por_tipo = stats.get("por_tipo", {})
        if por_tipo:
            for tipo, count in por_tipo.items():
                st.markdown(
                    f"""
                    <div class="incident-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #0A2463;">{tipo}</span>
                            <span style="background: #61A0AF; color: white; padding: 0.25rem 1rem; border-radius: 20px; font-weight: 600;">{count}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No hay datos de tipos de incidente")

    alertas = stats.get("por_gravedad", {}).get("crítica", 0) + stats.get(
        "por_gravedad", {}
    ).get("alta", 0)
    if alertas > 0:
        st.markdown(
            f"<div class='alert-banner'>🔔 {alertas} alertas activas requieren atención</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="bottom-nav">
            <button class="nav-btn active">🏠<br><small>Inicio</small></button>
            <button class="nav-btn" onclick="window.location.reload()">📊<br><small>Resumen</small></button>
            <button class="nav-btn" onclick="window.location.reload()">🔔<br><small>Alertas</small></button>
            <button class="nav-btn" onclick="window.location.reload()">👤<br><small>Perfil</small></button>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_nav2:
        if st.button("📊 Incidentes", use_container_width=True):
            st.session_state.page = "incidents"
            st.rerun()
    with col_nav3:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
    with col_nav4:
        if st.button("👤 Perfil", use_container_width=True):
            st.session_state.page = "profile"
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
                "Tipo de incidente",
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
            gravedad = st.selectbox(
                "Nivel de gravedad", ["baja", "media", "alta", "crítica"]
            )

        descripcion = st.text_area(
            "Descripción detallada del incidente",
            placeholder="Describe el incidente con el mayor detalle posible...",
        )

        col3, col4 = st.columns(2)
        with col3:
            ubicacion = st.text_input(
                "Dirección/Ubicación", placeholder="Ej: Cra. 48 #Sur-45, El Poblado"
            )
        with col4:
            barrio = st.text_input(
                "Barrio", placeholder="Ej: El Poblado, Laureles, Belén"
            )

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
                st.success("✅ Incidente reportado exitosamente en Medellín")
                st.rerun()
            else:
                st.error("⚠️ Completa todos los campos del incidente")

    with tab2:
        st.markdown("### Mis Incidentes Reportados")
        incidents = db.get_incidents(user["id"])

        if incidents:
            for inc in incidents:
                g = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-item {g}">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <strong style="color: #0A2463; font-size: 1.1rem;">{inc.get("tipo")}</strong>
                                <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "Sin descripción")}</p>
                                <p style="margin: 0; color: #888; font-size: 0.85rem;">📍 {inc.get("barrio", "N/A")} - {inc.get("ubicacion", "N/A")}</p>
                                <small style="color: #AAA;">🕐 {inc.get("fecha", "N/A")}</small>
                            </div>
                            <div style="text-align: right;">
                                <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado", "pendiente")}</span>
                                <p style="margin: 0.5rem 0 0 0; color: #888; font-size: 0.8rem;">Gravedad: {inc.get("gravedad", "N/A")}</p>
                            </div>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("📭 No has reportado incidentes aún. ¡Sé el primero en reportar!")

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_nav2:
        if st.button("📊 Incidentes", use_container_width=True):
            st.session_state.page = "incidents"
            st.rerun()
    with col_nav3:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
    with col_nav4:
        if st.button("👤 Perfil", use_container_width=True):
            st.session_state.page = "profile"
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

    st.markdown("## 🔍 Búsqueda semántica con GraphRAG")
    st.markdown("*Busca incidentes relacionados usando inteligencia artificial*")

    query = st.text_input(
        "Buscar incidentes",
        placeholder="Ej: hurtos en El Poblado, accidentes en la Avenida Oriental...",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        limit = st.selectbox("Resultados", [5, 10, 20])
    with col2:
        st.write("")

    if st.button("🔍 Buscar con GraphRAG", use_container_width=True, type="primary"):
        if query:
            if st.session_state.graphrag.is_available():
                with st.spinner("Buscando..."):
                    results = st.session_state.graphrag.search_incidents(
                        query, limit=limit
                    )

                    if results:
                        st.success(f"✅ {len(results)} resultados encontrados")

                        for r in results:
                            metadata = r.get("metadata", {})
                            st.markdown(
                                f"""
                                <div class="incident-item">
                                    <p style="color: #0A2463; font-weight: 600;">{r.get("content", "")}</p>
                                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                                        <small style="color: #888;">📍 {metadata.get("barrio", "N/A")}</small>
                                        <small style="color: #888;">🏷️ {metadata.get("tipo", "N/A")}</small>
                                        <small style="color: #888;">⚠️ {metadata.get("gravedad", "N/A")}</small>
                                        <small style="color: #61A0AF;">📊 Similitud: {r.get("score", 0):.2f}</small>
                                    </div>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No se encontraron resultados para tu búsqueda")
            else:
                st.warning(
                    "⚠️ GraphRAG no disponible. Configure ZEP_API_KEY en secrets."
                )
                st.markdown("""
                    **Nota:** Para activar GraphRAG:
                    1. Obtén tu API key en [Zep Cloud](https://www.zep.cloud)
                    2. Agrega `ZEP_API_KEY` en los secrets de Streamlit Cloud
                """)

    st.markdown("---")
    st.markdown("### 💡 Sugerencias de búsqueda")

    suggestions = [
        "hurtos en El Poblado",
        "accidentes en Laureles",
        "vandalismo en el centro",
        "robos vehiculares en Envigado",
        "agresiones en Estadio",
    ]

    cols = st.columns(len(suggestions))
    for i, sug in enumerate(suggestions):
        with cols[i]:
            if st.button(sug, key=f"sug_{i}"):
                st.session_state.query = sug
                st.rerun()

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_nav2:
        if st.button("📊 Incidentes", use_container_width=True):
            st.session_state.page = "incidents"
            st.rerun()
    with col_nav3:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
    with col_nav4:
        if st.button("👤 Perfil", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()


def render_profile():
    apply_styles()
    user = st.session_state.user

    stats = db.get_incident_stats()
    user_incidents = db.get_incidents(user["id"])

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
    with col1:
        st.metric("Incidentes reportados", len(user_incidents))
    with col2:
        criticos = sum(1 for i in user_incidents if i.get("gravedad") == "crítica")
        st.metric("Casos críticos", criticos)
    with col3:
        st.metric("Total ciudad", stats.get("total", 0))

    st.markdown("### 📋 Mi Información")
    st.markdown(
        f"""
        <div class="card">
            <p><strong>Nombre:</strong> {user["nombre"]}</p>
            <p><strong>Email:</strong> {user["email"]}</p>
            <p><strong>Teléfono:</strong> {user["telefono"]}</p>
            <p><strong>ID Usuario:</strong> <code style="font-size: 0.8rem;">{user["id"]}</code></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.graphrag.is_available():
        st.markdown("### 📊 Análisis con GraphRAG")
        patterns = st.session_state.graphrag.analyze_incident_patterns(user["id"])

        if patterns.get("total_incidents", 0) > 0:
            st.markdown(
                f"**Total incidentes analizados:** {patterns['total_incidents']}"
            )

            if patterns.get("incident_types"):
                st.markdown("**Tipos de incidentes:**")
                for tipo, count in patterns["incident_types"].items():
                    st.markdown(f"- {tipo}: {count}")

            if patterns.get("recommendations"):
                st.markdown("### 💡 Recomendaciones")
                for rec in patterns["recommendations"]:
                    st.info(rec)
        else:
            st.info("No hay suficientes datos para análisis. Reporta más incidentes.")

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_nav2:
        if st.button("📊 Incidentes", use_container_width=True):
            st.session_state.page = "incidents"
            st.rerun()
    with col_nav3:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
    with col_nav4:
        if st.button("👤 Perfil", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()


def main():
    init_session()

    if not st.session_state.user:
        render_login_register()
    else:
        pages = {
            "dashboard": render_dashboard,
            "incidents": render_incidents,
            "search": render_search,
            "profile": render_profile,
        }

        if st.session_state.page in pages:
            pages[st.session_state.page]()
        else:
            render_dashboard()


if __name__ == "__main__":
    main()
