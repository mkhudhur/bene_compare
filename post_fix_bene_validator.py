import streamlit as st
import pandas as pd

st.set_page_config(page_title="Post-Fix Bene Validator", layout="wide")
st.title("✅ Post-Fix Beneficiary Matching Checker")

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

def normalize_bd_visibility_status(status):
    return "deleted" if str(status).strip().lower() == "inactive" else "active"

def normalize_visibility_status(value):
    return "deleted" if str(value).strip().lower() == "true" else "active"

def get_name_key(row):
    designation = normalize_designation(row.get("designation", ""))
    first = normalize_name(row.get("first_name", ""))
    last = normalize_name(row.get("last_name", ""))
    entity_name = normalize_name(row.get("entity_name", ""))

    if not first and not last and entity_name:
        return (designation, entity_name, "entity")

    full_name = f"{first} {last}".strip()
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

# --- File Uploads ---
bd_file = st.file_uploader("Upload BD_Bene.csv", type="csv")
ac_file = st.file_uploader("Upload AC_Bene.csv", type="csv")
fixed_file = st.file_uploader("Upload Fixed Account List (CSV with 'account_number' column)", type="csv")

if bd_file and ac_file and fixed_file:
    bd_df = pd.read_csv(bd_file)
    ac_df = pd.read_csv(ac_file)
    fixed_df = pd.read_csv(fixed_file)

    bd_df.columns = bd_df.columns.str.lower().str.strip()
    ac_df.columns = ac_df.columns.str.lower().str.strip()
    fixed_df.columns = fixed_df.columns.str.lower().str.strip()

    bd_df["visibility_status"] = bd_df["status"].fillna("").astype(str).apply(normalize_bd_visibility_status)
    ac_df["visibility_status"] = ac_df["deleted"].fillna("").astype(str).apply(normalize_visibility_status)

    bd_active = bd_df[bd_df["visibility_status"] == "active"]
    ac_active = ac_df[ac_df["visibility_status"] == "active"]
    bd_deleted = bd_df[bd_df["visibility_status"] == "deleted"]
    ac_deleted = ac_df[ac_df["visibility_status"] == "deleted"]

    bd_grouped = group_beneficiaries(bd_active)
    ac_grouped = group_beneficiaries(ac_active)
    bd_deleted_grouped = group_beneficiaries(bd_deleted)
    ac_deleted_grouped = group_beneficiaries(ac_deleted)

    fixed_accounts = fixed_df["account_number"].astype(str).str.strip()

    results = []
    for acct in fixed_accounts:
        bd_keys = bd_grouped.get(acct, set())

        # Determine account status from AC sheet
        ac_subset = ac_df[ac_df["account_number"] == acct]
        if not ac_subset.empty:
            restricted_flag = ac_subset["restricted"].astype(str).str.lower() == "true"
            closed_flag = ac_subset["closed"].astype(str).str.lower() == "true"
            if closed_flag.any():
                account_status = "Closed"
            elif restricted_flag.any():
                account_status = "Restricted"
            else:
                account_status = "Active"
        else:
            account_status = None

        ac_keys = ac_grouped.get(acct, set())
        bd_deleted_keys = bd_deleted_grouped.get(acct, set())
        ac_deleted_keys = ac_deleted_grouped.get(acct, set())
        match = bd_keys == ac_keys

        results.append({
            "account_number": acct,
            "account_status": account_status,
            "bd_benes": list(bd_keys) if bd_keys else None,
            "ac_benes": list(ac_keys) if ac_keys else None,
            "bd_deleted_benes": list(bd_deleted_keys) if bd_deleted_keys else None,
            "ac_deleted_benes": list(ac_deleted_keys) if ac_deleted_keys else None,
            "match_status": "Match" if match else "Mismatch"
        })

    result_df = pd.DataFrame(results)

    # --- Summary ---
    total_accounts = len(result_df)
    num_matches = (result_df["match_status"] == "Match").sum()
    percent_success = round((num_matches / total_accounts) * 100, 1) if total_accounts > 0 else 0

    st.markdown("### ✅ Summary")
    st.markdown(f"- Total accounts reviewed: **{total_accounts}**")
    st.markdown(f"- Total fixed accounts: **{num_matches}** ({percent_success}%)")

    st.dataframe(result_df, use_container_width=True)

    st.download_button(
        label="Download Results",
        data=result_df.to_csv(index=False),
        file_name="post_fix_bene_check.csv",
        mime="text/csv"
    )
