test_choices = [
    {
        "name": 'Add project to portfolio site',
        "prompt": """I just created a new project! It is called Tiny Gen. Is it possible to add this project to portfolio site? Tiny Gen is basically an application that can add code to a repository given a user prompt. Basically, you give a repoUrl and the prompt, Tiny Gen is able to locate the file to modify and modifies it! It then returns a unified diff showing the correct changes. I'll upload the links, images and other information later.
            """,
        "repoUrl": "https://github.com/tawsifkamal/portfolio-site"
     },
     {
        "name": 'Make LLM.sh work with windows',
        "prompt": r""" 
             The program doesn't output anything in windows 10.
        (base) C:\Users\off99\Documents\Code\>llm list files in current dir; windows
        / Querying GPT-3200
        ───────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────
            │ File: temp.sh
        ───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        1   │
        2   │ dir
        3   │ ```
        ───────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        >> Do you want to run this program? [Y/n] y

        Running...


        (base) C:\Users\off99\Documents\Code\>
        Notice that there is no output. Is this supposed to work on Windows also?
        Also it might be great if the script detects which OS or shell I'm using and try to use the appropriate command e.g. dir instead of ls because I don't want to be adding windows after every prompt.
            """,
        "repoUrl": "https://github.com/jayhack/llm.sh"
     },
     {
        "name": 'Convert calculator.js app to Typescript',
        "prompt": """
            convert project to typescript
            """,
        "repoUrl": "https://github.com/andrewagain/calculator"
     }
]