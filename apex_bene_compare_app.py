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

def normalize_allocation(value):
    """Normalize allocation percentage to float"""
    if pd.isna(value) or value == "":
        return 0.0
    try:
        # Handle percentage strings like "50%" or "50.5%"
        if isinstance(value, str) and "%" in value:
            return float(value.replace("%", "").strip())
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def extract_name_designation_allocation_date(row):
    """Extract name, designation, allocation, and last updated date from a row"""
    raw_designation = row.get("designation", "").strip()
    designation = normalize_designation(raw_designation)
    
    # Try to get name from first/last name fields
    first_name_raw = row.get("first_name", None)
    last_name_raw = row.get("last_name", None)
    first_missing = pd.isna(first_name_raw) or str(first_name_raw).strip() == ""
    last_missing = pd.isna(last_name_raw) or str(last_name_raw).strip() == ""
    
    # If first/last names are missing, use entity_name
    if first_missing and last_missing:
        name = normalize_name(row.get("entity_name", ""))
    else:
        first_name = normalize_name(first_name_raw)
        last_name = normalize_name(last_name_raw)
        name = f"{first_name} {last_name}".strip()
    
    # Get allocation percentage from "percentage" column
    allocation = normalize_allocation(row.get("percentage", 0))
    
    # Get last updated date - try multiple possible column names
    last_updated = ""
    possible_date_columns = ["last_updated", "updated_date", "modified_date", "date_modified", "last_modified", "updated", "modified"]
    
    for col in possible_date_columns:
        if col in row and not pd.isna(row.get(col)) and str(row.get(col)).strip() != "":
            last_updated = str(row.get(col)).strip()
            break
    
    return (designation, name, allocation, last_updated)

def group_beneficiaries_with_allocation_and_dates(df):
    """Group beneficiaries by account with allocation and date information"""
    grouped = {}
    for _, row in df.iterrows():
        acct = str(row.get("account_number")).strip()
        designation, name, allocation, last_updated = extract_name_designation_allocation_date(row)
        
        if acct not in grouped:
            grouped[acct] = set()
        
        # Only add if we have a valid name
        if name and name.strip():
            grouped[acct].add((designation, name, allocation, last_updated))
    
    return grouped

def check_specific_name_order_mismatches(bd_data, ac_data):
    """Check if names are swapped first/last name between BD and AC"""
    bd_names = {(name, designation, allocation) for designation, name, allocation, last_updated in bd_data}
    ac_names = {(name, designation, allocation) for designation, name, allocation, last_updated in ac_data}
    
    name_order_issues = []
    
    for bd_designation, bd_name, bd_allocation, bd_date in bd_data:
        bd_parts = bd_name.strip().split()
        if len(bd_parts) != 2:  # Only check two-part names
            continue
            
        bd_first, bd_last = bd_parts
        
        for ac_designation, ac_name, ac_allocation, ac_date in ac_data:
            ac_parts = ac_name.strip().split()
            if len(ac_parts) != 2:  # Only check two-part names
                continue
                
            ac_first, ac_last = ac_parts
            
            # Check if first/last are swapped
            if bd_first == ac_last and bd_last == ac_first:
                name_order_issues.append((
                    (bd_designation, bd_name, bd_allocation, bd_date),
                    (ac_designation, ac_name, ac_allocation, ac_date)
                ))
    
    return name_order_issues

def check_allocation_matches(bd_data, ac_data):
    """Check if allocations match between BD and AC for the same beneficiaries"""
    # Create dictionaries for easy lookup: {(designation, name): (allocation, date)}
    bd_allocations = {(designation, name): (allocation, last_updated) for designation, name, allocation, last_updated in bd_data}
    ac_allocations = {(designation, name): (allocation, last_updated) for designation, name, allocation, last_updated in ac_data}
    
    allocation_issues = []
    
    # Check allocations for matching beneficiaries
    for (designation, name) in bd_allocations:
        if (designation, name) in ac_allocations:
            bd_alloc, bd_date = bd_allocations[(designation, name)]
            ac_alloc, ac_date = ac_allocations[(designation, name)]
            
            # Allow for small floating point differences
            if abs(bd_alloc - ac_alloc) > 0.01:
                allocation_issues.append({
                    'designation': designation,
                    'name': name.title(),
                    'bd_allocation': bd_alloc,
                    'ac_allocation': ac_alloc,
                    'difference': abs(bd_alloc - ac_alloc),
                    'bd_date': bd_date,
                    'ac_date': ac_date
                })
    
    return allocation_issues

