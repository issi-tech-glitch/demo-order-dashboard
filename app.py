import streamlit as st

# 1. Seiteneinstellungen (Das ändert das "app" im Browser-Tab!)
st.set_page_config(
    page_title="Clarissa | Dashboard Zentrale", 
    layout="wide", 
    page_icon="🚀"
)

# --- STYLING ---
# Ein bisschen CSS, um die unschöne Standard-Navigation oben rechts auszublenden 
# und die Kacheln hübsch zu machen.
st.markdown("""
    <style>
    .dashboard-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    html[data-theme="dark"] .dashboard-card {
        background-color: #1e2430;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("Dashboard Hub")
st.markdown("Alle Systeme laufen stabil. 🟢")
st.write("---")

# --- KACHELN FÜR DASHBOARDS ---
st.subheader("Verfügbare Dashboards")

# Wir erstellen zwei Spalten für eine schöne Grid-Ansicht
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="dashboard-card">
            <h3>📦 Live Bestell-Dashboard</h3>
            <p>Überwachung der aktuellen E-Mail-Bestellungen, automatische Datenextraktion und Abgleich mit dem Supabase-Lagerbestand.</p>
        </div>
    """, unsafe_allow_html=True)
    # Ein nativer Streamlit-Button, der optisch darunter sitzt
    st.info("← Wähle 'demo-order-dashboard' in der linken Navigation")

