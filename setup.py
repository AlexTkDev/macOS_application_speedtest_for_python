from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="macOS_speedtest",
    version="2.0.1",
    author="Aleksandr",
    author_email="yourmail@example.com",
    description="A macOS application to test internet connection speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexTkDev/macOS_application_speedtest_for_python",
    project_urls={
        "Bug Tracker": "https://github.com/AlexTkDev/macOS_application_speedtest_for_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "speedtest-cli>=2.1.3",
        "matplotlib>=3.5.0",
        "psutil>=5.9.0",
        "pyinstaller>=5.6.0",
    ],
    entry_points={
        "console_scripts": [
            "alex-speedtest=alex_speedtest:main",
        ],
    },
    include_package_data=True,
)