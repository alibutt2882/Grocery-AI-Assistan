# 🛒 Grocery AI Assistant - Smart Shopping Companion

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**An intelligent web application that helps consumers make smarter, safer, and more cost-effective grocery purchasing decisions**

[![Demo](https://img.shields.io/badge/🚀-Live_Demo-9cf)](https://grocery-ai-assistan.streamlit.app/)
[![Report Bug](https://img.shields.io/badge/🐛-Report_Bug-red)](https://github.com/alibutt2882/Grocery-AI-Assistan/issues)
[![Request Feature](https://img.shields.io/badge/💡-Request_Feature-green)](https://github.com/alibutt2882/Grocery-AI-Assistan/issues)

</div>

## 📋 Table of Contents
- [🌟 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Installation & Setup](#️-installation--setup)
- [🚀 Usage Guide](#-usage-guide)
- [📁 Project Structure](#-project-structure)
- [🔮 Future Enhancement Plan](#-future-enhancement-plan)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🌟 Overview

The **Grocery AI Assistant** is an all-in-one digital companion that leverages **computer vision and data analytics** to analyze grocery products in real-time. Built using **Python and Streamlit**, this application helps users verify dietary compliance, assess produce quality, and find the best prices—all through an intuitive web interface.

### 🎯 Project Goals
- **Empower consumers** with real-time product information
- **Ensure dietary compliance** for religious and personal preferences
- **Reduce food waste** through expiry detection and freshness assessment
- **Save money** with price comparison and receipt analysis
- **Simplify shopping** with an integrated digital cart

## ✨ Key Features

### 📱 Smart Product Scanner
| Feature | Description | Technology |
|---------|-------------|------------|
| **Halal Verification** | Instantly checks product barcodes against a database to verify Halal certification status | Barcode scanning, Database lookup |
| **Price Comparison** | Compares store prices with market averages to alert you if you're overpaying | Web scraping, Price APIs |
| **Expiry Detection** | Reads text from packaging to flag expired or near-expiry items | OCR (Optical Character Recognition) |

### 🥦 AI Freshness Checker
- **Visual Quality Analysis**: Uses computer vision to analyze images of fruits, vegetables, or meat
- **Freshness Score**: Provides a 0–100 score based on color vibrancy, texture, and other visual indicators
- **Storage Recommendations**: Offers tailored advice based on the assessed quality

### 🧾 Bill & Receipt Checker
- **Error Detection**: Digitizes physical receipts to detect billing errors (like double charges)
- **Spending Analysis**: Analyzes shopping patterns and tracks cumulative savings over time
- **Digital Record Keeping**: Maintains a history of purchases for budget tracking

### 📊 Interactive Dashboard
- **Shopping Statistics**: Visualizes metrics like total items scanned and money saved
- **Virtual Shopping Cart**: Tracks running totals and dietary compliance before checkout
- **Personalized Insights**: Provides recommendations based on shopping history

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alibutt2882/Grocery-AI-Assistan.git
   cd Grocery-AI-Assistan
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

### 📦 Dependencies
The main dependencies include:
- `streamlit` - Web application framework
- `opencv-python` - Computer vision for image analysis
- `pytesseract` - OCR for text extraction
- `pandas` - Data manipulation and analysis
- `plotly` / `matplotlib` - Data visualization
- `requests` - API communication

## 🚀 Usage Guide

### First-Time Setup
1. Launch the application using `streamlit run app.py`
2. Configure API keys (if needed) for extended features
3. Allow camera access for barcode and image scanning features

### Using the Product Scanner
1. **Select the "Product Scanner" tab** from the sidebar
2. **Choose your input method**:
   - Camera: Use your device's camera to scan barcodes
   - Upload: Upload an image of a product barcode
3. **View results** including Halal status, price comparison, and expiry information

### Assessing Product Freshness
1. **Navigate to the "Freshness Checker" tab**
2. **Upload an image** of the fruit, vegetable, or meat
3. **Receive analysis** including freshness score and storage recommendations

### Analyzing Receipts
1. **Go to the "Receipt Checker" tab**
2. **Upload a photo or scanned image** of your grocery receipt
3. **Review the analysis** for errors, spending patterns, and savings

### Dashboard Overview
The main dashboard provides:
- Weekly/Monthly spending trends
- Dietary compliance statistics
- Cumulative savings tracker
- Virtual cart with running total

## 📁 Project Structure

```
Grocery-AI-Assistan/
├── app.py                    # Main Streamlit application
├── README.md                 # Project documentation (this file)
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License file
├── data/                    # Data files and databases
│   ├── halal_database.csv   # Halal certification database
│   └── price_database.json  # Price comparison database
├── models/                  # AI/ML models
│   ├── freshness_model.h5   # Freshness assessment model
│   └── ocr_model/          # OCR model for text extraction
├── utils/                   # Utility functions
│   ├── barcode_scanner.py  # Barcode scanning functionality
│   ├── image_processor.py  # Image processing functions
│   └── price_comparator.py # Price comparison logic
└── assets/                  # Static assets
    ├── images/             # Sample images and icons
    └── styles/             # Custom CSS styles
```

## 🔮 Future Enhancement Plan

### 🎯 Short-Term Goals (Next 3 Months)
| Feature | Priority | Description | Expected Impact |
|---------|----------|-------------|-----------------|
| **Mobile Application** | High | Develop iOS/Android versions for on-the-go shopping | Increase accessibility and user adoption |
| **Multi-language Support** | Medium | Add support for multiple languages (Arabic, Urdu, Spanish) | Expand to international markets |
| **Enhanced Barcode Database** | High | Integrate with global product databases (Open Food Facts) | Improve product recognition accuracy |
| **User Profiles** | Medium | Personalized settings and shopping history | Better user experience and customization |

### 📈 Medium-Term Goals (3-6 Months)
| Feature | Priority | Description | Technologies Considered |
|---------|----------|-------------|-------------------------|
| **Real-time Price Tracking** | High | Monitor price fluctuations across stores | Web scraping, Price APIs |
| **Nutritional Analysis** | Medium | Scan products for nutritional information | Computer vision, Nutrition databases |
| **Allergen Detection** | High | Identify common allergens in products | NLP, Ingredient analysis |
| **Social Features** | Low | Share deals, create shopping lists with family | User accounts, Social integration |

### 🚀 Long-Term Vision (6-12 Months)
| Feature | Description | Potential Impact |
|---------|-------------|-----------------|
| **AR Shopping Assistant** | Augmented Reality overlay in stores showing product info | Revolutionary in-store experience |
| **Predictive Shopping List** | AI suggests items based on consumption patterns | Reduce waste, optimize spending |
| **Supply Chain Transparency** | Track product journey from farm to shelf | Ethical consumption support |
| **Voice Integration** | Voice commands for hands-free shopping assistance | Accessibility improvement |

### 🔧 Technical Improvements
1. **Performance Optimization**
   - Implement caching for frequent database queries
   - Optimize image processing algorithms
   - Reduce application load time

2. **Scalability Enhancements**
   - Migrate to microservices architecture
   - Implement cloud-based processing for heavy computations
   - Add support for concurrent users

3. **AI Model Improvements**
   - Train custom models on larger grocery-specific datasets
   - Implement transfer learning for better accuracy
   - Add support for more product categories

## 🤝 Contributing

We welcome contributions to the Grocery AI Assistant project! Here's how you can help:

### 🐛 Reporting Issues
1. Check if the issue already exists in the [GitHub Issues](https://github.com/alibutt2882/Grocery-AI-Assistan/issues)
2. Create a new issue with a clear title and description
3. Include steps to reproduce, expected behavior, and screenshots if applicable

### 💻 Development Process
1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes and commit**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### 📝 Development Guidelines
- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Include tests for new functionality
- Update documentation accordingly

### 🏆 Areas Needing Contribution
- Frontend UI/UX improvements
- Additional language translations
- Database expansion (especially for international products)
- Testing and bug fixes

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Acknowledgments
- Streamlit team for the amazing web framework
- Open source computer vision libraries
- Contributors and testers who help improve this project

---

<div align="center">

### ⭐ Support the Project

If you find this project useful, please consider giving it a star on GitHub!

[![Star on GitHub](https://img.shields.io/github/stars/alibutt2882/Grocery-AI-Assistan?style=social)](https://github.com/alibutt2882/Grocery-AI-Assistan/stargazers)

**Happy Smart Shopping! 🛍️🤖**

</div>

---

*Last Updated: December 2025*  
*Project Maintainer: [alibutt2882](https://github.com/alibutt2882)*
