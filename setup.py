"""
Setup configuration for NEXORA AI.

This file provides backward compatibility with older build systems.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nexora-ai",
    version="0.1.0",
    author="NEXORA AI Team",
    description="A modular, local-first Enterprise Intelligence Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/K-vino/nexora-ai",
    project_urls={
        "Bug Tracker": "https://github.com/K-vino/nexora-ai/issues",
        "Documentation": "https://github.com/K-vino/nexora-ai/blob/main/README.md",
        "Source Code": "https://github.com/K-vino/nexora-ai",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        # No external dependencies for the scaffold
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "ruff>=0.0.285",
            "mypy>=1.5.0",
        ],
    },
    zip_safe=False,
)
