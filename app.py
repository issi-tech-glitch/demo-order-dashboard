import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
import altair as alt

# --- KONFIGURATION ---
st.set_page_config(page_title="Bestell-Dashboard", layout="wide", page_icon="📦")

# --- HAUPTPROGRAMM ---
st.title("📦 Live Bestell-Dashboard")
try:
    conn = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=st.secrets["connections"]["supabase"]["url"],
        key=st.secrets["connections"]["supabase"]["key"]
    )
except Exception as e:
    st.error(f"Verbindungsfehler: {e}")
    st.stop()

with st.sidebar:
    st.header("Einstellungen")
    if st.button("🔄 Daten aktualisieren"):
        st.cache_data.clear()
        st.rerun()
    st.write("---")
    st.write("Server-Region: **Irland (EU)**")

col1, col2 = st.columns([1, 2])
df_products = pd.DataFrame()

with col1:
    st.subheader("📊 Lagerbestand")
    try:
        res_products = conn.table("products").select("sku, name, stock").execute()
        if res_products.data:
            df_products = pd.DataFrame(res_products.data)
            st.dataframe(
                df_products,
                column_config={
                    "sku": "SKU",
                    "name": "Produktname",
                    "stock": "Bestand"
                },
                hide_index=True,
                width="stretch"
            )
    except Exception as e:
        st.error(f"Fehler beim Laden der Produkte: {e}")

with col2:
    st.subheader("📜 Bestell-Historie")
    try:
        res_orders = conn.table("orders").select(
            "created_at, customer_name, quantity, products(name, sku)"
        ).order("created_at", desc=True).execute()

        if res_orders.data:
            flattened_data = []
            for row in res_orders.data:
                flattened_data.append({
                    "Datum": pd.to_datetime(row["created_at"]).strftime("%d.%m.%y %H:%M"),
                    "Kunde": row["customer_name"],
                    "Produkt": row["products"]["name"],
                    "SKU": row["products"]["sku"],
                    "Menge": row["quantity"]
                })
            
            st.table(flattened_data)
        else:
            st.info("Noch keine Bestellungen in der Datenbank.")
    except Exception as e:
        st.error(f"Fehler beim Laden der Bestellungen: {e}")

# --- BALKENDIAGRAMM UNTEN ---
st.write("---")
st.subheader("📈 Bestandsübersicht")

if not df_products.empty:
    chart = alt.Chart(df_products).mark_bar(color='#1f77b4').encode(
        x=alt.X('name:N', sort='-y', title='Produkt'),
        y=alt.Y('stock:Q', title='Menge im Lager'),
        tooltip=['name', 'stock']
    ).properties(height=400)
    
    st.altair_chart(chart, theme="streamlit", width="stretch") # Neue Syntax
else:
    st.info("Keine Daten für das Diagramm verfügbar.")

# Footer
st.write("---")
st.caption("Datenquelle: Supabase (AWS Ireland) | Automatisierung: Make.com")