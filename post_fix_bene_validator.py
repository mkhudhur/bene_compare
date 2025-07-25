import streamlit as st
import pandas as pd

st.set_page_config(page_title="Post-Fix Bene Validator", layout="wide")
st.title("✅ Post-Fix Beneficiary Matching Checker")

# --- Helper Functions ---
def normalize_name(name):
    return str(name).strip().lower()

def normalize_designation(value):
    """Normalize designation values with better handling of AC formats"""
    if pd.isna(value) or value == "":
        return "unknown"
    
    val = str(value).strip().lower()
    
    # Handle BD formats
    if val in ["primary"]:
        return "primary"
    elif val in ["contingent"]:
        return "contingent"
    
    # Handle AC formats (including potential variations)
    elif val in ["p", "pri", "prim"]:
        return "primary"
    elif val in ["s", "sec", "secondary", "c", "cont"]:
        return "contingent"
    
    # If no mapping found, return the original value for debugging
    return val

def normalize_designation_type(value):
    """Normalize designation types (per capita/per stirpes)"""
    val = str(value).strip().lower().replace(' ', '').replace('_', '')
    if val in ["percapita", "pc"]:
        return "per_capita"
    elif val in ["perstirpes", "ps"]:
        return "per_stirpes"
    return val

def normalize_bd_visibility_status(status):
    return "deleted" if str(status).strip().lower() == "inactive" else "active"

def normalize_visibility_status(value):
    return "deleted" if str(value).strip().lower() == "true" else "active"

def get_beneficiary_key(row, is_bd=True):
    """Create comprehensive beneficiary key including designation, name, type, and percentage"""
    designation_raw = row.get("designation", "")
    designation = normalize_designation(designation_raw)
    designation_type = normalize_designation_type(row.get("designation_type", ""))
    percentage = round(float(row.get("percentage", 0)), 2)
    
    # Debug specific problematic accounts
    account_num = str(row.get("account_number", ""))
    if account_num in ["3AA29133", "3AA35013"]:
        print(f"DEBUG - Account {account_num}: raw_designation='{designation_raw}', normalized='{designation}', is_bd={is_bd}")
    
    # Handle name normalization based on BD vs AC logic
    if is_bd:
        # BD logic: entity vs individual
        relationship = str(row.get("relationship", "")).strip().lower()
        if relationship == "entity":
            name = normalize_name(row.get("entity_name", ""))
            relationship_type = "entity"
        else:
            first = normalize_name(row.get("first_name", ""))
            last = normalize_name(row.get("last_name", ""))
            name = f"{first} {last}".strip()
            relationship_type = "individual"
    else:
        # AC logic: entity, spouse/non-spouse, or individual
        relationship = str(row.get("relationship", "")).strip().lower()
        first = normalize_name(row.get("first_name", ""))
        last = normalize_name(row.get("last_name", ""))
        entity_name = normalize_name(row.get("entity_name", ""))
        
        if relationship == "entity":
            name = entity_name or normalize_name(row.get("name", ""))
            relationship_type = "entity"
        elif relationship in ["spouse", "non-spouse"] and (not first or not last) and entity_name:
            name = entity_name
            relationship_type = "individual"  # Treat spouse/non-spouse as individual for matching
        else:
            name = f"{first} {last}".strip()
            relationship_type = "individual"

    return (designation, name, relationship_type, designation_type, percentage)

def analyze_beneficiaries(df, is_bd=True):
    """Group beneficiaries by account and analyze by designation"""
    grouped = {}
    for _, row in df.iterrows():
        acct = str(row.get("account_number")).strip()
        key = get_beneficiary_key(row, is_bd=is_bd)
        
        if acct not in grouped:
            grouped[acct] = {
                'all_keys': set(),
                'primary': set(),
                'contingent': set(),
                'primary_allocation': 0,
                'contingent_allocation': 0
            }
        
        grouped[acct]['all_keys'].add(key)
        
        designation, name, rel_type, des_type, percentage = key
        if designation == "primary":
            grouped[acct]['primary'].add(key)
            grouped[acct]['primary_allocation'] += percentage
        elif designation == "contingent":
            grouped[acct]['contingent'].add(key)
            grouped[acct]['contingent_allocation'] += percentage
    
    # Round allocations to avoid floating point issues
    for acct_data in grouped.values():
        acct_data['primary_allocation'] = round(acct_data['primary_allocation'], 2)
        acct_data['contingent_allocation'] = round(acct_data['contingent_allocation'], 2)
    
    return grouped

def format_beneficiary_display(bene_set):
    """Format beneficiary set for display"""
    if not bene_set:
        return "None"
    
    formatted = []
    for designation, name, rel_type, des_type, percentage in sorted(bene_set):
        rel_prefix = "[Entity] " if rel_type == "entity" else ""
        formatted.append(f"{designation.title()}: {rel_prefix}{name.title()} ({percentage}%, {des_type})")
    
    return " | ".join(formatted)

