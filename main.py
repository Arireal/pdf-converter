import streamlit as st
import pandas as pd
from fpdf import FPDF
from pathlib import Path
import os
from datetime import datetime
import zipfile
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="PDExcel",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern blue theme with rounded buttons
st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Content container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Headers styling */
    h1, h2, h3 {
        color: #667eea;
        font-weight: 700;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Download button styling */
    .stDownloadButton > button {
        border-radius: 20px;
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }

    /* File uploader styling */
    .uploadedFile {
        border-radius: 15px;
        background: rgba(102, 126, 234, 0.1);
        border: 2px dashed #667eea;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
    }

    /* Card styling */
    .css-1r6slb0 {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 15px;
        padding: 1rem;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #667eea;
    }

    /* Success/Error messages */
    .stAlert {
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with emoji
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 0;'>📄 PDExcel</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1.1rem; margin-top: 0;'>Transform Excel invoices into professional PDFs</p>",
    unsafe_allow_html=True)
st.markdown("---")

# Company customization section with clear labels
st.markdown(
    "<h3 style='color: #667eea; text-align: center;'>📝 Add Your Company Name and Logo</h3>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #666;'>Customize your invoices with your company information</p>",
    unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        "<p style='color: #667eea; font-weight: 600; margin-bottom: 0;'>Company Name:</p>",
        unsafe_allow_html=True)
    company_name = st.text_input(
        "Company Name",
        value="",
        placeholder="Type your company name here...",
        label_visibility="collapsed",
        key="company_name_input"
    )
    if not company_name:
        company_name = "PythonHow"  # Default if empty

with col2:
    st.markdown(
        "<p style='color: #667eea; font-weight: 600; margin-bottom: 0;'>Company Logo:</p>",
        unsafe_allow_html=True)
    logo_file = st.file_uploader(
        "Company Logo",
        type=['png', 'jpg', 'jpeg'],
        help="Drag and drop your logo image here",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# Main upload section
st.markdown("<h2 style='text-align: center;'>📤 Upload Your Invoices</h2>",
            unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Choose Excel files",
    type=['xlsx'],
    accept_multiple_files=True,
    help="Select one or more .xlsx invoice files",
    label_visibility="collapsed"
)

# Display uploaded files info
if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📁 Files Uploaded", len(uploaded_files))
    with col2:
        total_size = sum([file.size for file in uploaded_files]) / 1024
        st.metric("📊 Total Size", f"{total_size:.1f} KB")
    with col3:
        st.metric("⏱️ Status", "Ready")

    st.markdown("<br>", unsafe_allow_html=True)

    # Show file list
    with st.expander("📋 View Uploaded Files", expanded=True):
        for i, file in enumerate(uploaded_files, 1):
            st.write(f"{i}. **{file.name}** ({file.size / 1024:.1f} KB)")


def create_pdf_from_excel(file, company_name, logo_data=None):
    """Convert Excel file to PDF and return as bytes"""
    try:
        filename = Path(file.name).stem
        parts = filename.split("-")

        if len(parts) >= 2:
            invoice_nr = parts[0]
            date = parts[1]
        else:
            invoice_nr = filename
            date = datetime.now().strftime("%Y%m%d")

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(file, sheet_name="Sheet 1")

        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
            pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=25, h=8, txt=company_name)

        if logo_data is not None:
            logo_path = f"temp_logo_{datetime.now().timestamp()}.png"
            with open(logo_path, "wb") as f:
                f.write(logo_data)
            pdf.image(logo_path, w=10)
            os.remove(logo_path)

        return pdf.output(), filename

    except Exception as e:
        raise Exception(f"Error processing {file.name}: {str(e)}")


# Convert button
if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        convert_button = st.button("🚀 Convert to PDF",
                                   use_container_width=True, type="primary")

    if convert_button:
        logo_data = None
        if logo_file is not None:
            logo_data = logo_file.read()
            logo_file.seek(0)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>⚡ Converting...</h3>",
                    unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_text = st.empty()

        pdf_files = {}
        errors = []

        for idx, file in enumerate(uploaded_files):
            try:
                status_text.markdown(
                    f"<p style='text-align: center; color: #667eea;'>Processing: <b>{file.name}</b></p>",
                    unsafe_allow_html=True)

                # Simulate processing time for visual effect
                time.sleep(0.3)

                pdf_bytes, filename = create_pdf_from_excel(file, company_name,
                                                            logo_data)
                pdf_files[f"{filename}.pdf"] = pdf_bytes

            except Exception as e:
                errors.append(f"{file.name}: {str(e)}")

            progress_bar.progress((idx + 1) / len(uploaded_files))

        status_text.empty()
        progress_bar.empty()

        # Success message
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✅ Conversion Complete!")

        # Results metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Files", len(uploaded_files))
        with col2:
            st.metric("✅ Successful", len(pdf_files))
        with col3:
            st.metric("❌ Errors", len(errors))

        if errors:
            with st.expander("⚠️ View Errors", expanded=False):
                for error in errors:
                    st.error(error)

        if pdf_files:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<h3 style='text-align: center;'>📥 Download Your PDFs</h3>",
                unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # Individual downloads
            st.markdown("**Individual Files:**")
            cols = st.columns(min(3, len(pdf_files)))
            for idx, (pdf_name, pdf_data) in enumerate(pdf_files.items()):
                with cols[idx % min(3, len(pdf_files))]:
                    st.download_button(
                        label=f"📄 {pdf_name}",
                        data=pdf_data,
                        file_name=pdf_name,
                        mime="application/pdf",
                        use_container_width=True
                    )

            # Download all as ZIP
            if len(pdf_files) > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Download All:**")

                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w',
                                     zipfile.ZIP_DEFLATED) as zip_file:
                    for pdf_name, pdf_data in pdf_files.items():
                        zip_file.writestr(pdf_name, pdf_data)

                zip_buffer.seek(0)

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📦 Download All PDFs (ZIP)",
                        data=zip_buffer,
                        file_name=f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👆 Upload your Excel invoice files to get started")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #667eea; padding: 1rem;'>
        <p style='font-size: 0.9rem; margin: 0;'><b>PDExcel</b></p>
        <p style='font-size: 0.8rem; color: #888; margin: 0;'>Built with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)