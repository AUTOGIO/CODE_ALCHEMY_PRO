"""
CODE_ALCHEMY Professional Setup
AI-Powered Desktop Intelligence System
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="code-alchemy-pro",
    version="2.0.0",
    author="AUTOGIO",
    author_email="tech@alchemist-ai-labs.com",
    description="AI-Powered Desktop Intelligence System for Apple Silicon M3",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/AUTOGIO/CODE_ALCHEMY_PRO",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "code-alchemy=src.web.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.json", "*.md"],
    },
    keywords="ai, automation, desktop, organization, productivity, m3, apple-silicon",
    project_urls={
        "Bug Reports": "https://github.com/AUTOGIO/CODE_ALCHEMY_PRO/issues",
        "Source": "https://github.com/AUTOGIO/CODE_ALCHEMY_PRO",
        "Documentation": "https://github.com/AUTOGIO/CODE_ALCHEMY_PRO/docs",
    },
) 