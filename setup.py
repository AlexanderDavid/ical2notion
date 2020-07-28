from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "click==7.1.2",
    "requests==2.24.0",
    "notion==0.0.25",
    "ics==0.7"
]

setup(
    name="ical2notion",
    version="0.1.0",
    url="https://github.com/AlexanderDavid/ical2notion",
    license="MIT",
    author="Alex Day",
    author_email="alexday135@gmail.com",
    description="iCal to Notion made simple",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=dependencies,
    entry_points={"console_scripts": ["ical2notion = ical2notion:ical2notion",],},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Organization :: Workflow",
    ],
)

