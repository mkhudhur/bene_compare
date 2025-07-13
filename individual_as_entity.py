import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sync Status Checker", layout="wide")
st.title("🔍 Failed Sync Status Checker")

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

    st.write("BD Columns:", list(bd_df.columns))
    st.write("AC Columns:", list(ac_df.columns))

    bd_df["visibility_status"] = bd_df["status"].fillna("").astype(str).apply(normalize_bd_visibility_status)
    ac_df["visibility_status"] = ac_df["deleted"].fillna("").astype(str).apply(normalize_visibility_status)

    bd_active_df = bd_df[bd_df["visibility_status"] == "active"]
    ac_active_df = ac_df[ac_df["visibility_status"] == "active"]

    grouped_bd = group_beneficiaries(bd_active_df)
    grouped_ac = group_beneficiaries(ac_active_df)

    if "sync_state" in bd_active_df.columns:
        failed_sync_df = bd_active_df[bd_active_df["sync_state"].str.lower().str.strip() == "failed"]

        results = []
        name_mismatch_count = 0
        individual_as_entity_count = 0

        for acct in failed_sync_df["account_number"].unique():
            subset = failed_sync_df[failed_sync_df["account_number"] == acct]
            bd_benes = grouped_bd.get(acct, set())
            ac_benes = grouped_ac.get(acct, set())

            # Check for individual-as-entity mismatch (name-sensitive)
            ac_entity_names = {b[1] for b in ac_benes if b[-1] == "entity"}
            bd_individual_names = {b[1] for b in bd_benes if b[-1] == "individual"}
            individual_as_entity = not ac_entity_names.isdisjoint(bd_individual_names)
            if individual_as_entity:
                individual_as_entity_count += 1

            name_mismatch = bd_benes != ac_benes
            if name_mismatch:
                name_mismatch_count += 1

            sync_origin = "BD failed"

            # Allocation checks
            bd_primary_total = bd_active_df[
                (bd_active_df["account_number"] == acct) &
                (bd_active_df["designation"].str.lower().str.strip().isin(["p", "primary"]))
            ]["percentage"].astype(float).sum()

            ac_primary_total = ac_active_df[
                (ac_active_df["account_number"] == acct) &
                (ac_active_df["designation"].str.lower().str.strip().isin(["p", "primary"]))
            ]["percentage"].astype(float).sum()

            bd_contingent_total = bd_active_df[
                (bd_active_df["account_number"] == acct) &
                (bd_active_df["designation"].str.lower().str.strip().isin(["s", "contingent"]))
            ]["percentage"].astype(float).sum()

            ac_contingent_total = ac_active_df[
                (ac_active_df["account_number"] == acct) &
                (ac_active_df["designation"].str.lower().str.strip().isin(["s", "contingent"]))
            ]["percentage"].astype(float).sum()

            primary_allocation_match = bd_primary_total == ac_primary_total
            contingent_allocation_match = bd_contingent_total == ac_contingent_total

            # Last updated timestamp and updated by (BD vs AC)
            bd_subset = bd_df[bd_df["account_number"] == acct].copy()
            ac_subset = ac_df[ac_df["account_number"] == acct].copy()

            bd_subset["updated"] = pd.to_datetime(bd_subset["updated"], errors="coerce")
            ac_subset["updated"] = pd.to_datetime(ac_subset["updated"], errors="coerce")

            bd_latest = bd_subset.sort_values("updated", ascending=False).head(1)
            ac_latest = ac_subset.sort_values("updated", ascending=False).head(1)

            bd_time = bd_latest["updated"].values[0] if not bd_latest.empty else pd.NaT
            ac_time = ac_latest["updated"].values[0] if not ac_latest.empty else pd.NaT

            if pd.isna(bd_time) and pd.isna(ac_time):
                last_updated = None
                updated_by = None
            elif pd.isna(ac_time) or (not pd.isna(bd_time) and bd_time > ac_time):
                last_updated = bd_latest["updated"].dt.strftime("%Y-%m-%d %H:%M:%S").values[0]
                updated_by = bd_latest["updated_by"].values[0] if "updated_by" in bd_latest.columns else None
                last_updated += " (BD)"
            else:
                last_updated = ac_latest["updated"].dt.strftime("%Y-%m-%d %H:%M:%S").values[0]
                updated_by = ac_latest["updated_by"].values[0] if "updated_by" in ac_latest.columns else None
                last_updated += " (AC)"

            results.append({
                "account_number": acct,
                "account_status": subset["status"].iloc[0] if not subset["status"].isna().all() else None,
                "bd_benes": list(bd_benes) if bd_benes else None,
                "ac_benes": list(ac_benes) if ac_benes else None,
                "sync_state": sync_origin,
                "name_mismatch": name_mismatch,
                "primary_allocation_match": primary_allocation_match,
                "contingent_allocation_match": contingent_allocation_match,
                "last_updated": last_updated,
                "updated_by": updated_by,
                "individual_as_entity": individual_as_entity
            })

        failed_df = pd.DataFrame(results)

        tab = st.tabs(["Failed Sync Status Accounts"])[0]
        with tab:
            st.subheader(f"Accounts with Failed Sync Status (Name Mismatches: {name_mismatch_count}, Individual-As-Entity: {individual_as_entity_count})")
            st.dataframe(failed_df, use_container_width=True)
            st.download_button(
                label="Download Failed Sync Accounts",
                data=failed_df.to_csv(index=False),
                file_name="failed_sync_accounts.csv",
                mime="text/csv"
            )
    else:
        st.warning("The 'sync_state' column was not found in the uploaded BD file.")
