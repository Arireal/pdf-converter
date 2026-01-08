# 📄 Excel to PDF Invoice Converter

A modern web application that transforms Excel invoices into professionally formatted PDF documents with customizable branding. Built with Streamlit for an intuitive, browser-based interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Batch Processing** - Convert multiple Excel invoices to PDF in one go
- **Custom Branding** - Add your company logo and name to each invoice
- **Real-time Progress** - Visual feedback during conversion process
- **Flexible Downloads** - Download individual PDFs or all files as a ZIP archive
- **Error Handling** - Comprehensive error reporting for failed conversions
- **Clean Interface** - Modern, intuitive UI built with Streamlit
- **Cloud Ready** - Easily deployable to Streamlit Cloud

  <img width="682" height="356" alt="Untitled design(13)" src="https://github.com/user-attachments/assets/21688b85-8a5f-446b-8a23-16ded2230952" />


## 🚀 Demo

[Live Demo](https://pdf-invoice-converter-app.streamlit.app/) 

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[fpdf2](https://pyfpdf.github.io/fpdf2/)** - PDF generation library
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and Excel file processing
- **[openpyxl](https://openpyxl.readthedocs.io/)** - Excel file reading engine

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-invoices.git
   cd pdf-invoices
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage

### Running Locally

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`

3. **Convert invoices**
   - Upload one or more Excel files (.xlsx)
   - Optionally customize company name and upload logo
   - Click "Convert to PDF"
   - Download individual PDFs or all as ZIP

### Excel File Format

Your Excel files should follow this structure:

**Filename format:** `InvoiceNumber-Date.xlsx` (e.g., `10001-20240115.xlsx`)

**Required columns:**
- `product_id` - Product identifier
- `product_name` - Product description
- `amount_purchased` - Quantity
- `price_per_unit` - Unit price
- `total_price` - Total amount

**Sheet name:** `Sheet 1`

### Example Excel Structure

| product_id | product_name | amount_purchased | price_per_unit | total_price |
|------------|--------------|------------------|----------------|-------------|
| 1001       | Product A    | 5                | 10.00          | 50.00       |
| 1002       | Product B    | 3                | 15.00          | 45.00       |

## ☁️ Deployment

### Deploy to Streamlit Cloud

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `main.py`
   - Click "Deploy"

3. **Configure secrets** (if needed)
   - Go to app settings
   - Add any required environment variables

## 📁 Project Structure

```
pdf-invoices/
│
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore rules
```

## 🔧 Configuration

### Customization Options

- **Company Name** - Set in the sidebar (default: "PythonHow")
- **Company Logo** - Upload PNG, JPG, or JPEG files
- **PDF Format** - A4 portrait orientation
- **Font** - Times New Roman

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'fpdf'**
```bash
pip install fpdf2
```

**Excel file not recognized**
- Ensure file extension is `.xlsx`
- Verify sheet name is "Sheet 1"
- Check that all required columns are present

**PDF generation fails**
- Verify Excel data contains no null values in required columns
- Ensure numeric columns contain valid numbers
- Check that filename follows the format: `InvoiceNumber-Date.xlsx`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@Arireal](https://github.com/Arireal)
- LinkedIn: [Your LinkedIn]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/ariane-souza-dev/))

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- fpdf2 contributors for the PDF generation library
- Pandas community for data processing tools

## 📮 Support

For support, email your-email@example.com or open an issue in the GitHub repository.

---

Made with ❤️ and Python
