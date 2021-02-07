from setuptools import find_packages
from setuptools import setup


try:
    README = open("README.md").read()
except IOError:
    README = None

setup(
    name="mahjong_sample_web_app",
    version="0.1.0",
    description="Mahjong Sample Web APP",
    long_description=README,
    install_requires=[
        "Flask",
        # "jsonschema",
        # "flask-cors",
        "Jinja2",
        "mahjong",
        "uWSGI",
        "pillow",
        "numpy",
        # "scipy",
        "keras",
        # "tensorflow",
    ],
    author="Manabu TERADA",
    author_email="terada@cmscom.jp",
    url="",
    packages=find_packages(include=["mahjong_sample_web_app"]),
    include_package_data=True,
    tests_require=["pytest", "black"],
    extras_require={"test": ["pytest"]},
    classifiers=[],
    entry_points={},
)