def check_total_allocations(bd_data, ac_data):
    """Check if total allocations match by designation"""
    # Calculate totals by designation
    bd_totals = {'primary': 0.0, 'contingent': 0.0}
    ac_totals = {'primary': 0.0, 'contingent': 0.0}
    
    for designation, name, allocation, last_updated in bd_data:
        if designation in bd_totals:
            bd_totals[designation] += allocation
    
    for designation, name, allocation, last_updated in ac_data:
        if designation in ac_totals:
            ac_totals[designation] += allocation
    
    total_issues = []
    for designation in ['primary', 'contingent']:
        bd_total = bd_totals[designation]
        ac_total = ac_totals[designation]
        
        if abs(bd_total - ac_total) > 0.01:  # Allow for small floating point differences
            total_issues.append({
                'designation': designation,
                'bd_total': bd_total,
                'ac_total': ac_total,
                'difference': abs(bd_total - ac_total)
            })
    
    return total_issues

def compare_beneficiaries_comprehensive(bd_benes, ac_benes):
    """Comprehensive comparison including names, designations, allocations, and dates"""
    # Extract just the names and designations for basic comparison
    bd_names_designations = {(designation, name) for designation, name, allocation, last_updated in bd_benes}
    ac_names_designations = {(designation, name) for designation, name, allocation, last_updated in ac_benes}
    
    # Check if names and designations match exactly
    names_designations_match = bd_names_designations == ac_names_designations
    
    # Check for specific name order issues
    name_order_issues = check_specific_name_order_mismatches(bd_benes, ac_benes)
    
    # Check allocation issues (only for matching beneficiaries)
    allocation_issues = check_allocation_matches(bd_benes, ac_benes)
    
    # Check total allocation issues
    total_allocation_issues = check_total_allocations(bd_benes, ac_benes)
    
    # Extract dates for display
    bd_dates = {last_updated for designation, name, allocation, last_updated in bd_benes if last_updated}
    ac_dates = {last_updated for designation, name, allocation, last_updated in ac_benes if last_updated}
    
    bd_last_updated = max(bd_dates) if bd_dates else ""
    ac_last_updated = max(ac_dates) if ac_dates else ""
    
    # Determine match status and details
    issues = []
    has_name_order_issue = False
    
    if names_designations_match and bd_benes == ac_benes:
        return True, "Perfect Match", False, [], [], [], bd_last_updated, ac_last_updated
    
    if name_order_issues:
        has_name_order_issue = True
        issue_details = []
        for (bd_designation, bd_name, bd_allocation, bd_date), (ac_designation, ac_name, ac_allocation, ac_date) in name_order_issues:
            issue_details.append(f"BD: {bd_name.title()} → AC: {ac_name.title()}")
        issues.append(f"Name Order Issues: {' | '.join(issue_details)}")
    
    if allocation_issues:
        alloc_details = []
        for issue in allocation_issues:
            alloc_details.append(f"{issue['name']} ({issue['designation'].title()}): BD {issue['bd_allocation']}% → AC {issue['ac_allocation']}%")
        issues.append(f"Allocation Mismatches: {' | '.join(alloc_details)}")
    
    if total_allocation_issues:
        total_details = []
        for issue in total_allocation_issues:
            total_details.append(f"{issue['designation'].title()}: BD {issue['bd_total']}% → AC {issue['ac_total']}%")
        issues.append(f"Total Allocation Issues: {' | '.join(total_details)}")
    
    if names_designations_match and not name_order_issues:
        # Names and designations match, but allocations might differ
        if allocation_issues or total_allocation_issues:
            return False, " | ".join(issues), False, allocation_issues, total_allocation_issues, [], bd_last_updated, ac_last_updated
        else:
            return True, "Names Match, Designation Differences", False, [], [], [], bd_last_updated, ac_last_updated
    
    if not names_designations_match and not name_order_issues:
        # Real name/designation mismatches
        bd_only = bd_names_designations - ac_names_designations
        ac_only = ac_names_designations - bd_names_designations
        
        mismatch_detail = []
        if bd_only:
            bd_formatted = [f"{designation.title()}: {name.title()}" for designation, name in sorted(bd_only)]
            mismatch_detail.append(f"BD Only: {', '.join(bd_formatted)}")
        if ac_only:
            ac_formatted = [f"{designation.title()}: {name.title()}" for designation, name in sorted(ac_only)]
            mismatch_detail.append(f"AC Only: {', '.join(ac_formatted)}")
        
        issues.extend(mismatch_detail)
    
    match_details = " | ".join(issues) if issues else "Unknown Issue"
    
    return False, match_details, has_name_order_issue, allocation_issues, total_allocation_issues, name_order_issues, bd_last_updated, ac_last_updated

