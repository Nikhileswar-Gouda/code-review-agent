import os
import pandas as pd
import streamlit as st

# Import local modules
try:
    from detector import detect_bugs
    from ga_engine import evolve_fix
    from validator import validate_fix
    from memory import save_fix, recall_similar_fix
    from report import generate_report
except ImportError as e:
    st.error(f"Error importing modules: {e}")

# Comment: Page config
st.set_page_config(
  page_title="Code Review Agent",
  page_icon="🤖",
  layout="wide"
)

# Comment: Initialize session state variables
if "input_code" not in st.session_state:
    st.session_state["input_code"] = ""
if "bugs" not in st.session_state:
    st.session_state["bugs"] = None
if "code" not in st.session_state:
    st.session_state["code"] = ""
if "fixes" not in st.session_state:
    st.session_state["fixes"] = None
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# Comment: SIDEBAR Setup
st.sidebar.title("Configuration")
api_key_input = st.sidebar.text_input(
    "Enter Anthropic API Key", 
    type="password", 
    value=st.session_state["api_key"]
)
st.session_state["api_key"] = api_key_input

if st.session_state["api_key"]:
    st.sidebar.success("✅ API Key Set")

generations = st.sidebar.slider(
    "Generations", 
    min_value=3, 
    max_value=5, 
    value=3
)
pop_size = st.sidebar.slider(
    "Population Size", 
    min_value=4, 
    max_value=6, 
    value=4
)

# Comment: HEADER Section
st.title("🤖 Autonomous Code Review & Bug Fix Agent")
st.caption("Powered by Claude AI + Genetic Algorithms")

# Comment: TABS Definition
tab1, tab2, tab3, tab4 = st.tabs([
  "📝 Code Input",
  "🐛 Bug Detection", 
  "🧬 Fix Evolution (GA)",
  "📄 Results & Report"
])

# Sample buggy code templates
BUG1_CODE = """def divide_numbers(a, b):
    # Divide a by b
    return a / b

result = divide_numbers(10, 0)
print(result)"""

BUG2_CODE = """def write_log(message):
    # Open log file
    f = open("log.txt", "w")
    f.write(message)
    # File is never closed

write_log("System started")"""

BUG3_CODE = """def factorial(n):
    # Calculate factorial
    # Missing base case
    return n * factorial(n - 1)

print(factorial(5))"""

# Comment: TAB 1 — Code Input
with tab1:
    st.subheader("Input Python Code for Review")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Load Bug 1: Division by Zero"):
            st.session_state["input_code"] = BUG1_CODE
            st.rerun()
    with col2:
        if st.button("Load Bug 2: File Not Closed"):
            st.session_state["input_code"] = BUG2_CODE
            st.rerun()
    with col3:
        if st.button("Load Bug 3: Infinite Recursion"):
            st.session_state["input_code"] = BUG3_CODE
            st.rerun()
            
    code_area = st.text_area(
        "Python Code", 
        value=st.session_state["input_code"], 
        height=300
    )
    st.session_state["input_code"] = code_area
    
    if st.button("🔍 Start Analysis"):
        if not st.session_state["api_key"].strip():
            st.warning("Please enter your Anthropic API Key in the sidebar.")
        elif not code_area.strip():
            st.warning("Please enter or load some Python code to analyze.")
        else:
            try:
                with st.spinner("Analyzing code for bugs..."):
                    bugs = detect_bugs(code_area, st.session_state["api_key"])
                    st.session_state["bugs"] = bugs
                    st.session_state["code"] = code_area
                    st.session_state["fixes"] = None # Reset previous fixes
                    st.success(f"Analysis complete. Found {len(bugs)} bug(s).")
            except Exception as e:
                st.error(f"Error during bug detection call: {e}")

# Comment: TAB 2 — Bug Detection
with tab2:
    st.subheader("Bug Analysis Results")
    if st.session_state["bugs"] is None:
        st.info("No bugs detected yet. Go to the 'Code Input' tab and start analysis.")
    else:
        bugs = st.session_state["bugs"]
        st.metric("Total Bugs", len(bugs))
        
        # Prepare bug table and display severities
        table_data = []
        severity_counts = {"🔴 High": 0, "🟡 Medium": 0, "🟢 Low": 0}
        
        for bug in bugs:
            sev = bug.get("severity", "low").strip().lower()
            if sev == "high":
                sev_display = "🔴 High"
            elif sev == "medium":
                sev_display = "🟡 Medium"
            else:
                sev_display = "🟢 Low"
                
            severity_counts[sev_display] += 1
            table_data.append({
                "Line": bug.get("line_number", "N/A"),
                "Type": bug.get("bug_type", "N/A"),
                "Severity": sev_display,
                "Description": bug.get("description", "N/A")
            })
            
        st.write("### Severity Breakdown")
        df_counts = pd.DataFrame(list(severity_counts.items()), columns=["Severity", "Count"]).set_index("Severity")
        st.bar_chart(df_counts)
        
        st.write("### Bug Table")
        df_bugs = pd.DataFrame(table_data)
        st.dataframe(df_bugs, use_container_width=True)

