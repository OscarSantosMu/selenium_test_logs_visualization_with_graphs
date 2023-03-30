from setuptools import setup, find_packages

setup(
    name="lambdatest-logsviz",
    version="1.0",
    description="My GitHub Octernship assignment",
    author="Oscar Santos",
    author_email="oscarsantosmu@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    license_files=("LICENSE",),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy",
        "pandas",
        "Flask",
        "Flask-Caching",
        "plotly",
        "selenium",
        "webdriver-manager",
        "python-dotenv",
        "elasticsearch",
        "pdoc",
    ],
)
