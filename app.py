import streamlit as st
import database as db
import graphrag as grag

st.set_page_config(
    page_title="SAFE - Seguridad Inteligente",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FONT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
    
    * { font-family: 'Open Sans', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; color: #0A2463 !important; }
    
    .stApp { background: linear-gradient(135deg, #F8F9FA 0%, #E8ECEF 100%); }
    
    .stButton > button {
        background-color: #0A2463 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(10, 36, 99, 0.2) !important;
        transition: all 0.3s ease !important;
        min-height: 52px !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #0d2d52 !important; transform: scale(0.98); }
    .stButton > button:active { transform: scale(0.95); }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid #E0E0E0 !important;
        padding: 0.875rem !important;
        background-color: #FAFAFA !important;
        min-height: 52px !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #61A0AF !important;
        box-shadow: 0 0 0 3px rgba(97, 160, 175, 0.2) !important;
    }
    
    .auth-panel-left {
        position: fixed;
        top: 0; left: 0; width: 45%; height: 100vh;
        background: linear-gradient(145deg, #0A2463 0%, #0d2d6a 40%, #1a4575 70%, #61A0AF 100%);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 3rem;
    }
    .auth-panel-right {
        margin-left: 45%;
        padding: 3rem 2rem;
        display: flex; flex-direction: column; justify-content: center;
        min-height: 100vh;
    }
    .brand-icon { font-size: 5rem; margin-bottom: 1rem; }
    .brand-title { color: white; font-size: 3.5rem; font-weight: 700; margin: 0; letter-spacing: 3px; }
    .brand-subtitle { color: rgba(255,255,255,0.85); font-size: 1.2rem; text-align: center; line-height: 1.6; margin-top: 1.5rem; }
    .brand-tagline { color: rgba(255,255,255,0.5); margin-top: 4rem; font-size: 0.95rem; }
    
    .form-title { font-size: 2rem; color: #0A2463; margin-bottom: 0.5rem; }
    .form-subtitle { color: #61A0AF; margin-bottom: 2.5rem; font-size: 1.05rem; }
    
    .input-group { margin-bottom: 1.25rem; }
    .input-label { font-weight: 600; color: #0A2463; margin-bottom: 0.5rem; display: block; font-size: 0.9rem; }
    .input-hint { color: #888; font-size: 0.8rem; margin-top: 0.25rem; }
    
    .submit-btn { margin-top: 1.5rem; }
    
    .form-footer { text-align: center; margin-top: 2.5rem; color: #666; }
    .form-footer a { color: #0A2463; font-weight: 600; text-decoration: none; }
    .form-footer a:hover { text-decoration: underline; }
    
    .nav-bar {
        display: flex; justify-content: space-around;
        background: white; padding: 0.75rem 1rem;
        border-radius: 16px; box-shadow: 0 4px 20px rgba(10, 36, 99, 0.1);
        margin-bottom: 2rem; position: sticky; bottom: 1rem;
    }
    .nav-item { display: flex; flex-direction: column; align-items: center; padding: 0.5rem 1rem; border-radius: 12px; transition: all 0.3s ease; cursor: pointer; min-width: 65px; }
    .nav-item:hover { background: rgba(10, 36, 99, 0.05); }
    .nav-item.active { background: rgba(10, 36, 99, 0.1); }
    .nav-icon { font-size: 1.4rem; margin-bottom: 0.2rem; }
    .nav-label { font-size: 0.7rem; font-weight: 600; color: #0A2463; }
    
    .metric-card { background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(10, 36, 99, 0.08); text-align: center; transition: all 0.3s ease; }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(10, 36, 99, 0.12); }
    .metric-value { font-size: 2.5rem; font-weight: 700; color: #0A2463; }
    .metric-label { color: #61A0AF; font-size: 0.9rem; margin-top: 0.5rem; }
    
    .incident-card { background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(10, 36, 99, 0.08); margin-bottom: 1rem; border-left: 5px solid #61A0AF; }
    .incident-card.critica { border-left-color: #FF6B6B; }
    .incident-card.alta { border-left-color: #FF8C00; }
    .incident-card.media { border-left-color: #FFD700; }
    .incident-card.baja { border-left-color: #4CAF50; }
    
    .status-badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .status-badge.pendiente { background: #FFF3CD; color: #856404; }
    .status-badge.procesando { background: #D1ECF1; color: #0C5460; }
    .status-badge.resuelto { background: #D4EDDA; color: #155724; }
    
    .user-info { background: linear-gradient(135deg, #0A2463 0%, #1a3a7a 100%); padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 2rem; }
    .user-avatar { width: 55px; height: 55px; border-radius: 50%; background: #61A0AF; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; }
    
    .stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0 !important; padding: 0.75rem 1.5rem !important; color: #61A0AF !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] { background-color: #0A2463 !important; color: white !important; }
    
    div[data-testid="stForm"] { background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(10, 36, 99, 0.12); max-width: 500px; margin: 0 auto; }
    
    .success-box { background: #D4EDDA; border: 1px solid #C3E6CB; border-radius: 12px; padding: 1rem; color: #155724; }
    .error-box { background: #F8D7DA; border: 1px solid #F5C6CB; border-radius: 12px; padding: 1rem; color: #721C24; }
    
    .step-indicator { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; }
    .step { width: 40px; height: 40px; border-radius: 50%; background: #E0E0E0; display: flex; align-items: center; justify-content: center; font-weight: 600; color: #666; }
    .step.active { background: #0A2463; color: white; }
    .step.completed { background: #4CAF50; color: white; }
    
    .redirect-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 36, 99, 0.95); display: flex; flex-direction: column;
        align-items: center; justify-content: center; z-index: 9999;
        color: white; text-align: center;
    }
    .redirect-icon { font-size: 4rem; margin-bottom: 1rem; }
    .redirect-text { font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
    .redirect-sub { font-size: 1rem; opacity: 0.8; }
</style>
"""


def apply_styles():
    st.markdown(FONT_CSS, unsafe_allow_html=True)


def show_auth_brand_panel():
    st.markdown(
        """
        <div class="auth-panel-left">
            <div class="brand-icon">🛡️</div>
            <h1 class="brand-title">SAFE</h1>
            <p class="brand-subtitle">Seguridad Inteligente<br>y Siempre Activa</p>
            <p class="brand-tagline">Protegiendo a Medellín<br>Incidentes • Alertas • Análisis</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "redirect_to" not in st.session_state:
        st.session_state.redirect_to = None
    if "graphrag" not in st.session_state:
        st.session_state.graphrag = grag.create_graphrag_service()


def handle_register():
    st.markdown('<div class="auth-panel-right">', unsafe_allow_html=True)

    st.markdown(
        '<div class="step-indicator"><div class="step completed">✓</div><div class="step active">2</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h2 class="form-title">¡Registro Exitoso! 🎉</h2>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="form-subtitle">Ahora puedes reportar tu primer incidente</p>',
        unsafe_allow_html=True,
    )

    if st.button("🚨 Ir a Reportar Incidente", use_container_width=True):
        st.session_state.current_page = "incidents"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_register():
    apply_styles()
    show_auth_brand_panel()

    st.markdown('<div class="auth-panel-right">', unsafe_allow_html=True)

    st.markdown(
        '<div class="step-indicator"><div class="step active">1</div><div class="step">2</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<h2 class="form-title">Crear Cuenta</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="form-subtitle">Regístrate para reportar incidentes en Medellín</p>',
        unsafe_allow_html=True,
    )

    nombre = st.text_input("Nombre completo", placeholder="Ej: Juan Pérez")
    email = st.text_input("Correo electrónico", placeholder="tu@email.com")
    password = st.text_input(
        "Contraseña", placeholder="Mínimo 6 caracteres", type="password"
    )
    telefono = st.text_input("Teléfono", placeholder="Ej: 300 123 4567", type="tel")

    if st.button("Crear mi cuenta", use_container_width=True):
        if not all([nombre, email, password, telefono]):
            st.error("⚠️ Por favor completa todos los campos")
        elif len(password) < 6:
            st.error("⚠️ La contraseña debe tener al menos 6 caracteres")
        else:
            success, msg = db.create_user(nombre, email, password, telefono)
            if success:
                st.success("✅ ¡Cuenta creada exitosamente!")
                user = db.verify_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = "register_success"
                    st.rerun()
            else:
                st.error(f"❌ {msg}")

    st.markdown(
        '<p class="form-footer">¿Ya tienes cuenta? <a href="#" onclick="window.location.reload()">Inicia sesión</a></p>',
        unsafe_allow_html=True,
    )

    if st.button("← Volver al login", use_container_width=True):
        st.session_state.current_page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_login():
    apply_styles()
    show_auth_brand_panel()

    st.markdown('<div class="auth-panel-right">', unsafe_allow_html=True)

    st.markdown(
        '<h2 class="form-title">Bienvenido de nuevo</h2>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="form-subtitle">Ingresa tus credenciales para continuar</p>',
        unsafe_allow_html=True,
    )

    email = st.text_input("Correo electrónico", placeholder="tu@email.com")
    password = st.text_input("Contraseña", placeholder="Tu contraseña", type="password")

    if st.button("Iniciar Sesión", use_container_width=True):
        if not all([email, password]):
            st.error("⚠️ Por favor completa todos los campos")
        else:
            user = db.verify_user(email, password)
            if user:
                st.success("✅ ¡Bienvenido!")
                st.session_state.user = user
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error("❌ Email o contraseña incorrectos")

    st.markdown(
        '<p class="form-footer">¿No tienes cuenta? <a href="#">Regístrate aquí</a></p>',
        unsafe_allow_html=True,
    )

    if st.button("Crear una cuenta", use_container_width=True):
        st.session_state.current_page = "register"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_incidents():
    apply_styles()

    if not st.session_state.user:
        st.session_state.current_page = "login"
        st.rerun()
        return

    user = st.session_state.user

    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div>
                <h2 style="margin: 0;">📊 Reporte de Incidentes</h2>
                <p style="color: #61A0AF; margin: 0;">Bienvenido, """
        + user["nombre"]
        + """</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["➕ Nuevo Reporte", "📋 Mis Reportes", "🔍 Buscar"])

    with tab1:
        st.markdown("### Reportar Nuevo Incidente")

        col1, col2 = st.columns(2)
        with col1:
            tipo = st.selectbox(
                "Tipo de incidente",
                [
                    "Seleccionar...",
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
            "Descripción detallada", placeholder="Describe el incidente con detalle..."
        )

        col3, col4 = st.columns(2)
        with col3:
            ubicacion = st.text_input("Dirección", placeholder="Ej: Cra. 48 #Sur-45")
        with col4:
            barrio = st.text_input("Barrio", placeholder="Ej: El Poblado")

        if st.button("💾 Reportar Incidente", use_container_width=True, type="primary"):
            if tipo == "Seleccionar...":
                st.error("⚠️ Selecciona un tipo de incidente")
            elif not descripcion:
                st.error("⚠️ Agrega una descripción")
            else:
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
                }
                st.session_state.graphrag.add_incident_context(
                    user["id"], incident_data
                )
                st.success("✅ Incidente reportado exitosamente")
                st.rerun()

    with tab2:
        incidents = db.get_incidents(user["id"])
        if incidents:
            for inc in incidents:
                g = inc.get("gravedad", "baja").lower()
                st.markdown(
                    f"""
                    <div class="incident-card {g}">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <strong style="color: #0A2463; font-size: 1.1rem;">{inc.get("tipo")}</strong>
                                <p style="margin: 0.5rem 0; color: #555;">{inc.get("descripcion", "Sin descripción")}</p>
                                <small style="color: #888;">📍 {inc.get("barrio", "N/A")} • {inc.get("ubicacion", "N/A")}</small>
                            </div>
                            <span class="status-badge {inc.get("estado", "pendiente")}">{inc.get("estado", "pendiente")}</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("📭 No has reportado incidentes aún. ¡Sé el primero en reportar!")

    with tab3:
        st.markdown("### Búsqueda con GraphRAG")
        query = st.text_input(
            "Buscar incidentes", placeholder="Ej: hurtos en El Poblado..."
        )
        if query and st.button("🔍 Buscar"):
            if st.session_state.graphrag.is_available():
                results = st.session_state.graphrag.search_incidents(query)
                if results:
                    st.markdown(f"**{len(results)} resultados encontrados:**")
                    for r in results:
                        st.markdown(
                            f"<div class='incident-card'><p>{r.get('content', '')}</p><small>Similitud: {r.get('score', 0):.2f}</small></div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No se encontraron resultados")
            else:
                st.warning("GraphRAG no disponible. Configure ZEP_API_KEY.")


def show_nav():
    nav_items = [
        ("🏠", "Inicio"),
        ("🔔", "Alertas"),
        ("📊", "Incidentes"),
        ("👤", "Perfil"),
    ]
    cols = st.columns(4)
    for i, (icon, label) in enumerate(nav_items):
        with cols[i]:
            active = st.session_state.current_page == label.lower() or (
                label == "Inicio" and st.session_state.current_page == "home"
            )
            cls = "nav-item active" if active else "nav-item"
            st.markdown(
                f"<div class='{cls}'><span class='nav-icon'>{icon}</span><span class='nav-label'>{label}</span></div>",
                unsafe_allow_html=True,
            )
            if st.button(icon, key=f"nav_{i}"):
                page_map = {
                    "Inicio": "home",
                    "Alertas": "alerts",
                    "Incidentes": "incidents",
                    "Perfil": "profile",
                }
                st.session_state.current_page = page_map[label]
                st.rerun()


def render_home():
    apply_styles()
    user = st.session_state.user

    stats = db.get_incident_stats()

    col1, col2, col3 = st.columns(3)
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
            "<div class='metric-card'><div class='metric-value'>🛡️</div><div class='metric-label'>SAFE Activo</div></div>",
            unsafe_allow_html=True,
        )

    show_nav()

    if st.button(
        "🚨 Reportar Nuevo Incidente", use_container_width=True, type="primary"
    ):
        st.session_state.current_page = "incidents"
        st.rerun()


def render_alerts():
    apply_styles()
    st.markdown("### 🔔 Centro de Alertas")
    stats = db.get_incident_stats()

    alertas = stats.get("por_gravedad", {}).get("crítica", 0) + stats.get(
        "por_gravedad", {}
    ).get("alta", 0)
    if alertas > 0:
        st.markdown(
            f"<div style='background: #FF6B6B; color: white; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; animation: pulse 2s infinite;'>🔔 {alertas} alertas activas requieren atención</div>",
            unsafe_allow_html=True,
        )

    top = list(stats.get("top_barrios", {}).items())[:5]
    if top:
        for barrio, count in top:
            st.markdown(
                f"<div class='incident-card'><div style='display: flex; justify-content: space-between;'><strong>📍 {barrio}</strong><span style='background: #FF6B6B; color: white; padding: 0.25rem 0.75rem; border-radius: 20px;'>{count}</span></div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No hay alertas activas")

    show_nav()


def render_profile():
    apply_styles()
    user = st.session_state.user

    st.markdown(
        f"""
        <div class="user-info">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="user-avatar">{user["nombre"][0].upper()}</div>
                <div>
                    <h3 style="margin: 0; color: white;">{user["nombre"]}</h3>
                    <p style="margin: 0; opacity: 0.8;">{user["email"]}</p>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"<div style='text-align: center;'><div class='user-avatar' style='width: 100px; height: 100px; font-size: 2.5rem; margin: 0 auto;'>{user['nombre'][0].upper()}</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='metric-card'><h3 style='color: #0A2463;'>{user['nombre']}</h3><p><strong>Email:</strong> {user['email']}</p><p><strong>Teléfono:</strong> {user['telefono']}</p></div>",
            unsafe_allow_html=True,
        )

    show_nav()

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.user = None
        st.session_state.current_page = "login"
        st.rerun()


def main():
    init_session()

    if not st.session_state.user:
        if st.session_state.current_page == "register":
            render_register()
        elif st.session_state.current_page == "register_success":
            apply_styles()
            handle_register()
        else:
            render_login()
    else:
        pages = {
            "home": render_home,
            "alerts": render_alerts,
            "incidents": render_incidents,
            "profile": render_profile,
        }
        if st.session_state.current_page in pages:
            pages[st.session_state.current_page]()
        else:
            render_home()


if __name__ == "__main__":
    main()
