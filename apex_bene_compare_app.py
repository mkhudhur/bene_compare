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
        
        # Special download for user-specified accounts with repeated names
        st.subheader("📥 Special Downloads")
        
        # List of accounts with repeated name issues (from user)
        repeated_name_account_list = [
            "3AA24505", "3AA39997", "3AA20200", "3AA08615", "3AA28991", "3AA23625", "3AA23109", "3AA29177", 
            "3AA37439", "3AA36909", "3AA18746", "3AA23696", "3AA27375", "3AA39620", "3AA24922", "3AA20755", 
            "3AA19654", "3AA25770", "3AA42413", "3AA29263", "3AA45269", "3AA32585", "3AA34732", "3AA22260", 
            "3AA35441", "3AA16862", "3AA10133", "3AA23475", "3AA35486", "3AA16779", "3AA34677", "3AA39403", 
            "3AA34186", "3AA38133", "3AA21580", "3AA21579", "3AA06744", "3AA12135", "3AA40074", "3AA46425", 
            "3AA21474", "3AA41190", "3AA24435", "3AA18715", "3AA28239", "3AA21951", "3AA30022", "3AA45578", 
            "3AA13625", "3AA24890", "3AA34881", "3AA18294", "3AA42327", "3AA22994", "3AA12361", "3AA19996", 
            "3AA20199", "3AA26326", "3AA31957", "3AA19149", "3AA21938", "3AA39128", "3AA44009", "3AA20450", 
            "3AA14943", "3AA38592", "3AA22232", "3AA21840", "3AA16004", "3AA22811", "3AA25792", "3AA29919", 
            "3AA11599", "3AA28989", "3AA18892", "3AA27670", "3AA12049", "3AA20340", "3AA39778", "3AA41110", 
            "3AA21314", "3AA18865", "3AA16155", "3AA27495", "3AA10095", "3AA19615", "3AA26362", "3AA40527", 
            "3AA20091", "3AA09239", "3AA30187", "3AA22152", "3AA11598", "3AA30178", "3AA40108", "3AA27669", 
            "3AA08404", "3AA45265", "3AA26457", "3AA23680", "3AA20920", "3AA24434", "3AA45249", "3AA22231", 
            "3AA27039", "3AA24339", "3AA45952", "3AA28442", "3AA41643", "3AA44224", "3AA16473", "3AA12657", 
            "3AA22807", "3AA24370", "3AA44700", "3AA41948", "3AA18516", "3AA08522", "3AA18862", "3AA12652", 
            "3AA31960", "3AA23054", "3AA25352", "3AA08521", "3AA24341", "3AA23002", "3AA39343", "3AA13897", 
            "3AA36334", "3AA14947", "3AA18528", "3AA36007", "3AA37442", "3AA30422", "3AA28227", "3AA39404", 
            "3AA37484", "3AA23011", "3AA34341", "3AA17154", "3AA19447", "3AA16807", "3AA37314", "3AA26325", 
            "3AA18767", "3AA21220", "3AA11531", "3AA26838", "3AA42328", "3AA28851", "3AA41186", "3AA44008", 
            "3AA32097", "3AA44922", "3AA12399", "3AA09340", "3AA39380", "3AA09807", "3AA41029", "3AA17122", 
            "3AA20383", "3AA29090", "3AA29370", "3AA37451", "3AA22974", "3AA28979", "3AA25430", "3AA18893", 
            "3AA45165", "3AA33987", "3AA12656", "3AA18747", "3AA21360", "3AA37937", "3AA42330", "3AA20857", 
            "3AA24049", "3AA23144", "3AA23282", "3AA12770", "3AA41744", "3AA22975", "3AA12895", "3AA22154", 
            "3AA42309", "3AA10225", "3AA11985", "3AA43897", "3AA46334", "3AA24132", "3AA39437", "3AA28440", 
            "3AA18500", "3AA34066", "3AA40979", "3AA26633", "3AA27078", "3AA05986", "3AA31056", "3AA24377", 
            "3AA28416", "3AA18863", "3AA42436", "3AA27772", "3AA19226", "3AA22949", "3AA26647", "3AA41109", 
            "3AA28237", "3AA36958", "3AA36737", "3AA17511", "3AA16154", "3AA16381", "3AA20792", "3AA43578", 
            "3AA43120", "3AA40195", "3AA34014", "3AA43888", "3AA21182", "3AA20385", "3AA44391", "3AA41832", 
            "3AA35548", "3AA29374", "3AA07377", "3AA44949", "3AA27079", "3AA21581", "3AA28228", "3AA44250", 
            "3AA20090", "3AA19499", "3AA27372", "3AA30049", "3AA37485", "3AA42323", "3AA29536", "3AA25460", 
            "3AA41439", "3AA36333", "3AA22034", "3AA16005", "3AA14109", "3AA26074", "3AA23993", "3AA17070", 
            "3AA41772", "3AA42348", "3AA44711", "3AA38846", "3AA15060", "3AA09154", "3AA38887", "3AA08896", 
            "3AA38538", "3AA22261", "3AA22651", "3AA08956", "3AA25767", "3AA34018", "3AA45264", "3AA16500", 
            "3AA19446", "3AA20195", "3AA25588", "3AA46112", "3AA37318", "3AA37677", "3AA12359", "3AA18693", 
            "3AA17162", "3AA42442", "3AA42943", "3AA22683", "3AA26158", "3AA24506", "3AA38616", "3AA22993", 
            "3AA13527", "3AA29178", "3AA24288", "3AA08523", "3AA43119", "3AA17291", "3AA18328", "3AA24966", 
            "3AA42676", "3AA41713", "3AA21464", "3AA28980", "3AA19222", "3AA06536", "3AA08671", "3AA13022", 
            "3AA28744", "3AA38593", "3AA36004", "3AA28441", "3AA40783", "3AA14030", "3AA30544", "3AA31237", 
            "3AA08955", "3AA31952", "3AA12659", "3AA19846", "3AA38954", "3AA18784", "3AA16856", "3AA24200", 
            "3AA32504", "3AA16881", "3AA23070", "3AA29928", "3AA27599", "3AA28525", "3AA24001", "3AA40981", 
            "3AA41712", "3AA43084", "3AA18766", "3AA16846", "3AA35534", "3AA34880", "3AA38542", "3AA39689", 
            "3AA24551", "3AA23705", "3AA19398", "3AA14524", "3AA24820", "3AA08426", "3AA31139", "3AA34136", 
            "3AA40819", "3AA19936", "3AA26467", "3AA37324", "3AA39201", "3AA24149", "3AA41842", "3AA44150", 
            "3AA44249", "3AA26193", "3AA26324", "3AA36331", "3AA44921", "3AA16704", "3AA24818", "3AA29921", 
            "3AA36910", "3AA41193", "3AA39379", "3AA14876", "3AA46335", "3AA22027", "3AA22872", "3AA31234", 
            "3AA26075", "3AA23056", "3AA09915", "3AA20559", "3AA40106", "3AA23474", "3AA38886", "3AA20384", 
            "3AA27600", "3AA07286", "3AA22871", "3AA08233", "3AA44035", "3AA28526", "3AA40782", "3AA13642", 
            "3AA40816", "3AA23283", "3AA11722", "3AA21934", "3AA41986", "3AA31783", "3AA23706", "3AA12653", 
            "3AA09125", "3AA06761", "3AA19228", "3AA33404", "3AA41395", "3AA05541", "3AA34137", "3AA34281", 
            "3AA17220", "3AA07380", "3AA41198", "3AA44026", "3AA41194", "3AA21463", "3AA22682", "3AA18716", 
            "3AA38425", "3AA12195", "3AA39473", "3AA20856", "3AA08670", "3AA43581", "3AA12402", "3AA14946", 
            "3AA16636", "3AA30046", "3AA19229", "3AA24857", "3AA14944", "3AA18753", "3AA27463", "3AA37482", 
            "3AA19847", "3AA37478", "3AA28330", "3AA43184", "3AA46241", "3AA31951", "3AA42232", "3AA12395", 
            "3AA20791", "3AA43577", "3AA26825", "3AA29371", "3AA34487", "3AA39375", "3AA22219", "3AA39497", 
            "3AA16780", "3AA12483", "3AA39829", "3AA41516", "3AA38783", "3AA21155", "3AA42331", "3AA19227", 
            "3AA24655", "3AA43121", "3AA42072", "3AA19617", "3AA18748", "3AA29927", "3AA13198", "3AA46332", 
            "3AA18529", "3AA25772", "3AA12033", "3AA18669", "3AA23112", "3AA23055", "3AA28529", "3AA41665", 
            "3AA44511", "3AA27063", "3AA08673", "3AA32501", "3AA36005", "3AA42269", "3AA18688", "3AA23093", 
            "3AA16001", "3AA23992", "3AA07379", "3AA43942", "3AA41841", "3AA09147", "3AA09638", "3AA12583", 
            "3AA25431", "3AA36394", "3AA41108", "3AA36332", "3AA09891", "3AA41460", "3AA43579", "3AA45967", 
            "3AA38682", "3AA20341", "3AA13660", "3AA23703", "3AA20921", "3AA21028", "3AA20194", "3AA18515", 
            "3AA06981", "3AA14011", "3AA45951", "3AA16253", "3AA21475", "3AA07869", "3AA16726", "3AA17878", 
            "3AA09122", "3AA06052", "3AA07378", "3AA19453", "3AA23737", "3AA38551", "3AA45267", "3AA14577", 
            "3AA17073", "3AA25860", "3AA12116", "3AA18694", "3AA22650", "3AA23830", "3AA29372", "3AA39127", 
            "3AA13898", "3AA42324", "3AA22789", "3AA10123", "3AA46528", "3AA39202", "3AA11733", "3AA12893", 
            "3AA20453", "3AA12655"
        ]
        
        # Filter the main dataframe for these specific accounts
        specified_accounts_df = three_aa_df[three_aa_df["account_number"].isin(repeated_name_account_list)]
        
        if len(specified_accounts_df) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📋 Download Specified Repeated Name Accounts",
                    data=specified_accounts_df.to_csv(index=False),
                    file_name="specified_repeated_name_accounts.csv",
                    mime="text/csv",
                    help=f"Download {len(specified_accounts_df)} accounts from your specified list"
                )
            with col2:
                st.metric("Specified Accounts Found", f"{len(specified_accounts_df)} / {len(repeated_name_account_list)}")
        else:
            st.info("None of the specified accounts with repeated names were found in the current dataset.")202", "3AA11733", "3AA12893", 
            "3AA20453", "3AA12655"
        ]
        
        # Filter the main dataframe for these specific accounts
        specified_accounts_df = three_aa_df[three_aa_df["account_number"].isin(repeated_name_account_list)]
        
        if len(specified_accounts_df) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📋 Download Specified Repeated Name Accounts",
                    data=specified_accounts_df.to_csv(index=False),
                    file_name="specified_repeated_name_accounts.csv",
                    mime="text/csv",
                    help=f"Download {len(specified_accounts_df)} accounts from your specified list"
                )
            with col2:
                st.metric("Specified Accounts Found", f"{len(specified_accounts_df)} / {len(repeated_name_account_list)}")
        else:
            st.info("None of the specified accounts with repeated names were found in the current dataset.")import streamlit as st
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

