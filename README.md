# Resume Analyzer

This is a guide on how to use and modify the Resume Analyzer application. The application uses OpenAI's GPT-3 model to analyze resumes and generate a set of questions based on the resume content.

## How to Use

1. Run the application.
2. Upload a PDF or DOCX file of a resume using the file uploader.
3. Wait for the analysis to complete.
4. The analysis result will be displayed on the left side of the screen, and the uploaded resume will be displayed on the right side.

## How to Change the OpenAI Model

The OpenAI model used in this application is specified in the `analyze_with_openai` function. To change the model, follow these steps:

1. Locate the `analyze_with_openai` function in the `rs/app_modified.py` file.
2. Find the line where the `model` variable is defined. The line should look like this: `model = "gpt-3.5-turbo-16k"`.
3. Replace `"gpt-3.5-turbo-16k"` with the name of the desired model. For example, if you want to use the `text-davinci-002` model, the line should look like this: `model = "text-davinci-002"`.

## How to Change the Prompt

The prompt used in this application is specified in the `analyze_with_openai` function. To change the prompt, follow these steps:

1. Locate the `analyze_with_openai` function in the `rs/app_modified.py` file.
2. Find the line where the `messages` list is defined. The line should look like this: `messages = [{...}, {...}]`.
3. The second dictionary in the `messages` list contains the prompt. The line should look like this: `{"role": "user", "content": text}`.
4. Replace `text` with the desired prompt. For example, if you want the prompt to be "Please analyze this resume", the line should look like this: `{"role": "user", "content": "Please analyze this resume"}`.

Please note that changing the prompt or the model may affect the performance of the application. It is recommended to have a basic understanding of how OpenAI's GPT-3 works before making these changes.