def analyze_mismatches(bd_data, ac_data):
    """Analyze specific types of mismatches"""
    mismatches = []
    
    # Primary beneficiary name mismatches
    bd_primary_names = {(name, rel_type) for _, name, rel_type, _, _ in bd_data['primary']}
    ac_primary_names = {(name, rel_type) for _, name, rel_type, _, _ in ac_data['primary']}
    if bd_primary_names != ac_primary_names:
        mismatches.append("Primary Names Mismatch")
    
    # Contingent beneficiary name mismatches
    bd_contingent_names = {(name, rel_type) for _, name, rel_type, _, _ in bd_data['contingent']}
    ac_contingent_names = {(name, rel_type) for _, name, rel_type, _, _ in ac_data['contingent']}
    if bd_contingent_names != ac_contingent_names:
        mismatches.append("Contingent Names Mismatch")
    
    # Primary designation type mismatches
    bd_primary_types = {des_type for _, _, _, des_type, _ in bd_data['primary']}
    ac_primary_types = {des_type for _, _, _, des_type, _ in ac_data['primary']}
    if bd_primary_types != ac_primary_types:
        mismatches.append("Primary Designation Type Mismatch")
    
    # Contingent designation type mismatches
    bd_contingent_types = {des_type for _, _, _, des_type, _ in bd_data['contingent']}
    ac_contingent_types = {des_type for _, _, _, des_type, _ in ac_data['contingent']}
    if bd_contingent_types != ac_contingent_types:
        mismatches.append("Contingent Designation Type Mismatch")
    
    # Primary allocation mismatches
    if bd_data['primary_allocation'] != ac_data['primary_allocation']:
        mismatches.append("Primary Allocation Mismatch")
    
    # Contingent allocation mismatches
    if bd_data['contingent_allocation'] != ac_data['contingent_allocation']:
        mismatches.append("Contingent Allocation Mismatch")
    
    # Allocation validation (should be 100% when beneficiaries exist)
    if bd_data['primary'] and bd_data['primary_allocation'] != 100.0:
        mismatches.append("BD Primary ≠ 100%")
    if ac_data['primary'] and ac_data['primary_allocation'] != 100.0:
        mismatches.append("AC Primary ≠ 100%")
    if bd_data['contingent'] and bd_data['contingent_allocation'] != 100.0:
        mismatches.append("BD Contingent ≠ 100%")
    if ac_data['contingent'] and ac_data['contingent_allocation'] != 100.0:
        mismatches.append("AC Contingent ≠ 100%")
    
    return mismatches

# --- File Uploads ---
st.subheader("📁 Upload Files")
col1, col2, col3 = st.columns(3)

with col1:
    bd_file = st.file_uploader("Upload BD_Bene.csv", type="csv")
with col2:
    ac_file = st.file_uploader("Upload AC_Bene.csv", type="csv")
with col3:
    fixed_file = st.file_uploader("Upload Fixed Account List (CSV with 'account_number' column)", type="csv")