def format_beneficiaries_display_with_allocation(bene_set):
    """Format beneficiaries for display with allocation"""
    if not bene_set:
        return "None"
    
    formatted = []
    for designation, name, allocation, last_updated in sorted(bene_set):
        formatted.append(f"{designation.title()}: {name.title()} ({allocation}%)")
    
    return " | ".join(formatted)

# --- Upload Files ---
bd_file = st.file_uploader("Upload BD_Bene.csv", type="csv")
ac_file = st.file_uploader("Upload AC_Bene.csv", type="csv")

if bd_file and ac_file:
    bd_df = pd.read_csv(bd_file)
    ac_df = pd.read_csv(ac_file)
    
    bd_df.columns = bd_df.columns.str.lower().str.strip()
    ac_df.columns = ac_df.columns.str.lower().str.strip()
    
    # Normalize visibility status
    bd_df["visibility_status"] = bd_df["status"].fillna("").astype(str).apply(normalize_bd_visibility_status)
    ac_df["visibility_status"] = ac_df["deleted"].fillna("").astype(str).apply(normalize_visibility_status)
    
    # Filter for active beneficiaries only
    bd_active_df = bd_df[bd_df["visibility_status"] == "active"]
    ac_active_df = ac_df[ac_df["visibility_status"] == "active"]
    
    # Group beneficiaries with allocation information
    grouped_bd = group_beneficiaries_with_allocation(bd_active_df)
    grouped_ac = group_beneficiaries_with_allocation(ac_active_df)
    
    # --- 3AA Accounts Logic ---
    three_aa_accounts = {
        acct for acct in set(grouped_bd.keys()).union(set(grouped_ac.keys()))
        if acct.startswith("3AA")
    }
    
    three_aa_entries = []
    for acct in three_aa_accounts:
        bd_benes = grouped_bd.get(acct, set())
        ac_benes = grouped_ac.get(acct, set())
        
        # Comprehensive comparison
        is_match, match_details, is_name_order_issue, allocation_issues, total_allocation_issues, name_order_pairs = compare_beneficiaries_comprehensive(bd_benes, ac_benes)
        
        # Create issue flags for filtering
        has_allocation_issues = len(allocation_issues) > 0
        has_total_allocation_issues = len(total_allocation_issues) > 0
        has_any_allocation_issues = has_allocation_issues or has_total_allocation_issues
        
        three_aa_entries.append({
            "account_number": acct,
            "bd_beneficiaries": format_beneficiaries_display_with_allocation(bd_benes),
            "ac_beneficiaries": format_beneficiaries_display_with_allocation(ac_benes),
            "match_status": "✅ Match" if is_match else "❌ Mismatch",
            "match_details": match_details,
            "is_name_order_issue": is_name_order_issue,
            "has_allocation_issues": has_any_allocation_issues,
            "individual_allocation_issues": has_allocation_issues,
            "total_allocation_issues": has_total_allocation_issues
        })
    
    three_aa_df = pd.DataFrame(three_aa_entries)
    
    # Summary metrics
    total_accounts = len(three_aa_df)
    perfect_matches = len(three_aa_df[three_aa_df["match_details"] == "Perfect Match"])
    name_matches = len(three_aa_df[three_aa_df["match_details"] == "Names Match, Designation Differences"])
    name_order_issues = len(three_aa_df[three_aa_df["is_name_order_issue"] == True])
    allocation_issues = len(three_aa_df[three_aa_df["has_allocation_issues"] == True])
    real_mismatches = total_accounts - perfect_matches - name_matches - name_order_issues - allocation_issues
    
    # Display results
    tab = st.tabs(["3AA Accounts Analysis"])[0]
    with tab:
        st.subheader("📊 3AA Accounts Summary")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("Total 3AA Accounts", f"{total_accounts:,}")
        with col2:
            st.metric("Perfect Matches", f"{perfect_matches:,}")
        with col3:
            st.metric("Name Matches (Minor Issues)", f"{name_matches:,}")
        with col4:
            st.metric("Name Order Issues", f"{name_order_issues:,}")
        with col5:
            st.metric("Allocation Issues", f"{allocation_issues:,}")
        with col6:
            st.metric("Real Mismatches", f"{real_mismatches:,}")
        
        # Filter options
        st.subheader("🔍 Filter Options")
        show_filter = st.selectbox(
            "Show:",
            ["All Accounts", "Only Real Mismatches", "Only Perfect Matches", "Only Name Matches (Minor Issues)", 
             "Only Name Order Issues", "Only Allocation Issues", "Only Individual Allocation Issues", "Only Total Allocation Issues"]
        )
        
        display_df = three_aa_df.copy()
        if show_filter == "Only Real Mismatches":
            display_df = display_df[
                (~display_df["match_details"].isin(["Perfect Match", "Names Match, Designation Differences"])) &
                (display_df["is_name_order_issue"] == False) &
                (display_df["has_allocation_issues"] == False)
            ]
        elif show_filter == "Only Perfect Matches":
            display_df = display_df[display_df["match_details"] == "Perfect Match"]
        elif show_filter == "Only Name Matches (Minor Issues)":
            display_df = display_df[display_df["match_details"] == "Names Match, Designation Differences"]
        elif show_filter == "Only Name Order Issues":
            display_df = display_df[display_df["is_name_order_issue"] == True]
        elif show_filter == "Only Allocation Issues":
            display_df = display_df[display_df["has_allocation_issues"] == True]
        elif show_filter == "Only Individual Allocation Issues":
            display_df = display_df[display_df["individual_allocation_issues"] == True]
        elif show_filter == "Only Total Allocation Issues":
            display_df = display_df[display_df["total_allocation_issues"] == True]
        
        st.subheader(f"📋 3AA Accounts Details ({len(display_df):,} accounts)")
        st.dataframe(display_df, use_container_width=True)
        
        # Download options
        st.subheader("📥 Download Options")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.download_button(
                label="📊 Download All 3AA Results",
                data=three_aa_df.to_csv(index=False),
                file_name="3aa_accounts_all.csv",
                mime="text/csv"
            )
        
        with col2:
            if name_order_issues > 0:
                name_order_df = three_aa_df[three_aa_df["is_name_order_issue"] == True]
                st.download_button(
                    label="📝 Download Name Order Issues",
                    data=name_order_df.to_csv(index=False),
                    file_name="3aa_accounts_name_order_fixes.csv",
                    mime="text/csv"
                )
        
        with col3:
            if allocation_issues > 0:
                allocation_df = three_aa_df[three_aa_df["has_allocation_issues"] == True]
                st.download_button(
                    label="💰 Download Allocation Issues",
                    data=allocation_df.to_csv(index=False),
                    file_name="3aa_accounts_allocation_issues.csv",
                    mime="text/csv"
                )
        
        with col4:
            if real_mismatches > 0:
                real_mismatch_df = three_aa_df[
                    (~three_aa_df["match_details"].isin(["Perfect Match", "Names Match, Designation Differences"])) &
                    (three_aa_df["is_name_order_issue"] == False) &
                    (three_aa_df["has_allocation_issues"] == False)
                ]
                st.download_button(
                    label="🚨 Download Real Mismatches Only",
                    data=real_mismatch_df.to_csv(index=False),
                    file_name="3aa_accounts_real_mismatches.csv",
                    mime="text/csv"
                )

