# 🏦 Kredit Lab - Report Generator

A Streamlit application that generates beautiful HTML reports from Claude's Experian credit analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone or download this repository
cd kredit_lab_streamlit

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📋 How It Works

1. **Chat with Claude** - Go to claude.ai and upload an Experian credit report PDF
2. **Get JSON Output** - Claude will analyze the report and output structured JSON
3. **Upload JSON Here** - Save Claude's JSON output to a file and upload it to this app
4. **Download Report** - Get your beautifully formatted HTML report!

## 🏦 Banks Evaluated

The Kredit Lab system evaluates creditworthiness against 6 Malaysian banks:

- RHB
- Maybank
- CIMB
- Standard Chartered
- SME Bank
- Bank Rakyat

## 📊 Parameters Analyzed

- **16 CCRIS Parameters** - Including CCRIS Vintage, Property Ownership, Overdraft Utilization, Conduct of Account, etc.
- **4 CTOS Parameters** - Including Legal Suits, Trade Bureau, Legal Status on Loan

## 🎯 Scoring System

| Classification | Weight | Impact |
|---------------|--------|--------|
| Strict 1 | 30% | Auto-reject if failed (Grade E) |
| Strict 2 | 30% | Decline if failed (Grade D) |
| Preference | 40% | Affects notch adjustment |

## 📁 Project Structure

```
kredit_lab_streamlit/
├── app.py              # Main Streamlit application
├── html_generator.py   # HTML report generation module
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── sample_analysis_output.json  # Example JSON for testing
```

## 📝 JSON Schema

The JSON output from Claude should follow this structure:

```json
{
  "company": {
    "name": "Company Name",
    "reg_no": "123456-X"
  },
  "meta": {
    "report_date": "2024-12-20",
    "analysis_date": "2024-12-21",
    "prepared_by": "Kredit Lab System"
  },
  "entities": [...],
  "banks": {
    "RHB": {...},
    "Maybank": {...},
    ...
  },
  "consolidated": {
    "score": 75.5,
    "raw_grade": "B",
    "final_grade": "B",
    ...
  },
  "strengths": [...],
  "attention_items": [...]
}
```

## 🔧 Dependencies

- streamlit
- pandas (optional, for data handling)

## 📄 License

This project is for internal use only.

## 🤝 Support

For issues or questions, contact the development team.

---

**Kredit Lab v1.0** - No API Key Needed! ✅
