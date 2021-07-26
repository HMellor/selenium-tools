import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="selenium-tools",
        version="1.0.0",
        author="HMellor",
        description="Tools to speed using Selenium",
        url="https://github.com/HMellor/selenium-tools",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.8",
        install_requires=[
            "yarl",
            "selenium",
            "chromedriver-py",
        ],
    )
