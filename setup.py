from setuptools import setup, find_packages

setup(
    name="repo2prompt",
    version="0.1.0",
    description="A lightweight CLI tool to convert GitHub repositories and local directories into LLM context prompts.",
    author="Viral",
    url="https://github.com/yourusername/repo2prompt",
    packages=find_packages(),
    install_requires=[
        "pathspec>=0.12.0",
        "GitPython>=3.1.0",
        "tiktoken>=0.6.0",
    ],
    entry_points={
        "console_scripts": [
            "repo2prompt=repo2prompt.main:main",
        ],
    },
    python_requires=">=3.8",
)
