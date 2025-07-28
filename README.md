# Adobe Hackathon 2025 - Challenge 1a Solution

## PDF Outline Extraction System

A robust, high-performance PDF processing solution that extracts structured outline data from PDF documents and outputs JSON files. This is a **standalone version** designed specifically for Adobe India Hackathon 2025 Challenge 1a requirements.

## 🚀 What Can This Tool Do?

This tool helps you:
- Extract outlines from PDFs quickly (less than 10 seconds for a 50-page document)
- Work with any type of PDF (books, reports, forms, technical documents)
- Handle multiple languages (including Japanese, Chinese, Korean, Arabic, Hebrew, and more)
- Detect document structure automatically
- Process multiple files at once for better speed
- Run either in Docker or directly on your computer
- Work efficiently without heavy resource usage
- Keep things simple with minimal software requirements

## 📋 Challenge Requirements Compliance

✅ **Execution Time**: ≤ 10 seconds for 50-page PDFs  
✅ **Resource Usage**: Works within 8 CPU + 16GB RAM  
✅ **Architecture**: AMD64 compatible  
✅ **Network**: No internet access required  
✅ **Open Source**: Uses only open-source libraries  
✅ **Input/Output**: Processes `/app/input` → `/app/output`  
✅ **Python Compatibility**: Python 3.13 ready (also works with 3.9+)

## 🛠 How to Install and Run

You have two ways to run this tool:

### 1. Using Docker (Recommended for Most Users)
If you have Docker installed, just run these commands:
```bash
# First time setup - create the processor
docker build -t pdf-processor .

# Run it with your PDF files
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

### 2. Direct Installation (For Python Users)
If you prefer to run it directly with Python:
```bash
<<<<<<< Updated upstream
# Ensure Python 3.9+ is installed (3.13.5 recommended)
=======
# Check if you have Python 3.9 or newer
>>>>>>> Stashed changes
python --version

# Create a clean environment
python -m venv .venv

# Install the required tools
pip install -r requirements.txt

# Start processing your PDFs
python main.py
```

## 🛠 Technology Stack

- **Language**: Python 3.9+ (3.13.5)
- **PDF Processing**: PyMuPDF 
- **Container**: Docker with linux/amd64 platform
- **Dependencies**: Minimal footprint - just PyMuPDF + Python standard library

## 🏗 Architecture

```
src/
├── pdf_extractor.py      # Main PDF processing engine
├── text_processor.py     # Text cleaning and formatting
├── heading_classifier.py # Intelligent heading detection
├── outline_hierarchy.py  # Structure building
├── cache_manager.py      # Performance caching
└── config.py            # Configuration management
```

## 🔧 How Does It Work?

The tool processes your PDFs in these steps:

1. First, it looks for any existing table of contents in the PDF
2. If that's not available, it analyzes the text layout and formatting
3. It identifies headings based on how they look and where they appear
4. It organizes everything into a clear structure (main headings, subheadings, etc.)
5. Finally, it cleans up the results by removing any unnecessary text or numbers

## 📦 Quick Start Commands

### Docker Build & Run
```bash
# Build the container
docker build --platform linux/amd64 -t pdf-processor .

# Run processing
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

## 📊 How Fast Is It?

Here's what you can expect:
- It takes about 0.1 seconds to process each page
- Uses less than 2GB of memory for most documents
- Makes good use of your computer's processing power
- Gets even faster when processing the same file again

## 🧪 Testing

Local testing with sample data:
```bash
# Place PDFs in input/ directory
mkdir -p input output

# Run processing
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor

# Check results in output/ directory
```

## 📋 Output Format

Each PDF generates a corresponding JSON file with:
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "1.1 Overview",
      "page": 2
    }
  ]
}
```

## 🎯 Hackathon Advantages

- **Reliability**: Handles edge cases and malformed PDFs gracefully
- **Performance**: Optimized for the 10-second constraint
- **Scalability**: Processes multiple PDFs efficiently in parallel
- **Quality**: Advanced filtering removes noise and artifacts
- **Flexibility**: Works with diverse PDF types and layouts
- **Minimal Footprint**: Only one external dependency (PyMuPDF) for faster deployment
- **Security**: Reduced attack surface with minimal dependencies
- **Multilingual**: Supports Japanese, Chinese, Korean, Arabic, Hebrew, Cyrillic and other scripts
- **Bonus Ready**: Implements multilingual support for bonus points (up to 10 points)

## 🏆 Solution Highlights

This solution demonstrates advanced PDF processing capabilities suitable for production use, while meeting all hackathon constraints. The intelligent text analysis approach ensures high-quality outline extraction across diverse document types.
