def normalize_name_order(name):
    """Normalize name to handle different word orders"""
    if not name or not name.strip():
        return ""
    
    # Split name into words and sort them alphabetically
    # This way "Randy Painter" and "Painter Randy" both become "painter randy"
    words = name.strip().lower().split()
    # Remove common prefixes/suffixes and sort
    normalized_words = sorted([word for word in words if word])
    return " ".join(normalized_words)

def extract_name_and_designation(row):
    """Extract just the name and designation, ignoring entity vs individual classification"""
    raw_designation = row.get("designation", "").strip()
    designation = normalize_designation(raw_designation)
    
    # Try to get name from first/last name fields
    first_name_raw = row.get("first_name", None)
    last_name_raw = row.get("last_name", None)
    first_missing = pd.isna(first_name_raw) or str(first_name_raw).strip() == ""
    last_missing = pd.isna(last_name_raw) or str(last_name_raw).strip() == ""
    
    # If first/last names are missing, use entity_name
    if firstimport streamlit as st
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

def extract_name_and_designation(row):
    """Extract just the name and designation, ignoring entity vs individual classification"""
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
    
    return (designation, name)

def group_beneficiaries_by_name(df):
    """Group beneficiaries by account, focusing on name and designation only"""
    grouped = {}
    for _, row in df.iterrows():
        acct = str(row.get("account_number")).strip()
        designation, name = extract_name_and_designation(row)
        
        if acct not in grouped:
            grouped[acct] = set()
        
        # Only add if we have a valid name
        if name and name.strip():
            grouped[acct].add((designation, name))
    
    return grouped

def compare_beneficiaries_flexibly(bd_benes, ac_benes):
    """Compare beneficiaries with flexible name matching"""
    # Extract just the names from both sets (ignoring designation for now)
    bd_names = {name for designation, name in bd_benes}
    ac_names = {name for designation, name in ac_benes}
    
    # Check if the names match exactly
    names_match = bd_names == ac_names
    
    # Check for name order issues (like "Randy Painter" vs "Painter Randy")
    name_order_issues = check_name_order_mismatches(bd_names, ac_names)
    
    # If names match exactly, check designations
    if names_match:
        return bd_benes == ac_benes, "Perfect Match" if bd_benes == ac_benes else "Names Match, Designation Differences", False
    elif name_order_issues:
        return False, "Name Order Mismatch", True
    else:
        # Names don't match - this is a real mismatch
        bd_only_names = bd_names - ac_names
        ac_only_names = ac_names - bd_names
        
        mismatch_detail = []
        if bd_only_names:
            mismatch_detail.append(f"BD Only: {', '.join(sorted(bd_only_names))}")
        if ac_only_names:
            mismatch_detail.append(f"AC Only: {', '.join(sorted(ac_only_names))}")
        
        return False, " | ".join(mismatch_detail), False

def check_name_order_mismatches(bd_names, ac_names):
    """Check if names are the same but in different order"""
    for bd_name in bd_names:
        bd_words = set(bd_name.lower().split())
        for ac_name in ac_names:
            ac_words = set(ac_name.lower().split())
            # If same words but different order
            if bd_words == ac_words and bd_name != ac_name:
                return True
    return False

