import streamlit as st

st.set_page_config(
    page_title="Intelligent Sales Forecasting",
    page_icon="📊",
    layout="wide"
)

try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-copy">
            <div class="eyebrow">Sales intelligence workspace</div>
            <h1>Forecast revenue, optimize inventory, and make decisions faster.</h1>
            <p class="hero-text">
                A modern command center for tracking performance, exploring patterns,
                training models, and turning sales data into sharper operational moves.
            </p>
            <div class="hero-actions">
                <span class="pill primary">Live forecasting</span>
                <span class="pill">Inventory planning</span>
                <span class="pill">Executive reporting</span>
            </div>
        </div>
        <div class="hero-panel">
            <div class="panel-label">Today at a glance</div>
            <div class="panel-grid">
                <div class="panel-card">
                    <span>Revenue</span>
                    <strong>₹15.2M</strong>
                    <small>+12% vs last period</small>
                </div>
                <div class="panel-card">
                    <span>Orders</span>
                    <strong>24,580</strong>
                    <small>+8% order growth</small>
                </div>
                <div class="panel-card">
                    <span>Accuracy</span>
                    <strong>95.6%</strong>
                    <small>Model confidence</small>
                </div>
                <div class="panel-card">
                    <span>Profit</span>
                    <strong>22.5%</strong>
                    <small>+5% margin gain</small>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-heading">
        <h2>Project Modules</h2>
        <p>Everything is organized into focused pages so you can move from raw data to action quickly.</p>
    </div>
    """,
    unsafe_allow_html=True
)

modules = [
    ("Data Upload", "Bring in raw sales files and prepare the workspace.", "pages/Data_Upload.py", "📂"),
    ("Preprocessing", "Clean, transform, and align the dataset for analysis.", "pages/Data_Preprocessing.py", "🔧"),
    ("EDA & Insights", "Surface trends, seasonality, and high-value segments.", "pages/EDA_Analysis.py", "📈"),
    ("Model Training", "Build and evaluate forecasting models with clear metrics.", "pages/Model_Training.py", "🤖"),
    ("Sales Forecasting", "Generate future demand estimates with scenario views.", "pages/Sales_Forecasting.py", "🔮"),
    ("Inventory Optimization", "Balance stock levels against projected demand.", "pages/Inventory_Optimization.py", "📦"),
    ("Reports", "Summarize performance in a business-ready format.", "pages/Reports.py", "📑"),
    ("Dashboard", "Track KPIs and visualization in one executive view.", "pages/Dashboard.py", "📊"),
]

for row_start in range(0, len(modules), 4):
    cols = st.columns(4)
    for offset, (title, description, page_path, icon) in enumerate(modules[row_start:row_start + 4]):
        with cols[offset]:
            st.markdown(
                f"""
                <div class="module-card">
                    <div class="module-index">0{row_start + offset + 1}</div>
                    <h3>{icon} {title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.page_link(page_path, label=f"Open {title}", icon=icon)

st.markdown(
    """
    <div class="callout success">
        Use the buttons above or the left sidebar to open each workflow page.
    </div>
    """,
    unsafe_allow_html=True
)
