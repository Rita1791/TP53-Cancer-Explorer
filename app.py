import os
import streamlit as st
import pandas as pd

# ------------- BASIC APP SETUP ------------- #

# Clinical + AI style: clean, wide layout
st.set_page_config(
    page_title="TP53 Cancer Resistance Explorer",
    layout="wide"
)

st.title("🧬 TP53 Cancer Resistance Explorer")
st.markdown("""
This app lets you explore **human and elephant TP53 genes** and understand  
how multiple TP53-like copies in elephants may contribute to **cancer resistance**.
""")

# ------------- LOAD DATA ------------- #

@st.cache_data
def load_features():
    # Try both possible filenames
    for fname in [
        "data/tp53_features_with_similarity_clustered.csv",
        "data/tp53_features_with_similarity.csv"
    ]:
        if os.path.exists(fname):
            df = pd.read_csv(fname)
            return df, fname
    return None, None

features_df, features_file = load_features()

if features_df is None:
    st.error("❌ Could not find features file in 'data/' folder.\n"
             "Please make sure your CSV is named:\n"
             "- tp53_features_with_similarity.csv OR\n"
             "- tp53_features_with_similarity_clustered.csv")
    st.stop()

st.sidebar.success(f"Loaded features from: {features_file}")

# Check what columns exist
has_cluster = "cluster" in features_df.columns

# ------------- SIDEBAR NAVIGATION ------------- #

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "TP53 Database", "Explore a Sequence", "About"]
)

# ------------- PAGE: OVERVIEW ------------- #
if page == "Overview":
    st.header("🔬 Overview of Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Phylogenetic Tree")
        tree_path = "images/TP53_tree.png"
        if os.path.exists(tree_path):
            st.image(tree_path, caption="Figure 1. Phylogenetic tree of TP53 and retrogenes.")
        else:
            st.warning("Tree image not found. Put 'TP53_tree.png' in the images folder.")

    with col2:
        st.subheader("MSA Conservation Logo")
        logo_path = "images/TP53_MSA_logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, caption="Figure 2. TP53 multiple sequence alignment logo.")
        else:
            st.warning("Logo image not found. Put 'TP53_MSA_logo.png' in the images folder.")

    st.markdown("---")
    st.subheader("Identity to Human TP53")
    barplot_path = "images/identity_barplot.png"
    if os.path.exists(barplot_path):
        st.image(barplot_path, caption="Figure 3. Top TP53/RTG sequences by % identity to human TP53.")
    else:
        st.warning("Barplot image not found. Put 'identity_barplot.png' in the images folder.")

    st.markdown("""
On this page you can see the **evolutionary tree**, **conservation pattern**,  
and overall **similarity** of elephant TP53-like genes to human TP53.
    """)

# ------------- PAGE: TP53 DATABASE ------------- #
elif page == "TP53 Database":
    st.header("📊 TP53 Feature Table")

    st.write("""
This table shows all TP53 and TP53-like sequences used in your analysis,
along with their **length**, **composition features**, and **similarity to human TP53**.
You can sort and filter the table using the options below.
    """)

    # Show only some important columns by default
    main_cols = ["id", "length", "identity_to_human"]
    cols_to_show = [c for c in main_cols if c in features_df.columns]

    if has_cluster:
        cols_to_show.append("cluster")

    st.dataframe(features_df[cols_to_show].sort_values("identity_to_human", ascending=False))

    st.markdown("""
**Tip for Viva / Thesis:**  
You can explain that sequences with higher `% identity_to_human` are more likely to preserve  
tumor-suppressor functions similar to human TP53.
    """)

# ------------- PAGE: EXPLORE A SEQUENCE ------------- #
elif page == "Explore a Sequence":
    st.header("🔍 Explore a Single TP53 / RTG Sequence")

    st.write("""
Choose a sequence ID from the dropdown below to see its properties and how  
similar it is to human TP53.
    """)

    seq_ids = features_df["id"].tolist()
    selected_id = st.selectbox("Select sequence ID", seq_ids)

    # Get that row
    row = features_df[features_df["id"] == selected_id].iloc[0]

    st.subheader(f"Details for: `{selected_id}`")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Basic properties:**")
        st.write(f"- Length: `{row['length']}` amino acids")
        if "identity_to_human" in row:
            st.write(f"- Identity to human TP53: `{row['identity_to_human']:.2f}%`")
        if has_cluster:
            st.write(f"- Cluster (AI group): `{row['cluster']}`")

    with col2:
        st.write("**Amino acid composition (fraction):**")
        aa_cols = [c for c in features_df.columns if c.startswith("frac_")]
        comp_df = row[aa_cols].to_frame(name="Fraction").reset_index()
        comp_df["Amino Acid"] = comp_df["index"].str.replace("frac_", "")
        comp_df = comp_df[["Amino Acid", "Fraction"]]
        st.dataframe(comp_df)

    st.markdown("""
You can explain in your thesis that sequences with:
- **High similarity** and **balanced composition** may be **functional TP53 paralogs**
- **Lower similarity** may represent **more diverged retrogenes**
    """)

# ------------- PAGE: ABOUT ------------- #
elif page == "About":
    st.header("ℹ️ About This App")

    st.markdown("""
**Project:** AI-Driven Comparative Analysis of TP53 Paralogs in Elephants and Humans  
**Student:** *Ritika Rawat*  
**Program:** M.Sc. Bioinformatics, Mumbai University  

This application is a user-friendly interface built on top of a full  
bioinformatics and AI pipeline that:

- Collected TP53-like sequences from **NCBI / UniProt**
- Performed **BLAST**, **Multiple Sequence Alignment**, and **Phylogenetic Analysis**
- Extracted **sequence features** and **similarity to human TP53**
- Used simple **AI clustering** to group sequences into similarity-based categories

The goal is to help explain how **multiple TP53 retrogenes in elephants**
may contribute to their **remarkable resistance to cancer** (Peto's Paradox).
    """)

    st.markdown("---")
    st.markdown("Built with **Python** and **Streamlit** — modern tools widely used in data science and bioinformatics.")
