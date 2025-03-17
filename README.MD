Collecting workspace informationHere's a comprehensive README.md file for the TalentScout System:

```markdown
# TalentScout Technical Interview Assistant 👨‍💼

A sophisticated AI-powered technical interview platform that automates candidate screening and evaluation.

## Features 🌟

- **Multi-language Support**: Available in English, Spanish, and French
- **Role-based Access**: Separate interfaces for candidates and recruiters
- **AI-powered Interviews**: Dynamic technical question generation using Google's Gemini AI
- **Real-time Evaluation**: Automated assessment of candidate responses
- **Interactive Dashboard**: Comprehensive analytics for recruiters
- **Secure Data Handling**: SQLite database with proper data validation

## Tech Stack 🛠️

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **AI Model**: Google Generative AI (Gemini)
- **Database**: SQLite
- **Key Libraries**:
  - `google-generativeai`: AI-powered question generation and evaluation
  - `streamlit`: Web interface
  - `pandas`: Data processing
  - `sqlite3`: Database management

## Installation 🔧


2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export GOOGLE_API_KEY=your_gemini_api_key  # On Windows: set GOOGLE_API_KEY=your_gemini_api_key
```

## Usage 🚀

1. Start the application:
```bash
streamlit run app.py
```

2. Access the platform at `http://localhost:5000`

3. Choose your role:
   - **Candidate**: Take technical interviews
   - **Recruiter**: Review candidate performances

## Project Structure 📁

```
talentscout-system/
├── app.py                 # Main application entry point
├── database.py           # Database operations
├── interview_manager.py  # Interview session management
├── llm_service.py       # AI service integration
├── translations.py      # Internationalization
├── utils.py            # Utility functions
├── views/              # UI components
│   ├── __init__.py
│   ├── candidate.py   # Candidate interface
│   └── recruiter.py   # Recruiter interface
└── .streamlit/        # Streamlit configuration
```

## Key Components 🔑

- **Interview Flow**:
  1. Candidate registration
  2. Technical stack declaration
  3. AI-generated questions
  4. Real-time response evaluation
  5. Comprehensive feedback

- **Recruiter Dashboard**:
  - Total interviews overview
  - Pass rate statistics
  - Average scores
  - Candidate filtering
  - Export functionality

## Security Measures 🔒

- Email and phone validation
- Unique candidate constraints
- Session state management
- Data privacy compliance
- Secure API key handling

## Customization 🎨

### Adding New Languages

Add translations to the translations.py file:

```python
translations["new_language"] = {
    "key": "translation",
    ...
}
```

### Modifying Question Generation

Adjust the prompt template in llm_service.py:

```python
prompt_template = """Your custom prompt here..."""
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors ✍️

- Your Name - Initial work - [YourGitHub](https://github.com/Aaditya4007)

