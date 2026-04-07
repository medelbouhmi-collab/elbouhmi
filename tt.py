import streamlit as st
import pandas as pd
import difflib

st.title("📊 Correcteur de modules basé sur fichier de référence")

# -----------------------
# Upload fichiers
# -----------------------
ref_file = st.file_uploader("📥 Fichier de référence", type=["xlsx"])
file_to_correct = st.file_uploader("📥 Fichier à corriger", type=["xlsx"])


# -----------------------
# Fonction de correction
# -----------------------
def corriger_module(module, reference_list):
   module_clean = str(module).capitalize()
    suggestions = difflib.get_close_matches(
        module_clean,
        reference_list,
        n=1,
        cutoff=0.6
    )

    if suggestions:
        return suggestions[0]

    return module


# -----------------------
# Traitement
# -----------------------
if ref_file and file_to_correct:

    # Lecture Excel
    df_ref = pd.read_excel(ref_file)
    df_corr = pd.read_excel(file_to_correct)

    st.subheader("Aperçu fichier référence")
    st.dataframe(df_ref.head())

    st.subheader("Aperçu fichier à corriger")
    st.dataframe(df_corr.head())

    if st.button("🔧 Corriger les modules"):

        # Liste de référence
        reference_list = df_ref["Module"].dropna().astype(str).str.lower().tolist()

        # Correction
        df_corr["Module_corrige"] = df_corr["Module"].apply(
            lambda x: corriger_module(x, reference_list)
        )

        st.subheader("✅ Résultat corrigé")
        st.dataframe(df_corr)

        # -----------------------
        # Export Excel
        # -----------------------
        from io import BytesIO

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output.seek(0)
            return output

        excel_data = to_excel(df_corr)

        st.download_button(
            label="📥 Télécharger le fichier corrigé",
            data=excel_data,
            file_name="modules_corriges.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