# Comment: TAB 3 — Fix Evolution (GA)
with tab3:
    st.subheader("Genetic Algorithm Fix Evolution")
    if st.session_state["bugs"] is None:
        st.info("No bugs detected yet. Please run analysis in 'Code Input' tab.")
    else:
        bugs = st.session_state["bugs"]
        code = st.session_state["code"]
        api_key = st.session_state["api_key"]
        
        if st.button("🧬 Evolve Fixes for All Bugs"):
            st.session_state["fixes"] = []
            progress_bar = st.progress(0.0)
            
            for idx, bug in enumerate(bugs):
                desc = bug.get("description", "")
                st.write(f"#### Processing Bug {idx+1}: {desc}")
                
                # Check memory first
                recalled_fix = None
                try:
                    recalled_fix = recall_similar_fix(desc)
                except Exception as e:
                    st.error(f"Error calling memory recall: {e}")
                    
                if recalled_fix:
                    st.info("Similar fix recalled from memory.")
                    evolved_code = recalled_fix
                else:
                    try:
                        with st.spinner("Running Genetic Evolution..."):
                            evolved_code = evolve_fix(code, bug, api_key)
                    except Exception as e:
                        st.error(f"Error evolving fix via GA: {e}")
                        evolved_code = code
                        
                # Validate the fix
                try:
                    validation = validate_fix(code, evolved_code)
                    score = validation.get("score", 0.0)
                    diff = validation.get("diff", "")
                except Exception as e:
                    st.error(f"Error calling validator: {e}")
                    score = 0.0
                    diff = ""
                    
                # Save fix in session state
                st.session_state["fixes"].append({
                    "original": code,
                    "evolved": evolved_code,
                    "score": score,
                    "diff": diff,
                    "bug_desc": desc
                })
                
                # Save to memory if it's a new fix
                if not recalled_fix and evolved_code != code:
                    try:
                        save_fix(desc, evolved_code)
                    except Exception as e:
                        st.error(f"Error saving fix to memory: {e}")
                        
                progress_bar.progress((idx + 1) / len(bugs))
                
            st.success("Evolution complete!")
            st.rerun()
            
        # Display evolved fixes if available
        if st.session_state["fixes"]:
            for idx, f in enumerate(st.session_state["fixes"]):
                st.write("---")
                st.subheader(f"Fix for Bug {idx+1}: {f['bug_desc']}")
                st.metric("Validation Score", f"{f['score']:.2f}")
                
                col_left, col_right = st.columns(2)
                with col_left:
                    st.markdown("**Original Code:**")
                    st.code(f["original"], language="python")
                with col_right:
                    st.markdown("**Evolved Fix:**")
                    st.code(f["evolved"], language="python")
                    
                st.markdown("**Unified Diff:**")
                st.code(f["diff"], language="diff")

# Comment: TAB 4 — Results & Report
with tab4:
    st.subheader("Report & Export Results")
    if not st.session_state["fixes"]:
        st.info("No evolved fixes found. Run evolution in 'Fix Evolution (GA)' tab first.")
    else:
        bugs = st.session_state["bugs"]
        fixes = st.session_state["fixes"]
        code = st.session_state["code"]
        
        # Display severity recommendation alert
        severities = [b.get("severity", "").lower() for b in bugs]
        if "high" in severities:
            st.error("🚨 Final Recommendation Status: CRITICAL")
        elif "medium" in severities:
            st.warning("⚠️ Final Recommendation Status: NEEDS FIX")
        else:
            st.success("✅ Final Recommendation Status: PASS")
            
        # Generate and show Markdown report
        report_md = ""
        try:
            report_md = generate_report(code, bugs, fixes)
            st.markdown(report_md)
        except Exception as e:
            st.error(f"Error calling report generator: {e}")
            
        # Download PDF button if PDF report exists
        if os.path.exists("code_review_report.pdf"):
            try:
                with open("code_review_report.pdf", "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name="code_review_report.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error reading PDF file: {e}")
