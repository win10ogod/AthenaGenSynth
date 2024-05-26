import openai
import json
import datetime
import os
from PyQt5 import QtWidgets, QtCore, QtGui

class OpenAIGenerator(QtWidgets.QWidget):
    def __init__(self):
         super().__init__()
         self.initUI()
         self.prompts = []

    def initUI(self):
         self.setWindowTitle("OpenAI Text Generator")
         self.setGeometry(100, 100, 600, 400)

         layout = QtWidgets.QVBoxLayout(self)

         form_layout = QtWidgets.QFormLayout()
         self.api_key = QtWidgets.QLineEdit(self)
         self.api_base = QtWidgets.QLineEdit(self)
         self.api_base.setText("http://127.0.0.1:5000/v1")
         self.model = QtWidgets.QLineEdit(self)
         self.temperature = QtWidgets.QDoubleSpinBox(self)
         self.temperature.setRange(0.0, 1.0)
         self.temperature.setValue(0.5)
         self.temperature.setSingleStep(0.1)
         self.max_tokens = QtWidgets.QSpinBox(self)
         self.max_tokens.setRange(1, 4096)
         self.max_tokens.setValue(100)
         self.output_json = QtWidgets.QCheckBox(self)

         form_layout.addRow("OpenAI API key:", self.api_key)
         form_layout.addRow("API base address:", self.api_base)
         form_layout.addRow("Model name (e.g. 'gpt-4'):", self.model)
         form_layout.addRow("Temperature (0.0-1.0):", self.temperature)
         form_layout.addRow("Maximum number of generated words:", self.max_tokens)
         form_layout.addRow("Output JSON file:", self.output_json)

         layout.addLayout(form_layout)

         btn_load_prompts = QtWidgets.QPushButton("Select prompt file", self)
         btn_generate = QtWidgets.QPushButton("Generate text", self)

         layout.addWidget(btn_load_prompts)
         layout.addWidget(btn_generate)

         self.output_text = QtWidgets.QTextEdit(self)
         self.output_text.setReadOnly(True)
         layout.addWidget(self.output_text)

         btn_load_prompts.clicked.connect(self.load_prompts_from_file)
         btn_generate.clicked.connect(self.generate_data)

    def load_prompts_from_file(self):
         file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
             self, "Select prompt file", "", "Text Files (*.txt);;All Files (*)")
         if file_path:
             with open(file_path, 'r') as file:
                 self.prompts = [line.strip() for line in file.readlines() if line.strip()]
             QtWidgets.QMessageBox.information(self, "Prompt file loading", f"{len(self.prompts)} prompts have been loaded")

    def generate_data(self):
        try:
            openai.api_key = self.api_key.text()
            openai.api_base = self.api_base.text()
            prompts = self.prompts
            model = self.model.text()
            temperature = self.temperature.value()
            max_tokens = self.max_tokens.value()
            output_json = self.output_json.isChecked()

            generated_texts = []
            json_data = []

            for prompt in prompts:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 1,
                    "stop": None,
                    "n": 1
                }

                response = openai.Completion.create(
                    model=model,
                    prompt=payload["prompt"],
                    max_tokens=payload["max_tokens"],
                    temperature=payload["temperature"],
                    top_p=payload["top_p"],
                    n=payload["n"]
                )

                generated_text = response.choices[0].text.strip()
                generated_texts.append(generated_text)

                if output_json:
                    json_data.append({"instruction": prompt, "input": prompt, "output": generated_text})

            if output_json:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                json_file_name = f"generated_texts_{timestamp}.json"
                with open(json_file_name, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                QtWidgets.QMessageBox.information(self, "JSON file saved", f"The generated JSON file has been saved to {json_file_name}")

            if generated_texts:
                output_file = self.create_output_file()
                self.save_to_file(output_file, generated_texts)
                self.output_text.append(f"The generated text has been saved to {output_file}\n")
                self.output_text.append("\n".join(generated_texts) + "\n\n")
            else:
                QtWidgets.QMessageBox.information(self, "Generate results", "No text was generated")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while generating text: {e}")

    def create_output_file(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"generated_texts_{timestamp}.txt"
        return file_name

    def save_to_file(self, file_path, texts):
        try:
            with open(file_path, 'w') as file:
                for text in texts:
                    file.write(f"{text}\n")
        except IOError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error saving file: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = OpenAIGenerator()
    window.show()
    app.exec_()