if bd_file and ac_file and fixed_file:
    # Load data
    with st.spinner("Loading and analyzing data..."):
        bd_df = pd.read_csv(bd_file)
        ac_df = pd.read_csv(ac_file)
        fixed_df = pd.read_csv(fixed_file)

        bd_df.columns = bd_df.columns.str.lower().str.strip()
        ac_df.columns = ac_df.columns.str.lower().str.strip()
        fixed_df.columns = fixed_df.columns.str.lower().str.strip()

        # Normalize visibility status
        bd_df["visibility_status"] = bd_df["status"].fillna("").astype(str).apply(normalize_bd_visibility_status)
        ac_df["visibility_status"] = ac_df["deleted"].fillna("").astype(str).apply(normalize_visibility_status)

        # Only process active beneficiaries
        bd_active = bd_df[bd_df["visibility_status"] == "active"]
        ac_active = ac_df[ac_df["visibility_status"] == "active"]

        # Analyze beneficiaries with proper BD vs AC normalization
        bd_grouped = analyze_beneficiaries(bd_active, is_bd=True)
        ac_grouped = analyze_beneficiaries(ac_active, is_bd=False)

        fixed_accounts = fixed_df["account_number"].astype(str).str.strip()

    # Process each fixed account
    results = []
    for acct in fixed_accounts:
        bd_data = bd_grouped.get(acct, {
            'all_keys': set(), 'primary': set(), 'contingent': set(),
            'primary_allocation': 0, 'contingent_allocation': 0
        })
        ac_data = ac_grouped.get(acct, {
            'all_keys': set(), 'primary': set(), 'contingent': set(),
            'primary_allocation': 0, 'contingent_allocation': 0
        })

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
            account_status = "Unknown"

        # Check for perfect match
        perfect_match = bd_data['all_keys'] == ac_data['all_keys']
        
        # Analyze specific mismatches
        if not perfect_match:
            mismatches = analyze_mismatches(bd_data, ac_data)
            mismatch_details = " | ".join(mismatches) if mismatches else "Unknown Mismatch"
        else:
            mismatch_details = "Perfect Match"

        results.append({
            "account_number": acct,
            "account_status": account_status,
            "bd_beneficiaries": format_beneficiary_display(bd_data['all_keys']),
            "ac_beneficiaries": format_beneficiary_display(ac_data['all_keys']),
            "bd_primary_allocation": f"{bd_data['primary_allocation']}%" if bd_data['primary'] else "N/A",
            "ac_primary_allocation": f"{ac_data['primary_allocation']}%" if ac_data['primary'] else "N/A",
            "bd_contingent_allocation": f"{bd_data['contingent_allocation']}%" if bd_data['contingent'] else "N/A",
            "ac_contingent_allocation": f"{ac_data['contingent_allocation']}%" if ac_data['contingent'] else "N/A",
            "match_status": "✅ Match" if perfect_match else "❌ Mismatch",
            "mismatch_details": mismatch_details
        })

    result_df = pd.DataFrame(results)

    # --- Summary ---
    st.subheader("📊 Validation Summary")
    
    total_accounts = len(result_df)
    num_matches = (result_df["match_status"] == "✅ Match").sum()
    num_mismatches = total_accounts - num_matches
    percent_success = round((num_matches / total_accounts) * 100, 1) if total_accounts > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Accounts", f"{total_accounts:,}")
    with col2:
        st.metric("Fixed Successfully", f"{num_matches:,}", delta=f"{percent_success}%")
    with col3:
        st.metric("Still Have Issues", f"{num_mismatches:,}")
    with col4:
        st.metric("Success Rate", f"{percent_success}%")

    # Show mismatch breakdown
    if num_mismatches > 0:
        st.subheader("🔍 Remaining Issues Breakdown")
        
        # Flatten mismatch details for analysis
        all_mismatches = []
        for details in result_df[result_df["match_status"] == "❌ Mismatch"]["mismatch_details"]:
            if details != "Perfect Match" and details != "Unknown Mismatch":
                all_mismatches.extend(details.split(" | "))
        
        if all_mismatches:
            mismatch_counts = pd.Series(all_mismatches).value_counts()
            st.bar_chart(mismatch_counts)
            
            st.write("**Most Common Remaining Issues:**")
            for i, (issue, count) in enumerate(mismatch_counts.head(5).items(), 1):
                st.write(f"{i}. **{issue}**: {count} accounts ({count/total_accounts*100:.1f}%)")

    # Display detailed results
    st.subheader("📋 Detailed Validation Results")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_only_mismatches = st.checkbox("Show Only Mismatched Accounts", value=False)
    with col2:
        sort_by_issues = st.checkbox("Sort by Issue Count", value=True)

    display_df = result_df.copy()
    if show_only_mismatches:
        display_df = display_df[display_df["match_status"] == "❌ Mismatch"]

    if sort_by_issues:
        # Sort mismatches first, then by number of issues
        display_df["issue_count"] = display_df["mismatch_details"].apply(
            lambda x: len(x.split(" | ")) if x not in ["Perfect Match", "Unknown Mismatch"] else 0
        )
        display_df = display_df.sort_values(["match_status", "issue_count"], ascending=[True, False])
        display_df = display_df.drop("issue_count", axis=1)

    st.dataframe(display_df, use_container_width=True)

    # Download options
    st.subheader("📥 Download Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📊 Download All Results",
            data=result_df.to_csv(index=False),
            file_name="post_fix_validation_all_results.csv",
            mime="text/csv"
        )
    
    with col2:
        if num_mismatches > 0:
            mismatched_df = result_df[result_df["match_status"] == "❌ Mismatch"]
            st.download_button(
                label="🚨 Download Still-Broken Accounts",
                data=mismatched_df.to_csv(index=False),
                file_name="post_fix_validation_still_broken.csv",
                mime="text/csv"
            )
        else:
            st.success("🎉 All accounts are fixed!")

else:
    st.info("👆 Please upload all three CSV files to begin validation.")
    
    st.markdown("""
    ### How to Use This Tool:
    
    1. **Upload BD_Bene.csv** - Your BD beneficiary data
    2. **Upload AC_Bene.csv** - Your AC beneficiary data  
    3. **Upload Fixed Account List** - CSV with account numbers you've attempted to fix
    
    The tool will validate each account and show:
    - ✅ **Perfect matches** (completely fixed)
    - ❌ **Remaining mismatches** with specific issue details
    - 📊 **Success rate** and breakdown of remaining issues
    - 📥 **Downloadable results** for further analysis
    
    ### What Gets Validated:
    - **Beneficiary names** (including entity vs individual handling)
    - **Designations** (primary vs contingent)
    - **Designation types** (per capita vs per stirpes)  
    - **Allocation percentages** (should be 100% per designation)
    - **Comprehensive matching** across all beneficiary attributes
    """)
