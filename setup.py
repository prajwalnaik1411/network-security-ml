"""
The setup.py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more
"""

from setuptools import find_packages, setup

# find_packages → Automatically finds all folders with __init__.py
# setuptools → Turns your project into a package
# setup → Main function: defines project name, version, files, etc.

from typing import List

# List[int] → list that should contain only integers
# List[str] → list that should contain only strings


def get_requirements() -> List[str]:  # Reads dependencies from requirements.txt
    requirement_lst: List[str] = []
    # Create empty list to store dependencies (strings)

    try:
        with open("requirements.txt", "r") as file:
            # Opens file in read mode
            # 'with' automatically closes file after use

            lines = file.readlines()
            # Reads all lines into a list

            for line in lines:
                requirement = line.strip()
                # Removes spaces and newline characters
                # Example: "numpy\n" → "numpy"

                # Ignore empty lines and "-e ."
                if requirement and requirement != "-e .":
                    # requirement → ensures line is not empty
                    # requirement != "-e ." → skips editable install command

                    requirement_lst.append(requirement)
                    # Add valid requirement to list

    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst


setup(  # Main configuration block
    name="NetworkSecurity",
    # Project name
    version="0.0.1",
    # Version of the project
    author="Prajwal naik",
    # Author name
    author_email="prajwalnaik820@gmail.com",
    # Author email
    packages=find_packages(),
    # Automatically finds all folders containing __init__.py
    install_requires=get_requirements(),
    # Installs all dependencies from requirements.txt
)


"""
-- pip install . --

Step-by-step:

1. Reads setup.py
2. Finds your packages (find_packages())
3. Runs get_requirements()
4. Installs dependencies
5. Copies your project into Python environment
"""
