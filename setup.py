from setuptools import setup, find_namespace_packages

setup(
    name="chemcharts",
    maintainer="Sophie Margreitter, Christian Margreitter",
    version="0.5.1",
    url="https://github.com/SMargreitter/ChemCharts",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    description="ChemCharts: Chemical Space Visualizer",
    python_requires=">=3.7",
    entry_points={"console_scripts": ["chemcharts_cli = chemcharts.scripts.chemcharts_cli:main",
                                      "chemcharts = chemcharts.scripts.chemcharts_json:main"]},
)
