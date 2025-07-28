# Adobe Hackathon 2025 - Challenge 1a Solution

## PDF Outline Extraction System

A robust, high-performance PDF processing solution that extracts structured outline data from PDF documents and outputs JSON files. This is a **standalone version** designed specifically for Adobe India Hackathon 2025 Challenge 1a requirements.

## 🚀 Features

- **Fast Processing**: Processes PDFs in under 10 seconds (optimized for 50-page documents)
- **Universal Compatibility**: Works with any PDF format - forms, technical documents, reports, books
- **Multilingual Support**: Handles Japanese, Chinese, Korean, Arabic, Hebrew, Cyrillic and other scripts
- **Intelligent Extraction**: Uses advanced text analysis and formatting detection
- **Parallel Processing**: Multi-threaded for maximum performance
- **Docker Ready**: Fully containerized solution
- **Resource Efficient**: Optimized for 8 CPU + 16GB RAM constraints
- **Dependencies**: Only PyMuPDF + Python 

## 📋 Challenge Requirements Compliance

✅ **Execution Time**: ≤ 10 seconds for 50-page PDFs  
✅ **Resource Usage**: Works within 8 CPU + 16GB RAM  
✅ **Architecture**: AMD64 compatible  
✅ **Network**: No internet access required  
✅ **Open Source**: Uses only open-source libraries  
✅ **Input/Output**: Processes `/app/input` → `/app/output`  
✅ **Python Compatibility**: Python 3.13 ready (also works with 3.9+)

## 🛠 Installation & Setup

### Docker 
```bash
# Build the container
docker build -t pdf-processor .

# Run with your PDFs
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

### Local Python Setup
```bash
# Ensure Python +3.9 is installed (3.13.5 recommended)
python --version

# Make the virtual env
python -m venv .venv

# Manual installation
pip install -r requirements.txt

# Run the processor
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

## 🔧 Algorithm Approach

1. **TOC Extraction**: First attempts to use PDF's built-in Table of Contents
2. **Text Analysis**: Falls back to intelligent text analysis with formatting detection
3. **Heading Classification**: Uses font size, formatting, and content patterns
4. **Hierarchy Building**: Creates proper H1/H2/H3/H4 level structure
5. **Quality Filtering**: Removes artifacts, dates, and incomplete text fragments

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

## 📊 Performance Metrics

- **Processing Speed**: ~0.1 seconds per PDF page
- **Memory Usage**: <2GB for typical documents
- **CPU Efficiency**: Utilizes all available cores
- **Cache Performance**: 5-10x speedup on repeated processing

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