else:
    st.info("👆 Please upload both BD and AC CSV files to begin analysis.")
    
    st.markdown("""
    ### What This Tool Does:
    
    This tool performs **comprehensive comparison** of 3AA account beneficiaries between BD and AC systems:
    
    - ✅ **Perfect Match**: Names, designations, and allocations all match exactly
    - 🟡 **Name Matches (Minor Issues)**: Same beneficiary names but different designations 
    - 📝 **Name Order Issues**: First/last names are swapped (e.g., "John Smith" vs "Smith John")
    - 💰 **Allocation Issues**: Same beneficiaries but different percentage allocations
    - ❌ **Real Mismatches**: Different beneficiary names between systems
    
    ### Key Allocation Validations:
    
    1. **Individual Allocation Matching**: Compares allocation percentages for each matching beneficiary
    2. **Total Allocation Validation**: Ensures primary and contingent totals match between systems
    3. **Detailed Issue Reporting**: Shows exact allocation differences (e.g., "John Smith (Primary): BD 50% → AC 60%")
    
    ### Features:
    - **Allocation percentage parsing**: Handles "50%", "50.5%", or numeric formats
    - **Floating point tolerance**: Ignores differences < 0.01% to handle rounding
    - **Comprehensive filtering**: View specific types of issues for targeted fixes
    - **Enhanced display**: Shows beneficiaries with their allocation percentages
    - **Multiple download options**: Separate files for different issue types
    
    This ensures both beneficiary information AND allocation percentages are synchronized between systems.
    """)
