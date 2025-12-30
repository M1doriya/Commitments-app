"""
Kredit Lab Report Generator - Simple Version
=============================================
Upload JSON from Claude → Generate HTML Report

NO API KEY NEEDED!

Usage:
    streamlit run app.py
"""

import streamlit as st
import json
from datetime import datetime
from html_generator import generate_html_report

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Kredit Lab - Report Generator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1e3a8a, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .step-box {
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    }
    .step-number {
        display: inline-block;
        width: 32px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        font-weight: 700;
        margin-right: 12px;
    }
    .step-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
    }
    .grade-display {
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .grade-a { background: linear-gradient(135deg, #d1fae5, #a7f3d0); color: #065f46; }
    .grade-b { background: linear-gradient(135deg, #dbeafe, #bfdbfe); color: #1e40af; }
    .grade-c { background: linear-gradient(135deg, #fef3c7, #fde68a); color: #92400e; }
    .grade-d { background: linear-gradient(135deg, #ffedd5, #fed7aa); color: #9a3412; }
    .grade-e { background: linear-gradient(135deg, #fee2e2, #fecaca); color: #991b1b; }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: #d1fae5;
        border: 1px solid #10b981;
        color: #065f46;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: #dbeafe;
        border: 1px solid #3b82f6;
        color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
    st.title("Kredit Lab")
    st.markdown("**Report Generator**")
    st.markdown("---")
    
    st.markdown("### 📋 How To Use")
    st.markdown("""
    1. Chat with Claude on claude.ai
    2. Upload Experian PDF to Claude
    3. Claude gives you JSON output
    4. Upload JSON here
    5. Download HTML report!
    """)
    
    st.markdown("---")
    st.markdown("### 🏦 Banks Evaluated")
    st.markdown("""
    - RHB
    - Maybank
    - CIMB
    - Standard Chartered
    - SME Bank
    - Bank Rakyat
    """)
    
    st.markdown("---")
    st.markdown("v1.0 | No API Key Needed! ✅")

# =============================================================================
# MAIN CONTENT
# =============================================================================

st.markdown('<p class="main-header">🏦 Kredit Lab Report Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload JSON from Claude → Download HTML Report</p>', unsafe_allow_html=True)

# Workflow explanation
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">1</span>
        <span class="step-title">Chat with Claude</span>
        <p style="margin-top: 0.5rem; color: #64748b; font-size: 0.9rem;">
            Upload Experian PDF to Claude on claude.ai and get JSON analysis output
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">2</span>
        <span class="step-title">Upload JSON Here</span>
        <p style="margin-top: 0.5rem; color: #64748b; font-size: 0.9rem;">
            Save Claude's JSON output to a file and upload it below
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">3</span>
        <span class="step-title">Download Report</span>
        <p style="margin-top: 0.5rem; color: #64748b; font-size: 0.9rem;">
            Get your beautiful HTML report ready to view or share
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# FILE UPLOAD
# =============================================================================

st.markdown("### 📤 Upload JSON Analysis")

uploaded_file = st.file_uploader(
    "Upload the JSON file from Claude's analysis",
    type=["json"],
    help="This is the JSON output that Claude provides after analyzing an Experian PDF"
)

if uploaded_file:
    try:
        json_content = uploaded_file.read().decode('utf-8')
        analysis_data = json.loads(json_content)
        
        if "company" not in analysis_data or "banks" not in analysis_data:
            st.error("❌ Invalid JSON structure. Make sure it's from Claude's Kredit Lab analysis.")
            st.stop()
        
        st.markdown('<div class="success-box">✅ <strong>JSON loaded successfully!</strong></div>', unsafe_allow_html=True)
        st.session_state['analysis_data'] = analysis_data
        st.session_state['company_name'] = analysis_data.get('company', {}).get('name', 'Unknown')
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON file: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.stop()

# =============================================================================
# RESULTS & DOWNLOAD
# =============================================================================

if 'analysis_data' in st.session_state:
    
    st.markdown("---")
    st.markdown("### 📊 Analysis Summary")
    
    data = st.session_state['analysis_data']
    company = data.get('company', {})
    consolidated = data.get('consolidated', {})
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Company:</strong> {company.get('name', 'N/A')}<br>
        <strong>Registration:</strong> {company.get('reg_no', 'N/A')}
    </div>
    """, unsafe_allow_html=True)
    
    # Grade display
    final_grade = consolidated.get('final_grade', 'C')
    grade_class = f"grade-{final_grade.lower()}"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="grade-display {grade_class}">
            Grade: {final_grade}
        </div>
        """, unsafe_allow_html=True)
    
    # Score metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{consolidated.get('score', 0)}%")
    with col2:
        st.metric("Strict 1", f"{consolidated.get('strict1_pass', 0)}/{consolidated.get('strict1_total', 0)}")
    with col3:
        st.metric("Strict 2", f"{consolidated.get('strict2_pass', 0)}/{consolidated.get('strict2_total', 0)}")
    with col4:
        st.metric("Preference", f"{consolidated.get('preference_pass', 0)}/{consolidated.get('preference_total', 0)}")
    
    # Bank grades
    st.markdown("### 🏦 Bank Grades")
    banks = data.get('banks', {})
    bank_cols = st.columns(6)
    for i, (bank_name, bank_data) in enumerate(banks.items()):
        with bank_cols[i % 6]:
            grade = bank_data.get('final_grade', 'C')
            score = bank_data.get('score', 0)
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border-radius: 0.5rem; background: #f1f5f9; margin: 0.5rem 0;">
                <div style="font-size: 0.8rem; color: #64748b;">{bank_name}</div>
                <div style="font-size: 2rem; font-weight: 700;">{grade}</div>
                <div style="font-size: 0.8rem; color: #64748b;">{score}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Generate HTML
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
    html_report = generate_html_report(data)
    company_name_safe = company.get('name', 'report').replace(' ', '_').replace('/', '_')[:50]
    filename = f"KreditLab_Report_{company_name_safe}_{datetime.now().strftime('%Y%m%d')}.html"
    
    st.download_button(
        label="📥 Download HTML Report",
        data=html_report,
        file_name=filename,
        mime="text/html",
        help="Click to download the complete HTML report"
    )
    
    # Preview option
    with st.expander("👁️ Preview Report"):
        st.components.v1.html(html_report, height=800, scrolling=True)

else:
    st.info("👆 Upload a JSON file to get started")
