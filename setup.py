#!/usr/bin/env python3
"""
Setup script for Adobe 1A Challenge - Python 3.13 Compatibility Check
"""

import sys
import subprocess
import platform
import os
import venv

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = ".venv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists at {venv_path}")
        return True
    
    print(f"📦 Creating virtual environment at {venv_path}...")
    try:
        venv.create(venv_path, with_pip=True)
        print(f"✅ Virtual environment created successfully!")
        print(f"💡 To activate it manually, run:")
        print(f"   {get_activation_command()}")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def get_venv_python():
    """Get the Python executable path for the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(".venv", "Scripts", "python.exe")
    else:
        # Linux, macOS, and other Unix-like systems
        return os.path.join(".venv", "bin", "python")

def get_activation_command():
    """Get the virtual environment activation command for the current platform"""
    if platform.system() == "Windows":
        return ".venv\\Scripts\\activate"
    else:
        # Linux, macOS, and other Unix-like systems
        return "source .venv/bin/activate"

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python executable: {sys.executable}")
    
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
    
    # Use virtual environment Python if it exists and is valid
    venv_python = get_venv_python()
    if os.path.exists(".venv") and os.path.exists(venv_python):
        python_exe = venv_python
        print(f"Using virtual environment Python: {python_exe}")
    else:
        python_exe = sys.executable
        print(f"Using system Python: {python_exe}")
    
    # Get the absolute path to requirements.txt
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("❌ Error: requirements.txt not found")
        return False
    
    try:
        # Upgrade pip first
        print("Upgrading pip...")
        result = subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], 
                               check=True, capture_output=True, text=True)
        
        # Install requirements
        print("Installing requirements...")
        result = subprocess.run([python_exe, "-m", "pip", "install", "-r", requirements_path], 
                               check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        "fitz",  # PyMuPDF - Only external dependency actually used
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
    print("=" * 50)
    
    # Check Python version and platform info
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    print("\n🎉 Setup completed successfully!")
    
    # Provide run instructions based on whether venv was created
    if os.path.exists(".venv"):
        print("\n📋 Next steps:")
        print(f"1. Activate virtual environment: {get_activation_command()}")
        print("2. Run the application: python main.py")
        print("\n💡 Platform-specific notes:")
        if platform.system() == "Windows":
            print("   - Use PowerShell or Command Prompt")
            print("   - You can also use: .venv\\Scripts\\python.exe main.py")
        elif platform.system() == "Darwin":  # macOS
            print("   - Use Terminal")
            print("   - You can also use: .venv/bin/python main.py")
        else:  # Linux and other Unix-like
            print("   - Use any terminal")
            print("   - You can also use: .venv/bin/python main.py")
    else:
        print("You can now run: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
