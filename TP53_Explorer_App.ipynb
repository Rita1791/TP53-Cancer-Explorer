!pip install gradio biopython

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from Bio import SeqIO
import os

BASE = "/content/drive/MyDrive/elephant-p53-project"

features_path = os.path.join(BASE, "results", "ML", "tp53_features_with_similarity.csv")
clean_fasta_path = os.path.join(BASE, "data", "processed", "TP53_clean.fasta")

# Load features table
df = pd.read_csv(features_path)

print("Columns:", df.columns.tolist())
print("Total sequences:", len(df))

# Load sequences into a dictionary
seq_dict = {rec.id: str(rec.seq) for rec in SeqIO.parse(clean_fasta_path, "fasta")}
print("Sequences loaded:", len(seq_dict))

# Optional: define a cluster label if you added cluster column later
if "cluster" in df.columns:
    def cluster_label(c):
        if c == 0:
            return "Cluster 0 (High TP53-like, AI)"
        elif c == 1:
            return "Cluster 1 (Intermediate)"
        else:
            return "Cluster 2 (Divergent)"
else:
    cluster_label = None

msa_logo_path = os.path.join(BASE, "results", "msa", "TP53_MSA_logo.png")
tree_path = os.path.join(BASE, "results", "phylogeny", "TP53_tree.png")
barplot_path = os.path.join(BASE, "results", "ML", "identity_barplot.png")

print("MSA logo exists:", os.path.exists(msa_logo_path))
print("Tree exists:", os.path.exists(tree_path))
print("Barplot exists:", os.path.exists(barplot_path))

import gradio as gr

def explain_sequence(seq_id):
    """
    Given a sequence ID, return a human-readable explanation
    and show global figures (tree, logo, barplot).
    """
    row = df[df["id"] == seq_id]
    if row.empty:
        summary = "Sequence not found in feature table."
        return summary, tree_path, msa_logo_path, barplot_path

    row = row.iloc[0]
    length = row["length"] if "length" in row else None
    identity = row["identity_to_human"] if "identity_to_human" in row else None
    gc_like = row["GC_like"] if "GC_like" in row else None

    # Build plain-English description
    summary_lines = []
    summary_lines.append(f"**Sequence ID:** `{seq_id}`")

    if length is not None:
        summary_lines.append(f"- Length: **{int(length)} amino acids**")
    if identity is not None:
        summary_lines.append(f"- Identity to human TP53: **{identity:.2f}%**")
    if gc_like is not None:
        summary_lines.append(f"- GC-like count (G+C): **{int(gc_like)}**")

    # Cluster label if available
    if "cluster" in df.columns and cluster_label is not None:
        c = int(row["cluster"])
        summary_lines.append(f"- AI Cluster: **{cluster_label(c)}**")

    # Very simple biological interpretation
    if identity is not None:
        if identity >= 80:
            summary_lines.append("> Interpretation: This sequence is **highly similar** to human TP53 and may preserve strong tumor-suppressor function.")
        elif identity >= 50:
            summary_lines.append("> Interpretation: This sequence is **moderately similar** to human TP53 and may have **partial** or **diverged** function.")
        else:
            summary_lines.append("> Interpretation: This sequence is **distant** from human TP53 and is more likely a **diverged retrogene**.")

    summary = "\n".join(summary_lines)

    # Return: text + images
    return summary, tree_path, msa_logo_path, barplot_path

# Choices for dropdown = all sequence IDs from features table
id_choices = df["id"].tolist()

# Clinical + AI feel: light theme, clean layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 TP53 Cancer Resistance Explorer")
    gr.Markdown("**Mumbai University – MSc Bioinformatics**  \nExplore human, Asian, and African elephant TP53 paralogs and their similarity to human TP53.")

    with gr.Row():
        with gr.Column(scale=1):
            seq_dropdown = gr.Dropdown(choices=id_choices, label="Choose a TP53 / RTG sequence ID")
            run_button = gr.Button("Analyze Sequence 🔍")
        with gr.Column(scale=2):
            summary_out = gr.Markdown(label="Sequence Interpretation")

    gr.Markdown("### 🌳 Phylogeny and Conservation")
    with gr.Row():
        tree_img = gr.Image(label="Phylogenetic Tree (Human vs Elephants)")
        logo_img = gr.Image(label="MSA Conservation (TP53 domains)")

    gr.Markdown("### 📊 AI Similarity Results")
    barplot_img = gr.Image(label="Top TP53 candidates by identity to human")

    def on_click(seq_id):
        return explain_sequence(seq_id)

    run_button.click(
        fn=on_click,
        inputs=seq_dropdown,
        outputs=[summary_out, tree_img, logo_img, barplot_img]
    )

demo.launch(share=True)
