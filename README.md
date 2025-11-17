# DoctorDork - Medical Professional Research Tool

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**Streamline your medical professional research from 30+ minutes to ~2 minutes**

[Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage) • [Export](#-export-capabilities) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

**DoctorDork** is a comprehensive Python-based command-line application designed to streamline medical professional research and discovery. By integrating multiple medical databases, review platforms, and professional networks into one unified interface, DoctorDork dramatically reduces research time while ensuring thoroughness.

### Why DoctorDork?

Looking for a doctor shouldn't be a daunting task. Whether you're:
- 🔍 **Searching for a specialist** in your area
- ✅ **Verifying medical licenses** across state boards
- ⭐ **Reading patient reviews** from multiple platforms
- 📱 **Finding professional profiles** on social media
- 📊 **Processing multiple queries** for research or comparison
- 📝 **Filing ethics complaints** with medical boards

DoctorDork consolidates all these tasks into a single, efficient tool.

---

## ✨ Key Features

### Nine Main Functions

| Function | Description | Resources |
|----------|-------------|-----------|
| **1. Doctor Contact Search** | Locates doctors with contact forms using optimized Google queries | Google Search |
| **2. Medical Board Lookup** | Direct links to verify licenses across all 51 US jurisdictions | 51 State Medical Boards |
| **3. Review Aggregation** | Searches 5 major review platforms simultaneously | Google, Healthgrades, Vitals, RateMDs, Zocdoc |
| **4. Ethics Violation Reporting** | Direct access to state medical board complaint filing | 51 State Medical Boards |
| **5. Social Media Search** | Locates professional profiles across social networks | LinkedIn, Twitter, Facebook |
| **6. Comprehensive Search** | Combines all features in one operation | All of the above |
| **7. Batch Processing** | Handles multiple queries simultaneously | N/A |
| **8. Settings** | Customizes preferences and manages search history | N/A |
| **9. Exit** | Closes the application | N/A |

### Advanced Capabilities

- 🎨 **Beautiful Interface** - Color-coded terminal output with progress indicators
- 💾 **Persistent Configuration** - Settings saved between sessions
- 📜 **Search History** - Track and review past searches (last 100 searches)
- 🌐 **Cross-Platform** - Works on Windows, macOS, Linux, Cloud Shell, Docker, Replit
- 🚀 **Zero External Dependencies** - Pure Python 3.7+ (no pip installs required)
- 📤 **Professional Export** - Results in CSV, JSON, or beautiful HTML reports

---

## 🎯 Technical Specifications

### Development Details
- **Language**: Pure Python 3.7+
- **Dependencies**: Zero required (stdlib only)
- **Codebase**: ~950 lines of clean, documented code
- **Platform Support**: Windows, macOS, Linux, Cloud Shell, Docker, Replit

### Data Coverage
- **Medical Boards**: 51 jurisdictions (all 50 states + DC)
- **Review Platforms**: 5 major services
- **Social Networks**: 3 major platforms
- **Total Integrations**: 59+ endpoints

---

## 🚀 Installation

### Quick Start (30 seconds)

```bash
# Clone the repository
git clone https://github.com/shadowdevnotreal/Doctor-Contact-Tool.git

# Navigate to directory
cd Doctor-Contact-Tool

# Run the application
python3 DoctorDork.py
```

That's it! No dependencies to install, no configuration required.

### Alternative: Direct Download

```bash
# Download the script directly
wget https://raw.githubusercontent.com/shadowdevnotreal/Doctor-Contact-Tool/main/DoctorDork.py

# Run it
python3 DoctorDork.py
```

### Cloud Platforms

#### Google Cloud Shell
```bash
# Open Cloud Shell and clone
git clone https://github.com/shadowdevnotreal/Doctor-Contact-Tool.git
cd Doctor-Contact-Tool
python3 DoctorDork.py
```

#### Replit
1. Create new Repl
2. Import from GitHub: `shadowdevnotreal/Doctor-Contact-Tool`
3. Run `DoctorDork.py`

#### Docker
```bash
# Pull Python image
docker run -it python:3.9 bash

# Inside container
git clone https://github.com/shadowdevnotreal/Doctor-Contact-Tool.git
cd Doctor-Contact-Tool
python3 DoctorDork.py
```

---

## 💻 Usage

### Interactive Menu

When you launch DoctorDork, you'll see a beautiful interactive menu:

```
╔════════════════════════════════════════════════════════════════╗
║                         MAIN MENU                              ║
╠════════════════════════════════════════════════════════════════╣
║  1. Doctor Contact Search    - Find doctors with contact forms║
║  2. Medical Board Lookup     - Verify licenses (51 states)    ║
║  3. Review Aggregation       - Search 5 review platforms      ║
║  4. Ethics Violation Report  - File medical board complaints  ║
║  5. Social Media Search      - Find professional profiles     ║
║  6. Comprehensive Search     - All features in one operation  ║
║  7. Batch Processing         - Process multiple queries       ║
║  8. Settings                 - Configure preferences          ║
║  9. Exit                     - Close application              ║
╚════════════════════════════════════════════════════════════════╝
```

### Example Workflows

#### 1. Finding a Doctor with Contact Form

```
Select option: 1

Enter Doctor Information:
Doctor's name: John Smith
City: Boston
State: MA
Specialty: Cardiology

✓ Browser opened successfully!
```

#### 2. Verifying Medical License

```
Select option: 2

Enter state (2-letter code) or 'ALL': MA

Medical Board: Massachusetts
URL: https://www.mass.gov/orgs/board-of-registration-in-medicine

✓ Browser opened successfully!
```

#### 3. Comprehensive Research

```
Select option: 6

Enter Doctor Information:
Doctor's name: Jane Doe
City: San Francisco
State: CA
Specialty: Pediatrics

ℹ 1/5 - Running contact search...
ℹ 2/5 - Looking up medical board...
ℹ 3/5 - Aggregating reviews...
ℹ 4/5 - Searching social media...
ℹ 5/5 - Complete!

✓ Comprehensive search completed!

Export results? (y/n): y
✓ Results exported to: doctordork_results_20250117_143022.html
```

#### 4. Batch Processing Multiple Doctors

```
Select option: 7

Enter doctors to search (one per line)
Example: John Smith, Boston, MA, Cardiology

Doctor #1: John Smith, Boston, MA, Cardiology
Doctor #2: Jane Doe, San Francisco, CA, Pediatrics
Doctor #3: [blank line to finish]

✓ Batch processing completed!
```

---

## 📤 Export Capabilities

DoctorDork supports three professional export formats:

### 1. CSV Export
- **Best for**: Excel analysis, data manipulation
- **Contains**: Category, Platform/Board, URL
- **File size**: Minimal
- **Use case**: Data analysis, spreadsheet imports

### 2. JSON Export
- **Best for**: API integration, automation workflows
- **Contains**: Timestamp, doctor info, all search results
- **File size**: Small
- **Use case**: Integration with other tools, programmatic access

### 3. HTML Export (Default)
- **Best for**: Presentation, sharing, archiving
- **Features**:
  - 🎨 Gradient design with modern styling
  - 📊 Interactive statistics dashboard
  - 📱 Mobile-responsive layout
  - 🔗 Clickable links to all resources
  - 📈 Visual categorization
- **File size**: Medium
- **Use case**: Professional reports, sharing with colleagues

#### HTML Export Preview

```html
🩺 DoctorDork Search Results
Comprehensive Medical Professional Research Report

Doctor Name: John Smith
City: Boston
State: MA
Specialty: Cardiology

[Statistics Dashboard]
3 Search Categories | 9 Total Resources | 51 Medical Boards

[Organized Results by Category]
```

---

## ⚙️ Settings & Configuration

### Available Settings

Access settings menu (Option 8) to configure:

| Setting | Options | Description |
|---------|---------|-------------|
| **Auto-open browser** | True/False | Automatically open search results in browser |
| **Export format** | CSV/JSON/HTML | Default format for exports |
| **Save history** | True/False | Save searches to history file |
| **Show progress** | True/False | Display progress indicators |

### Configuration Files

DoctorDork stores settings in your home directory:
- **Config**: `~/.doctordork_config.json`
- **History**: `~/.doctordork_history.json`

These files are created automatically and persist between sessions.

---

## 🗂️ Medical Board Coverage

DoctorDork includes direct links to all 51 US medical board verification portals:

<details>
<summary>View All 51 Jurisdictions (Click to expand)</summary>

- Alabama (AL) - Board of Medical Examiners
- Alaska (AK) - State Medical Board
- Arizona (AZ) - Medical Board
- Arkansas (AR) - State Medical Board
- California (CA) - Medical Board
- Colorado (CO) - Medical Board
- Connecticut (CT) - Medical Examining Board
- Delaware (DE) - Board of Medical Licensure
- District of Columbia (DC) - Board of Medicine
- Florida (FL) - Board of Medicine
- Georgia (GA) - Composite Medical Board
- Hawaii (HI) - Board of Medicine
- Idaho (ID) - State Board of Medicine
- Illinois (IL) - Medical Licensing Board
- Indiana (IN) - Medical Licensing Board
- Iowa (IA) - Board of Medicine
- Kansas (KS) - Board of Healing Arts
- Kentucky (KY) - Board of Medical Licensure
- Louisiana (LA) - State Board of Medical Examiners
- Maine (ME) - Board of Licensure in Medicine
- Maryland (MD) - Board of Physicians
- Massachusetts (MA) - Board of Registration in Medicine
- Michigan (MI) - Board of Medicine
- Minnesota (MN) - Board of Medical Practice
- Mississippi (MS) - State Board of Medical Licensure
- Missouri (MO) - State Board of Registration
- Montana (MT) - Board of Medical Examiners
- Nebraska (NE) - DHHS Licensure Unit
- Nevada (NV) - State Board of Medical Examiners
- New Hampshire (NH) - Board of Medicine
- New Jersey (NJ) - State Board of Medical Examiners
- New Mexico (NM) - Medical Board
- New York (NY) - State Board for Medicine
- North Carolina (NC) - Medical Board
- North Dakota (ND) - Board of Medical Examiners
- Ohio (OH) - State Medical Board
- Oklahoma (OK) - Board of Medical Licensure
- Oregon (OR) - Medical Board
- Pennsylvania (PA) - State Board of Medicine
- Rhode Island (RI) - Board of Medical Licensure
- South Carolina (SC) - Board of Medical Examiners
- South Dakota (SD) - Board of Medical Examiners
- Tennessee (TN) - Board of Medical Examiners
- Texas (TX) - Medical Board
- Utah (UT) - Physicians Licensing Board
- Vermont (VT) - Board of Medical Practice
- Virginia (VA) - Board of Medicine
- Washington (WA) - Medical Commission
- West Virginia (WV) - Board of Medicine
- Wisconsin (WI) - Medical Examining Board
- Wyoming (WY) - Board of Medicine

</details>

---

## 🎓 Use Cases

### For Patients
- 🏥 Find specialists in your area
- ✅ Verify doctor credentials and licenses
- ⭐ Read reviews from multiple platforms
- 📧 Quickly access contact forms

### For Researchers
- 📊 Compare multiple doctors simultaneously
- 💾 Export data for analysis
- 📝 Track search history
- 🔄 Batch process large lists

### For Healthcare Professionals
- 🔍 Research colleagues and competitors
- 📱 Find professional online presence
- 🌐 Verify licenses across states
- 📈 Market research and analysis

### For Legal/Compliance
- ⚖️ File ethics complaints
- 📋 Verify credentials
- 📄 Generate professional reports
- 🗂️ Maintain search documentation

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
- Use GitHub Issues
- Include Python version, OS, and error messages
- Provide steps to reproduce

### Feature Requests
- Check existing issues first
- Describe use case and expected behavior
- Consider submitting a pull request

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

- ✅ Free to use, modify, and distribute
- ✅ Must remain open source
- ✅ No warranty provided
- ✅ See [LICENSE](LICENSE) file for full details

---

## 🙏 Acknowledgments

- **Inspired by**: [LawyerDork](https://github.com/shadowdevnotreal/Lawyer-Web-Contact-Tool)
- **Author**: Slow (shadowdevnotreal)
- **Special Thanks**: To the open-source community

---

## 📞 Support

### Get Help
- 📖 Read this README
- 🐛 [Report Issues](https://github.com/shadowdevnotreal/Doctor-Contact-Tool/issues)
- 💬 [Discussions](https://github.com/shadowdevnotreal/Doctor-Contact-Tool/discussions)

### Donate

If DoctorDork saves you time and helps your research:

<a href="https://www.buymeacoffee.com/diatasso" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="40">
</a>

---

## 📊 Statistics

- **Research Time Saved**: 30+ minutes → ~2 minutes
- **Data Sources**: 59+ integrated endpoints
- **Jurisdictions Covered**: All 51 US medical boards
- **Review Platforms**: 5 major services
- **Export Formats**: 3 professional options
- **Dependencies Required**: 0

---

## 🔮 Roadmap

### Version 2.1 (Planned)
- [ ] Insurance acceptance lookup
- [ ] Hospital affiliations search
- [ ] Education and training verification
- [ ] Publication search integration

### Version 2.2 (Planned)
- [ ] Malpractice lawsuit database integration
- [ ] Medicare/Medicaid participation lookup
- [ ] Board certification verification
- [ ] Advanced filtering and sorting

### Community Requested
- [ ] GUI version
- [ ] Web interface
- [ ] API endpoints
- [ ] Mobile app

---

## ⚡ Quick Reference

### Run DoctorDork
```bash
python3 DoctorDork.py
```

### Configuration Files
```
~/.doctordork_config.json   # Settings
~/.doctordork_history.json  # Search history
```

### Supported Python Versions
- Python 3.7+
- No external dependencies required

### Supported Platforms
- ✅ Windows (7, 8, 10, 11)
- ✅ macOS (10.12+)
- ✅ Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- ✅ Google Cloud Shell
- ✅ Docker
- ✅ Replit
- ✅ Any platform with Python 3.7+

---

<div align="center">

**Made with ❤️ by Slow**

⭐ **Star this repo** if DoctorDork helps you! ⭐

[Report Bug](https://github.com/shadowdevnotreal/Doctor-Contact-Tool/issues) • [Request Feature](https://github.com/shadowdevnotreal/Doctor-Contact-Tool/issues) • [Donate](https://www.buymeacoffee.com/diatasso)

</div>