def format_beneficiaries_display(bene_set):
    """Format beneficiaries for display"""
    if not bene_set:
        return "None"
    
    formatted = []
    for designation, name in sorted(bene_set):
        formatted.append(f"{designation.title()}: {name.title()}")
    
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
    
    # Group beneficiaries by name and designation
    grouped_bd = group_beneficiaries_by_name(bd_active_df)
    grouped_ac = group_beneficiaries_by_name(ac_active_df)
    
    # --- 3AA Accounts Logic ---
    three_aa_accounts = {
        acct for acct in set(grouped_bd.keys()).union(set(grouped_ac.keys()))
        if acct.startswith("3AA")
    }
    
    three_aa_entries = []
    for acct in three_aa_accounts:
        bd_benes = grouped_bd.get(acct, set())
        ac_benes = grouped_ac.get(acct, set())
        
        # Use flexible comparison
        is_match, match_details, is_name_order_issue = compare_beneficiaries_flexibly(bd_benes, ac_benes)
        
        three_aa_entries.append({
            "account_number": acct,
            "bd_beneficiaries": format_beneficiaries_display(bd_benes),
            "ac_beneficiaries": format_beneficiaries_display(ac_benes),
            "match_status": "✅ Match" if is_match else "❌ Mismatch",
            "match_details": match_details,
            "is_name_order_issue": is_name_order_issue
        })
    
    three_aa_df = pd.DataFrame(three_aa_entries)
    
    # Summary metrics
    total_accounts = len(three_aa_df)
    perfect_matches = len(three_aa_df[three_aa_df["match_details"] == "Perfect Match"])
    name_matches = len(three_aa_df[three_aa_df["match_details"] == "Names Match, Designation Differences"])
    name_order_issues = len(three_aa_df[three_aa_df["is_name_order_issue"] == True])
    real_mismatches = total_accounts - perfect_matches - name_matches - name_order_issues
    
    # Display results
    tab = st.tabs(["3AA Accounts Analysis"])[0]
    with tab:
        st.subheader("📊 3AA Accounts Summary")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total 3AA Accounts", f"{total_accounts:,}")
        with col2:
            st.metric("Perfect Matches", f"{perfect_matches:,}")
        with col3:
            st.metric("Name Matches (Minor Issues)", f"{name_matches:,}")
        with col4:
            st.metric("Name Order Issues", f"{name_order_issues:,}")
        with col5:
            st.metric("Real Mismatches", f"{real_mismatches:,}")
        
        # Filter options
        st.subheader("🔍 Filter Options")
        show_filter = st.selectbox(
            "Show:",
            ["All Accounts", "Only Real Mismatches", "Only Perfect Matches", "Only Name Matches (Minor Issues)", "Only Name Order Issues"]
        )
        
        display_df = three_aa_df.copy()
        if show_filter == "Only Real Mismatches":
            display_df = display_df[
                (~display_df["match_details"].isin(["Perfect Match", "Names Match, Designation Differences"])) &
                (display_df["is_name_order_issue"] == False)
            ]
        elif show_filter == "Only Perfect Matches":
            display_df = display_df[display_df["match_details"] == "Perfect Match"]
        elif show_filter == "Only Name Matches (Minor Issues)":
            display_df = display_df[display_df["match_details"] == "Names Match, Designation Differences"]
        elif show_filter == "Only Name Order Issues":
            display_df = display_df[display_df["is_name_order_issue"] == True]
        
        st.subheader(f"📋 3AA Accounts Details ({len(display_df):,} accounts)")
        st.dataframe(display_df, use_container_width=True)
        
        # Download options
        st.subheader("📥 Download Options")
        col1, col2, col3 = st.columns(3)
        
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
            if real_mismatches > 0:
                real_mismatch_df = three_aa_df[
                    (~three_aa_df["match_details"].isin(["Perfect Match", "Names Match, Designation Differences"])) &
                    (three_aa_df["is_name_order_issue"] == False)
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
    
    This tool compares 3AA account beneficiaries between BD and AC systems with **flexible name matching**:
    
    - ✅ **Perfect Match**: Names, designations, and classifications all match
    - 🟡 **Name Matches (Minor Issues)**: Same beneficiary names but different designations (e.g., Primary vs Contingent)
    - ❌ **Real Mismatches**: Different beneficiary names between systems
    
    ### Key Features:
    - **Ignores entity vs individual classification differences** 
    - **Focuses on actual beneficiary name mismatches**
    - **Provides clear categorization** of issue types
    - **Downloadable results** for targeted fixes
    
    This helps you focus on accounts that truly have different beneficiaries rather than just classification differences.
    """)
