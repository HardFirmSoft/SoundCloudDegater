import setuptools

with open("README.md", "r") as file:
    readme = file.read()
setuptools.setup(
    name="soundcloud_degater",
    version="0.0.1",
    description="Download from SoundCloud in the best quality, regardless of gates.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/noahbaxter/SoundCloudDegater",
    packages=["soundcloud_degater"],
    install_requires=[
        'soundcloud',
        'selenium',
        'click',
    ],
    entry_points='''
        [console_scripts]
        scdegater=soundcloud_degater.main:cli
    '''
)
