import datetime
from fpdf import FPDF

# Function to generate code review reports in Markdown and PDF formats.
def generate_report(code: str, bugs: list, fixes: list) -> str:
    """
    Generates a code review report. Produces a Markdown string as the return value,
    and attempts to write a PDF file named 'code_review_report.pdf'.
    
    Parameters:
        code (str): The original Python source code.
        bugs (list): A list of detected bugs, each as a dict.
        fixes (list): A list of fixes (strings or dicts).
        
    Returns:
        str: The Markdown report, or "Report generation failed." on failure.
    """
    try:
        # Determine current date/time
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate summary statistics
        total_bugs = len(bugs)
        total_fixes = len(fixes)
        
        # Determine recommendation based on severity
        severities = [b.get("severity", "").lower() for b in bugs]
        if "high" in severities:
            recommendation = "CRITICAL"
        elif "medium" in severities:
            recommendation = "NEEDS FIX"
        else:
            recommendation = "PASS"
            
        # 1. Build Markdown Report
        md_lines = []
        md_lines.append("# Code Review Report")
        md_lines.append(f"**Date/Time:** {now_str}")
        md_lines.append("")
        md_lines.append("## Summary")
        md_lines.append(f"- **Total Bugs Found:** {total_bugs}")
        md_lines.append(f"- **Total Fixes Generated:** {total_fixes}")
        md_lines.append(f"- **Recommendation:** {recommendation}")
        md_lines.append("")
        
        md_lines.append("## Detected Bugs")
        if total_bugs > 0:
            md_lines.append("| Line | Type | Severity | Description |")
            md_lines.append("|---|---|---|---|")
            for bug in bugs:
                line = bug.get("line_number", "N/A")
                b_type = bug.get("bug_type", "N/A")
                sev = bug.get("severity", "N/A")
                desc = bug.get("description", "N/A")
                md_lines.append(f"| {line} | {b_type} | {sev} | {desc} |")
        else:
            md_lines.append("No bugs detected.")
        md_lines.append("")
        
        md_lines.append("## Fix Details")
        if total_fixes > 0:
            for idx, fix in enumerate(fixes):
                md_lines.append(f"### Fix {idx + 1}")
                if isinstance(fix, dict):
                    orig = fix.get("original", code)
                    evolved = fix.get("evolved", fix.get("fix", ""))
                else:
                    orig = code
                    evolved = fix
                    
                md_lines.append("**Original Code:**")
                md_lines.append("```python")
                md_lines.append(orig)
                md_lines.append("```")
                md_lines.append("**Evolved Fix:**")
                md_lines.append("```python")
                md_lines.append(evolved)
                md_lines.append("```")
                md_lines.append("")
        else:
            md_lines.append("No fixes generated.")
            
        md_lines.append("## Final Recommendation")
        md_lines.append(f"Status: **{recommendation}**")
        
        markdown_content = "\n".join(md_lines)
        
        # 2. Build PDF Report in a separate try/except
        try:
            print("[DEBUG] Initiating PDF generation...")
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("helvetica", style="B", size=18)
            pdf.cell(0, 12, "Code Review Report", ln=True, align="C")
            pdf.ln(5)
            
            # Metadata & Summary
            pdf.set_font("helvetica", size=10)
            pdf.cell(0, 6, f"Generated: {now_str}", ln=True)
            pdf.cell(0, 6, f"Recommendation: {recommendation}", ln=True)
            pdf.cell(0, 6, f"Total Bugs Found: {total_bugs}", ln=True)
            pdf.cell(0, 6, f"Total Fixes Generated: {total_fixes}", ln=True)
            pdf.ln(10)
            
            # Bug Table Header
            pdf.set_font("helvetica", style="B", size=11)
            pdf.cell(0, 8, "Detected Bugs List:", ln=True)
            pdf.ln(2)
            
            col_widths = [15, 40, 25, 110]
            pdf.set_font("helvetica", style="B", size=10)
            pdf.cell(col_widths[0], 8, "Line", border=1)
            pdf.cell(col_widths[1], 8, "Type", border=1)
            pdf.cell(col_widths[2], 8, "Severity", border=1)
            pdf.cell(col_widths[3], 8, "Description", border=1, ln=True)
            
            # Bug Table Rows
            pdf.set_font("helvetica", size=9)
            for bug in bugs:
                line = str(bug.get("line_number", "N/A"))
                b_type = str(bug.get("bug_type", "N/A"))
                sev = str(bug.get("severity", "N/A"))
                desc = str(bug.get("description", "N/A"))
                
                # Truncate description to fit page width safely
                if len(desc) > 65:
                    desc = desc[:62] + "..."
                    
                pdf.cell(col_widths[0], 8, line, border=1)
                pdf.cell(col_widths[1], 8, b_type, border=1)
                pdf.cell(col_widths[2], 8, sev, border=1)
                pdf.cell(col_widths[3], 8, desc, border=1, ln=True)
                
            pdf.output("code_review_report.pdf")
            print("Success: PDF report 'code_review_report.pdf' generated successfully.")
        except Exception as pdf_err:
            print(f"Error: Failed to generate PDF report: {pdf_err}")
            
        return markdown_content
        
    except Exception as e:
        print(f"[DEBUG] Error generating report: {e}")
        return "Report generation failed."
