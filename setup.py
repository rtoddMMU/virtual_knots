from setuptools import setup, find_packages

setup(
    name="vkt",
    version="0.2.0",
    author="Robert Todd",
    description="Virtual Knot Theory: Computing gl(n|m) invariants",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "sympy>=1.12",
        "networkx>=3.0",
        "pandas>=2.0.0",
        "joblib>=1.3.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0", "jupyter>=1.0.0"],
    },
)