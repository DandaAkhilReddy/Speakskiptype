"""
Setup script for SpeakSkipType.
"""

from setuptools import setup, find_packages

setup(
    name="speakskiptype",
    version="1.0.0",
    description="Speech-to-Text directly in your terminal - No API, 100% FREE, Works Locally",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/DandaAkhilReddy/Speakskiptype",
    py_modules=["speakskiptype"],
    install_requires=[
        "vosk>=0.3.45",
        "sounddevice>=0.4.6",
        "pynput>=1.7.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "numpy>=1.20.0",
        ],
    },
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "speakskiptype=speakskiptype:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
)