def check_repeated_names_in_beneficiary(name):
    """Check if a beneficiary name has repeated words/phrases"""
    name_clean = name.strip().lower()
    words = name_clean.split()
    
    # Check for exact word repetitions
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Find repeated words (excluding common words that might legitimately repeat)
    common_words = {'the', 'and', 'or', 'of', 'trust', 'family', 'jr', 'sr', 'ii', 'iii', 'iv'}
    repeated_words = []
    for word, count in word_counts.items():
        if count > 1 and word not in common_words and len(word) > 2:
            repeated_words.append(word)
    
    # Check for phrase repetitions (like "Aslan Family Trust Aslan Family Trust")
    name_parts = name_clean.split()
    
    # Check if first half equals second half (for even number of words)
    if len(name_parts) >= 4 and len(name_parts) % 2 == 0:
        mid_point = len(name_parts) // 2
        first_half = ' '.join(name_parts[:mid_point])
        second_half = ' '.join(name_parts[mid_point:])
        if first_half == second_half:
            return True, f"Full phrase repeated: '{first_half.title()}'"
    
    # Check for partial phrase repetitions at different positions
    for phrase_length in range(2, len(name_parts) // 2 + 1):
        for start_pos in range(len(name_parts) - phrase_length + 1):
            phrase = ' '.join(name_parts[start_pos:start_pos + phrase_length])
            
            # Check if this phrase appears again later in the name
            remaining_parts = name_parts[start_pos + phrase_length:]
            if len(remaining_parts) >= phrase_length:
                for check_pos in range(len(remaining_parts) - phrase_length + 1):
                    check_phrase = ' '.join(remaining_parts[check_pos:check_pos + phrase_length])
                    if phrase == check_phrase:
                        return True, f"Phrase repeated: '{phrase.title()}'"
    
    # Check for repeated individual words (excluding common ones)
    if repeated_words:
        return True, f"Words repeated: {', '.join([w.title() for w in repeated_words])}"
    
    return False, ""

def find_accounts_with_repeated_names(grouped_data, system_name):
    """Find accounts that have beneficiaries with repeated names"""
    repeated_name_accounts = []
    
    for acct, bene_set in grouped_data.items():
        account_issues = []
        
        for designation, name, allocation, last_updated in bene_set:
            has_repetition, repetition_detail = check_repeated_names_in_beneficiary(name)
            if has_repetition:
                account_issues.append({
                    'designation': designation,
                    'name': name.title(),
                    'allocation': allocation,
                    'last_updated': last_updated,
                    'repetition_detail': repetition_detail,
                    'system': system_name
                })
        
        if account_issues:
            repeated_name_accounts.append({
                'account_number': acct,
                'issues': account_issues
            })
    
    return repeated_name_accounts

def format_beneficiaries_display_with_allocation(bene_set):
    """Format beneficiaries for display with allocation"""
    if not bene_set:
        return "None"
    
    formatted = []
    for designation, name, allocation, last_updated in sorted(bene_set):
        formatted.append(f"{designation.title()}: {name.title()} ({allocation}%)")
    
    return " | ".join(formatted)
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
    
    # Group beneficiaries with allocation and date information
    grouped_bd = group_beneficiaries_with_allocation_and_dates(bd_active_df)
    grouped_ac = group_beneficiaries_with_allocation_and_dates(ac_active_df)
    
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
        is_match, match_details, is_name_order_issue, allocation_issues, total_allocation_issues, name_order_pairs, bd_last_updated, ac_last_updated = compare_beneficiaries_comprehensive(bd_benes, ac_benes)
        
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
            "bd_last_updated": bd_last_updated,
            "ac_last_updated": ac_last_updated,
            "is_name_order_issue": is_name_order_issue,
            "has_allocation_issues": has_any_allocation_issues,
            "individual_allocation_issues": has_allocation_issues,
            "total_allocation_issues": has_total_allocation_issues
        })
    
    # --- Find Repeated Name Issues ---
    bd_repeated_names = find_accounts_with_repeated_names(grouped_bd, "BD")
    ac_repeated_names = find_accounts_with_repeated_names(grouped_ac, "AC")
    
    # Combine and format repeated name issues
    all_repeated_names = []
    
    for account_data in bd_repeated_names:
        acct = account_data['account_number']
        for issue in account_data['issues']:
            all_repeated_names.append({
                'account_number': acct,
                'system': 'BD',
                'designation': issue['designation'].title(),
                'problematic_name': issue['name'],
                'allocation': f"{issue['allocation']}%",
                'last_updated': issue['last_updated'],
                'repetition_detail': issue['repetition_detail']
            })
    
    for account_data in ac_repeated_names:
        acct = account_data['account_number']
        for issue in account_data['issues']:
            all_repeated_names.append({
                'account_number': acct,
                'system': 'AC',
                'designation': issue['designation'].title(),
                'problematic_name': issue['name'],
                'allocation': f"{issue['allocation']}%",
                'last_updated': issue['last_updated'],
                'repetition_detail': issue['repetition_detail']
            })
    
    repeated_names_df = pd.DataFrame(all_repeated_names)
    
    three_aa_df = pd.DataFrame(three_aa_entries)
    
    # Summary metrics
    total_accounts = len(three_aa_df)
    perfect_matches = len(three_aa_df[three_aa_df["match_details"] == "Perfect Match"])
    name_matches = len(three_aa_df[three_aa_df["match_details"] == "Names Match, Designation Differences"])
    name_order_issues = len(three_aa_df[three_aa_df["is_name_order_issue"] == True])
    allocation_issues = len(three_aa_df[three_aa_df["has_allocation_issues"] == True])
    real_mismatches = total_accounts - perfect_matches - name_matches - name_order_issues - allocation_issues
    
    # Display results
    tab1, tab2 = st.tabs(["3AA Accounts Analysis", "Repeated Name Issues"])
    
    with tab1:
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
    
    with tab2:
        st.subheader("🔍 Repeated Name Issues")
        
        if len(repeated_names_df) > 0:
            # Summary metrics for repeated names
            total_repeated_issues = len(repeated_names_df)
            bd_issues = len(repeated_names_df[repeated_names_df["system"] == "BD"])
            ac_issues = len(repeated_names_df[repeated_names_df["system"] == "AC"])
            unique_accounts_affected = repeated_names_df["account_number"].nunique()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Repeated Name Issues", f"{total_repeated_issues:,}")
            with col2:
                st.metric("BD Issues", f"{bd_issues:,}")
            with col3:
                st.metric("AC Issues", f"{ac_issues:,}")
            with col4:
                st.metric("Accounts Affected", f"{unique_accounts_affected:,}")
            
            # Filter options for repeated names
            st.subheader("🔍 Filter Repeated Name Issues")
            system_filter = st.selectbox(
                "Show issues from:",
                ["All Systems", "BD Only", "AC Only"],
                key="repeated_names_filter"
            )
            
            display_repeated_df = repeated_names_df.copy()
            if system_filter == "BD Only":
                display_repeated_df = display_repeated_df[display_repeated_df["system"] == "BD"]
            elif system_filter == "AC Only":
                display_repeated_df = display_repeated_df[display_repeated_df["system"] == "AC"]
            
            st.subheader(f"📋 Repeated Name Issues Details ({len(display_repeated_df):,} issues)")
            st.dataframe(display_repeated_df, use_container_width=True)
            
            # Download option for repeated names
            st.subheader("📥 Download Repeated Name Issues")
            st.download_button(
                label="📝 Download Repeated Name Issues",
                data=repeated_names_df.to_csv(index=False),
                file_name="repeated_name_issues.csv",
                mime="text/csv"
            )
            
            # Show examples of the most common repeated name patterns
            st.subheader("📊 Most Common Repetition Patterns")
            pattern_counts = repeated_names_df["repetition_detail"].value_counts().head(10)
            if len(pattern_counts) > 0:
                st.bar_chart(pattern_counts)
        
        else:
            st.success("🎉 No repeated name issues found in either BD or AC systems!")
            st.info("All beneficiary names appear to be properly formatted without duplications.")

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
