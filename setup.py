import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="azapyGUI",
    version="0.0.1",
    author="Mircea Marinescu",
    author_email="mircea.marinescu@outlook.com",
    description="GUI for azapy library - Financial Portfolio Optimization Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mircea-MMXXI/azapyGUI.git",
    project_urls={
        "Documentation": "https://azapyGUI.readthedocs.io/en/latest",
        "Source": "https://github.com/Mircea-MMXXI/azapyGUI",
        "Bug Tracker": "https://github.com/Mircea-MMXXI/azapyGUI/issues",
    },
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
    install_requires=[
          'azapy',
          'numpy',
          'pandas',
          'matplotlib',
          'xlsxwriter'
    ],
)
