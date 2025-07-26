#!/usr/bin/env python3
"""
Setup script for Adobe 1A Challenge - Python 3.13 Compatibility Check
"""

import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 9:
        print("❌ Error: Python 3.9+ required (3.13 recommended)")
        return False
    elif version.minor >= 13:
        print("✅ Python 3.13+ detected - Perfect!")
    elif version.minor >= 9:
        print("✅ Python 3.9+ detected - Compatible")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        "fitz",  # PyMuPDF
        "sklearn",
        "numpy", 
        "numba",
        "cachetools",
        "psutil",
        "nltk",
        "langdetect",
        "spacy",
        "pydantic"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def main():
    """Main setup function"""
    print("Adobe 1A Challenge - Python 3.13 Setup")
    print("=" * 40)
    
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("You can now run: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
