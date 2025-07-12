import streamlit as st
import pandas as pd

st.set_page_config(page_title="Apex Accounts", layout="wide")
st.title("Apex Accounts")

# --- Helper Functions ---
def normalize_name(name):
    return str(name).strip().lower()

def normalize_designation(value):
    val = str(value).strip().lower()
    if val in ["p", "primary"]:
        return "primary"
    elif val in ["s", "contingent"]:
        return "contingent"
    return val

def normalize_visibility_status(value):
    val = str(value).strip().lower()
    return "deleted" if val == "true" else "active"

def normalize_bd_visibility_status(value):
    val = str(value).strip().lower()
    return "deleted" if val == "inactive" else "active"

def get_name_key(row):
    raw_designation = row.get("designation", "").strip()
    designation = normalize_designation(raw_designation)

    first_name_raw = row.get("first_name", None)
    last_name_raw = row.get("last_name", None)

    first_missing = pd.isna(first_name_raw) or str(first_name_raw).strip() == ""
    last_missing = pd.isna(last_name_raw) or str(last_name_raw).strip() == ""

    if first_missing and last_missing:
        entity_name = normalize_name(row.get("entity_name", ""))
        return (designation, entity_name, "entity")

    first_name = normalize_name(first_name_raw)
    last_name = normalize_name(last_name_raw)
    full_name = f"{first_name} {last_name}".strip()
    return (designation, full_name, "individual")

def group_beneficiaries(df):
    grouped = {}
    for _, row in df.iterrows():
        acct = str(row.get("account_number")).strip()
        key = get_name_key(row)
        if acct not in grouped:
            grouped[acct] = set()
        grouped[acct].add(key)
    return grouped

# --- Upload Files ---
bd_file = st.file_uploader("Upload BD_Bene.csv", type="csv")
ac_file = st.file_uploader("Upload AC_Bene.csv", type="csv")

if bd_file and ac_file:
    bd_df = pd.read_csv(bd_file)
    ac_df = pd.read_csv(ac_file)
    bd_df.columns = bd_df.columns.str.lower().str.strip()
    ac_df.columns = ac_df.columns.str.lower().str.strip()

    bd_df["visibility_status"] = bd_df["status"].fillna("").astype(str).apply(normalize_bd_visibility_status)
    ac_df["visibility_status"] = ac_df["deleted"].fillna("").astype(str).apply(normalize_visibility_status)

    bd_active_df = bd_df[bd_df["visibility_status"] == "active"]
    ac_active_df = ac_df[ac_df["visibility_status"] == "active"]

    grouped_bd = group_beneficiaries(bd_active_df)
    grouped_ac = group_beneficiaries(ac_active_df)

    # --- 3AA Accounts Logic ---
    three_aa_accounts = {
        acct for acct in set(grouped_bd.keys()).union(set(grouped_ac.keys()))
        if acct.startswith("3AA")
    }

    three_aa_entries = []
    for acct in three_aa_accounts:
        bd_active_keys = grouped_bd.get(acct, set())
        ac_active_keys = grouped_ac.get(acct, set())

        mismatch = bd_active_keys != ac_active_keys

        three_aa_entries.append({
            "account_number": acct,
            "bd_benes": list(bd_active_keys) if bd_active_keys else None,
            "ac_benes": list(ac_active_keys) if ac_active_keys else None,
            "match_status": "Mismatch" if mismatch else "Match"
        })

    three_aa_df = pd.DataFrame(three_aa_entries)

    # Display only 3AA tab
    tab = st.tabs(["3AA Accounts"])[0]
    with tab:
        st.subheader("3AA Accounts (Across BD and AC)")
        st.dataframe(three_aa_df, use_container_width=True)
        st.download_button(
            label="Download 3AA Accounts",
            data=three_aa_df.to_csv(index=False),
            file_name="3aa_accounts.csv",
            mime="text/csv"
        )
