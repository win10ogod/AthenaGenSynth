\[ English | [中文](README-CN.md) \]

![image](image.png)。

#AthenaGen
Generate data using OLLAMA
and use a simple script to create a pre-training data set

# how to use
Refer to how to use ollama serve to start the api.

Run pythonSynth.py

Enter the ollama model you want to use.

To enter prompts, enter done to end manual prompt entry, or place one prompt per line in the txt file.
# alltxttojson.py
Modify data=""

For example:

txt is stored in ./cleaned3

data="./cleaned3"

Run python alltxttojson.py

You will get the data{}.json file
