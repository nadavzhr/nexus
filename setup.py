"""
Setup configuration for code-editor-widget package.

Professional PyQt5 multi-language code editor widget.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
with open(requirements_path, "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="code-editor-widget",
    version="1.0.0",
    author="Nadav Zhr",
    description="Professional multi-language code editor widget for PyQt5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nadavzhr/nexus",
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Dependencies
    install_requires=requirements,
    python_requires=">=3.7",
    
    # Classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Qt",
        "Operating System :: OS Independent",
    ],
    
    # Keywords
    keywords="pyqt5 code-editor syntax-highlighting text-editor widget ide",
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/nadavzhr/nexus/issues",
        "Source": "https://github.com/nadavzhr/nexus",
        "Documentation": "https://github.com/nadavzhr/nexus/tree/main/docs",
    },
)
