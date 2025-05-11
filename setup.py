from setuptools import setup, find_packages

setup(
    name="filmfinder",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'streamlit-option-menu',
        'streamlit-extras',
        'pandas',
        'nltk',
        'scikit-learn',
        'requests'
    ],
) 