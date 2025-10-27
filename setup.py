#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, Extension, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

# Force Clang compiler
os.environ["CC"] = "clang"
os.environ["CXX"] = "clang++"
os.environ["LD"] = "clang"

# Extreme optimization flags for Clang targeting your specific CPU
compile_flags = [
    # Aggressive optimization levels
    "-O3",
    "-ffast-math",
    "-fstrict-aliasing",
    "-funroll-loops",
    "-finline-functions",
    
    # Advanced LTO and inlining (Full LTO for maximum optimization)
    "-flto",  # Full LTO - small project, worth the compile time
    "-fwhole-program-vtables",
    "-fvisibility=hidden",
    "-fvisibility-inlines-hidden",
    
    # CPU-specific optimization - use native for auto-detection
    "-march=native",
    "-mtune=native",
    
    # Explicitly enable crypto-relevant instructions
    "-maes",           # AES-NI instructions (critical for crypto!)
    "-mvpclmulqdq",    # PCLMULQDQ for GCM mode (note: 'v' prefix!)
    "-mavx2",          # AVX2 for SIMD
    "-mbmi2",          # Bit manipulation
    "-mrdseed",        # Random seed instruction
    "-madx",           # Multi-precision arithmetic
    
    # Loop and vector optimization
    "-fvectorize",
    "-fslp-vectorize",
    "-fno-math-errno",
    
    # Security and performance
    "-DNDEBUG",
    "-fstack-protector-strong",
    "-fomit-frame-pointer",
    
    # LLVM-specific optimizations for crypto workloads
    "-mllvm", "-enable-loop-distribute",
    "-mllvm", "-enable-interleaved-mem-accesses",
    "-mllvm", "-unroll-threshold=1000",  # More aggressive unrolling
    "-mllvm", "-inline-threshold=1000",   # More aggressive inlining
]

link_flags = [
    # LTO and optimization (Full LTO)
    "-flto",
    "-O3",
    
    # CPU-specific
    "-march=native",
    
    # Linker optimization
    "-Wl,--gc-sections",
    "-Wl,--as-needed",
    "-Wl,--icf=all",
    "-Wl,-O3",
    "-Wl,--lto-O3",
    
    # Strip unnecessary symbols
    "-Wl,--strip-all",
    
    # Additional linker optimizations
    "-Wl,--build-id=none",  # Skip build ID for smaller size
]

setup(
    name="TgCrypto",
    version="1.2.5",
    description="Fast and Portable Cryptography Extension Library for Pyrogram",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pyrogram",
    download_url="https://github.com/pyrogram/tgcrypto/releases/latest",
    author="Dan",
    author_email="dan@pyrogram.org",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="pyrogram telegram crypto cryptography encryption mtproto extension library aes",
    project_urls={
        "Tracker": "https://github.com/pyrogram/tgcrypto/issues",
        "Community": "https://t.me/pyrogram",
        "Source": "https://github.com/pyrogram/tgcrypto",
        "Documentation": "https://docs.pyrogram.org",
    },
    python_requires="~=3.9",
    packages=find_packages(),
    test_suite="tests",
    zip_safe=False,
    ext_modules=[
        Extension(
            "tgcrypto",
            sources=[
                "tgcrypto/tgcrypto.c",
                "tgcrypto/aes256.c",
                "tgcrypto/ige256.c",
                "tgcrypto/ctr256.c",
                "tgcrypto/cbc256.c"
            ],
            extra_compile_args=compile_flags,
            extra_link_args=link_flags
        )
    ]
)
