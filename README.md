# AI Password Security Analyzer

This is a Python project I made that checks password strength using different security checks and the OpenAI API. It looks at things like password length, common passwords, and predictable patterns, then gives a score and explains what could be improved.

I also deployed it to AWS EC2 to get some experience working with Linux and cloud services.

## About the Project

I made this project because I wanted to get more experience with Python while also learning more about cybersecurity. I wanted to make something that did more than just check if a password had a capital letter, number, or special character.

The program checks passwords for different weaknesses, including repeated characters, common passwords, and number or letter sequences. It uses these checks to give the password a score from 0–6 and rates it as Weak, Fair, Strong, or Very Strong.

I also used the OpenAI API to give more detailed feedback about the password and explain what could make it stronger.

## Features

- Checks password length and character types
- Detects common passwords from a built-in list
- Checks for repeated characters and predictable sequences
- Gives a password strength score from 0–6
- Rates passwords as Weak, Fair, Strong, or Very Strong
- Uses the OpenAI API to explain weaknesses and suggest improvements
- Hides the password while typing in the terminal
- Can still run the local checks without the OpenAI API

## Technologies Used

- **Python:** Used to build the program and run the password checks
- **OpenAI API:** Used to explain the results and give recommendations
- **Regex:** Used to find repeated characters and predictable patterns
- **AWS EC2:** Used to run the program on a cloud server
- **Amazon Linux 2023:** Operating system used on the EC2 instance
- **Git/GitHub:** Used to store and manage the code
- **SSH:** Used to connect to the EC2 instance

## How It Works

1. The user enters a password in the terminal.
2. The program checks the password locally using Python.
3. It calculates a score based on the checks and displays the results.
4. The results are sent to the OpenAI API for additional feedback.
5. The AI explains what could be improved, and the user can try another password.

The actual password isn't sent to OpenAI. Only the results from the local checks are sent.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Jrxuu/AI-Password-Security-Analyzer.git
```

### 2. Open the project folder

```bash
cd AI-Password-Security-Analyzer
```

### 3. Install the OpenAI library

Make sure Python is installed, then run:

```bash
python -m pip install openai
```

### 4. Set your OpenAI API key

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

**Linux/macOS:**

```bash
export OPENAI_API_KEY="your-api-key"
```

The program can still check passwords without an API key, but it won't give AI feedback.

### 5. Run the program

```bash
python "AI Password Checker Full.py"
```

Run it in a terminal rather than the PyCharm Run console so the hidden password input works properly.

## AWS EC2 Deployment

After finishing the Python program, I wanted to try running it on AWS instead of only on my computer. I used Amazon EC2 with Amazon Linux 2023 to get some practice with cloud computing and Linux.

I created an EC2 instance and connected to it using SSH from my computer. I also had to configure the security group to allow SSH traffic from my public IPv4 address.

At first, I was having trouble connecting because the security group was using an IPv6 address while I was trying to connect using IPv4. After fixing the inbound rule, I was able to connect.

Once I got into the instance, I installed Python and Git, cloned my GitHub repository, and set up a virtual environment for the OpenAI library. I also configured the API key as an environment variable so I wouldn't have to put it directly into the code.

The program now runs through the Linux terminal on EC2. Since it isn't a website, I only needed SSH access and left the HTTP and HTTPS ports closed.

### Running on EC2

After connecting to the instance through SSH:

```bash
cd ~/AI-Password-Security-Analyzer
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Set the OpenAI API key for the current session:

```bash
read -rsp "Enter your OpenAI API key: " OPENAI_API_KEY
echo
export OPENAI_API_KEY
```

Run the program:

```bash
python "AI Password Checker Full.py"
```

## Security Considerations

One thing I learned while working on this was that sending the actual password to the OpenAI API wasn't a good idea. I changed the program so it analyzes the password locally and only sends the results to the API.

I also used `getpass` so the password doesn't appear while someone types it, and I kept my API key in an environment variable instead of putting it in the Python file.

For AWS, I restricted SSH access to my public IP instead of allowing traffic from anywhere.

The program uses my own scoring system and a small list of common passwords, so it isn't meant to be a complete password security tool. It also doesn't check whether a password has been found in a data breach. It's mainly a project I made to practice Python and learn more about security, so it should be tested with sample passwords rather than real credentials.

## What I Learned

This project helped me get more comfortable with Python, especially using functions, dictionaries, regex, and working with APIs.

I also got a better understanding of how password security works. Before making this, I mainly thought about password strength in terms of length and character requirements. While working on it, I learned that a password can still be predictable even if it has numbers, capital letters, and special characters.

The AWS deployment was also useful because I hadn't done much with EC2 before. I learned how to connect to a Linux server using SSH, set up security group rules, install dependencies, and pull code from GitHub.

## Future Improvements

There are still some things I'd like to improve if I come back to this project:

- Add breached-password detection using the Have I Been Pwned API
- Improve the password scoring system
- Add automated tests
- Make a web interface instead of only using the terminal

## Author

**Julian Bolton**

Computer Science & Mathematics  
Virginia Tech
