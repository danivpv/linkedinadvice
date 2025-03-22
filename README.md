---
title: LinkedIn Career Advisor
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.22.0
app_file: app/main.py
pinned: true
---

# LinkedIn Career Advisor 🚀

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A professional career pathway analysis tool that leverages AI to provide tailored career path recommendations based on your professional background, education, and goals. No telemetry.

![LinkedIn Career Advisor Demo](https://img.shields.io/badge/Demo-Hugging%20Face%20Spaces-yellow)

## ✨ Features

- **Comprehensive Career Analysis**: Get detailed insights on potential career paths tailored to your unique professional background
- **Multi-dimensional Evaluation**: Each path is scored on financial potential, human impact, and opportunity creation
- **Customizable Preferences**: Adjust weights for different factors based on your personal priorities
- **Time Horizon Options**: Choose between short-term (3 years), mid-term (10 years), or long-term (10+ years) career planning
- **Easy Sharing**: Export your analysis to LinkedIn or copy to clipboard with a single click
- **Intuitive Interface**: User-friendly Gradio UI for seamless interaction

## 🔧 Installation

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/danivpv/linkedinadvice.git
cd linkedinadvice
```

2. Install dependencies using uv (recommended):
```bash
uv sync --all-extras
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## 🚀 Running Locally

Start the application with:

```bash
uv run poe start # alternatively, uv run gradio app/main.py
```

The Gradio interface will be available at `http://localhost:7860` in your browser.

## 📦 Project Structure

```
linkedin-career-advisor/
├── app/
│   ├── main.py          # Application entry point and Gradio UI
│   ├── constants.py     # Application constants and example data
│   └── utils.py         # Utility functions for clipboard and sharing
│
├── linkedinadvice/
│   ├── __init__.py
│   ├── career_analysis.py  # Career analysis using LangChain and LLM
│   └── monitoring.py       # API usage monitoring and logging
│
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (not tracked by git)
└── README.md            # Project documentation
```

## 🌐 Deploying to Hugging Face Spaces

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choose Gradio as the SDK
3. Push this repository to the created Space
4. Add your `OPENAI_API_KEY` as a secret in the Space settings

## 💻 Development

### Dependencies

- `gradio`: For the web interface
- `langchain`: For LLM integration and career analysis pipeline
- `openai`: For accessing GPT models
- `python-dotenv`: For environment variable management

### Adding New Features

To extend the application:
1. Modify the analysis logic in `linkedinadvice/career_analysis.py`
2. Update UI components in `app/main.py`
3. Add new constants in `app/constants.py` if needed

## 📊 Usage Example

1. **Input your professional experience**:
   - Add current and previous roles
   - Specify years of experience
   - List notable achievements

2. **Add educational background**:
   - Enter degrees, institutions, and dates
   - Highlight academic achievements

3. **Define your goals and preferences**:
   - Set career goals
   - Add additional insights
   - Adjust time horizon and factor weights

4. **Analyze and review results**:
   - Get personalized career path recommendations
   - See detailed scoring across dimensions
   - Export or share your results

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for providing the underlying language models
- [Gradio](https://gradio.app/) for the easy-to-use UI framework
framework

---

Built with ❤️ for career professionals worldwide