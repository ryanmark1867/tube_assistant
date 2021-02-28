## tube_assistant

Harness to exercise simple GPT-3 applications.

- data: contains CSV files for prompts (used to define examples used to define the gpt object) and tests (test inputs to exercise the application)



* **tube_assistant.py** - main Python module
* **tube_assistant_config.yml**  - config file. **NOTE** for the code to work, you need to set the value of gpt_key in this file to set your own SECRET key from https://beta.openai.com/developer-quickstart
* **git.py** - required GPT-3 classes

More background:
- article: https://towardsdatascience.com/on-the-tube-with-gpt-3-6f9572e88292
- videos: https://www.youtube.com/watch?v=790PiTSqi4Y https://youtu.be/Xzb1Vc8dYAY
