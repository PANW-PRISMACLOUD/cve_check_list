# `cve_list_check` 🚀

Welcome to the `cve_list_check` project! 🎉 This program fetches Common Vulnerabilities and Exposures (CVEs) from the Prisma Cloud CVE Viewer, checks their alignment with intelligence streams, and preserves the CVE details in a neatly organized `cve_details.json` file. But hold on, there's more! 🌟

## How to Use the Program

Using `cve_list_check` is a straightforward process. Simply follow these steps:

### **Step 1: Prerequisites 🛠️**

Ensure that you have the following prerequisites in place:

- **Python 🐍**: Make sure Python is installed on your system. If it's not already installed, you can download it from the official website [here](https://www.python.org/downloads/).

- **Configuration File 📜**: Create a configuration file named `config.json` with the necessary settings. Customize these options to suit your specific requirements.

### **Step 2: Installation 📦**

To install the required Python packages, navigate to the project directory and execute the following command:

```bash
pip install -r requirements.txt
```

This command will magically summon all the essential dependencies, including the mighty `pydantic`, the versatile `dotenv`, and more.

### **Step 3: Configuration ⚙️**

Edit the `config.json` file with your specific configuration settings. The configuration covers crucial options like `auth_key`, `jwt_token`, `api_base_url`, and more. Ensure that you provide the necessary values for seamless authentication and access to the Prisma Cloud CVE Viewer.

### **Step 4: Running the Program 🚀**

Prepare for takeoff! To launch the program, execute the following command in your terminal:

```bash
python main.py
```

The program orchestrates a series of actions:

- 🔄 Loads the configuration from `config.json`, environment variables, and command-line arguments.

- 🚀 Initializes the CVE Fetcher with the provided configuration.

- 📃 Loads the list of CVEs to be fetched from `cve_list.json`.

- 🌐 Fetches the details of the CVEs from the Prisma Cloud CVE Viewer.

- 💾 Saves the fetched CVE details to a `cve_details.json` file.

- 📊 Provides comprehensive logging information and statistics concerning the fetched CVEs.

### **Step 5: Reviewing the Results 🕵️‍♀️**

Once the program completes its mission, it's time to examine the outcomes:

- Open the `cve_details.json` file to delve into the rich trove of CVE details.

- Peruse the program's log for valuable insights about the process and enlightening statistics related to the fetched CVEs.

That's it! You've successfully harnessed the power of the `cve_list_check` program to acquire and process CVE data from the Prisma Cloud CVE Viewer. Don't hesitate to tailor the program's configuration to your specific needs.

## Key Components

### **`config.py` ⚙️**

- Defines a `Config` class responsible for managing configuration loading from various sources, including environment variables, command-line arguments, and configuration files.

- Utilizes Pydantic for configuration validation, while neatly organizing configuration keys, flags, and their corresponding descriptions.

### **`cve_fetcher.py` 🌐**

- Implements a `CVEFetcher` class that excels at retrieving CVE details from the Prisma Cloud CVE Viewer.

- Leverages the configuration provided in `config.py` for streamlined authentication and CVE data retrieval.

### **`file_utils.py` 📂**

- Hosts utility functions dedicated to file operations, including:

  - `load_cve_list`: A magical function to load a list of CVEs from a file.

  - `save_cve_details`: An enchanting function for saving CVE details to a JSON file.

### **`main.py` 🚀**

- Serves as the project's primary entry point.

- In the spotlight of `main.py`:

  - Artfully loads the configuration settings.

  - Elegantly initializes the `CVEFetcher`.

  - Gracefully loads the list of CVEs to be fetched.

  - Precisely fetches CVE details.

  - Stylishly saves the results in a JSON file.

## Additional Information

For more details on how to customize and extend the functionality of the `cve_list_check` program, refer to the source code and comments within each file. Happy coding! 🎉
