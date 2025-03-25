To set up a virtual environment in **VS Code on Windows PC** and install all packages from the `requirements.txt` file, follow these steps:

---

## **1. Open Your Project in VS Code**
1. Launch **VS Code**.
2. Open the terminal in VS Code using:
   - **Shortcut**: `Ctrl + `` (backtick)`
   - Or go to **View → Terminal**.

---

## **2. Create a Virtual Environment**
In the VS Code terminal, navigate to your project folder:
```bash
cd C:\path\to\your\project
```
Then, create a virtual environment using:
```bash
python -m venv venv
```
This creates a folder called `venv` inside your project directory.

---

## **3. Activate the Virtual Environment**
Run the following command to activate the virtual environment:
```bash
venv\Scripts\activate
```
Once activated, you should see `(venv)` appear at the beginning of your terminal prompt.

---

## **4. Install Packages from `requirements.txt`**
If you already have a `requirements.txt` file, install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## **5. Configure VS Code to Use the Virtual Environment**
1. Open the **Command Palette** (`Ctrl + Shift + P`).
2. Search for and select **"Python: Select Interpreter"**.
3. Choose the Python interpreter inside your virtual environment. It should look like:
   ```
   C:\path\to\your\project\venv\Scripts\python.exe
   ```
4. Restart VS Code to apply changes.

---

## **6. Verify Installation**
To check if the installed packages are available, run:
```bash
pip list
```

---

## **7. Deactivate the Virtual Environment**
When you're done, deactivate the virtual environment using:
```bash
deactivate
``` 
