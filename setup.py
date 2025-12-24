from setuptools import setup, find_packages

setup(
    name="nexora",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "scikit-learn",
        "fastapi",
        "uvicorn",
        "jinja2",
        "python-multipart",
        "joblib"
    ],
)
