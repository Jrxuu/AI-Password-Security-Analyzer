
"""
Julian Bolton

AI Password Security Analyzer
Analyzes password strength using local Python security checks
and the OpenAI API to provide security recommendations.

Nov 2026
"""

import os
import re
import json
import getpass
from openai import OpenAI


# Common passwords used for basic local detection
COMMON_PASSWORDS = {
    "password",
    "password1",
    "password123",
    "passw0rd",
    "123456",
    "1234567",
    "12345678",
    "123456789",
    "1234567890",
    "123123",
    "111111",
    "000000",
    "qwerty",
    "qwerty123",
    "letmein",
    "welcome",
    "welcome123",
    "admin",
    "admin123",
    "abc123",
    "iloveyou",
    "monkey",
    "dragon",
    "football",
    "baseball",
    "trustno1"
}


def analyze_password(password):
    """
    Analyze password characteristics locally.
    No password information is sent to an external service.
    """

    score = 0
    warnings = []

    # Password length
    length = len(password)

    if length >= 20:
        score += 6
    elif length >= 16:
        score += 5
    elif length >= 12:
        score += 4
    elif length >= 8:
        score += 2
    else:
        warnings.append(
            "Password is too short. Consider using 15 or more characters."
        )

    # Character checks
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    character_types = sum([
        has_lowercase,
        has_uppercase,
        has_number,
        has_special
    ])

    # Character variety is a bonus, not a requirement
    if character_types >= 2:
        score += 1

    # Common passwords
    normalized_password = re.sub(
        r"[^a-z0-9]", "", password.lower()
    )

    is_common = normalized_password in COMMON_PASSWORDS

    if is_common:
        warnings.append(
            "This password is commonly used and easily guessed."
        )

    # Predictable words
    predictable_words = [
        "password",
        "qwerty",
        "letmein",
        "admin",
        "welcome"
    ]

    has_predictable_word = any(
        word in normalized_password
        for word in predictable_words
    )

    if has_predictable_word and not is_common:
        score -= 2
        warnings.append(
            "Password contains a predictable word or pattern."
        )

    # Repeated characters
    has_repeated_characters = bool(
        re.search(r"(.)\1{2,}", password)
    )

    if has_repeated_characters:
        score -= 2
        warnings.append(
            "Avoid repeating the same character multiple times."
        )

    # Predictable number sequences
    number_sequences = [
        "123", "234", "345", "456",
        "567", "678", "789",
        "987", "876", "765", "654",
        "543", "432", "321"
    ]

    has_number_sequence = any(
        sequence in password
        for sequence in number_sequences
    )

    if has_number_sequence:
        score -= 1
        warnings.append(
            "Avoid predictable number sequences."
        )

    # Predictable letter sequences
    letter_sequences = [
        "abc", "bcd", "cde", "def",
        "qwe", "asd", "zxc"
    ]

    has_letter_sequence = any(
        sequence in password.lower()
        for sequence in letter_sequences
    )

    if has_letter_sequence:
        score -= 1
        warnings.append(
            "Avoid predictable letter or keyboard sequences."
        )

    # Common passwords always receive the lowest score
    if is_common:
        score = 0

    # Keep score between 0 and 6
    score = max(0, min(score, 6))

    # Strength classification
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Fair"
    elif score == 5:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "length": length,
        "has_uppercase": has_uppercase,
        "has_lowercase": has_lowercase,
        "has_number": has_number,
        "has_special": has_special,
        "is_common": is_common,
        "score": score,
        "strength": strength,
        "warnings": warnings
    }


def get_ai_assessment(analysis):
    """
    Request AI security recommendations.

    Only local analysis results are sent to OpenAI.
    The actual password is never transmitted.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "AI assessment unavailable.\n"
            "Set OPENAI_API_KEY to enable AI feedback."
        )

    client = OpenAI(api_key=api_key)

    # Safe summary contains no actual password
    analysis_summary = json.dumps(analysis, indent=2)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cybersecurity educator. "
                    "Explain password security in simple language. "
                    "Use only the supplied local analysis results. "
                    "Do not claim that breach databases were checked. "
                    "Do not provide exact password cracking times. "
                    "Give a short assessment and 2-3 practical "
                    "recommendations. Do not request the password."
                )
            },
            {
                "role": "user",
                "content": (
                    "Assess the following password security results. "
                    "The actual password is intentionally withheld.\n\n"
                    + analysis_summary
                )
            }
        ]
    )

    return response.choices[0].message.content or (
        "No AI assessment was returned."
    )


def display_results(analysis):
    """
    Display local password security analysis.
    """

    print("\n" + "=" * 45)
    print("PASSWORD SECURITY ANALYSIS")
    print("=" * 45)

    print(f"Length:              {analysis['length']}")

    print(
        "Uppercase letters:   "
        + ("Yes" if analysis["has_uppercase"] else "No")
    )

    print(
        "Lowercase letters:   "
        + ("Yes" if analysis["has_lowercase"] else "No")
    )

    print(
        "Numbers:             "
        + ("Yes" if analysis["has_number"] else "No")
    )

    print(
        "Special characters:  "
        + ("Yes" if analysis["has_special"] else "No")
    )

    print(f"\nLocal strength: {analysis['strength']}")
    print(f"Score: {analysis['score']}/6")

    if analysis["warnings"]:
        print("\nWarnings:")

        for warning in analysis["warnings"]:
            print(f"- {warning}")
    else:
        print("\nNo obvious weaknesses detected.")

    print("\nNote: This is a basic heuristic assessment.")
    print("It is not a comprehensive security or breach check.")

    print("=" * 45)


def main():
    """
    Main program loop.
    """

    print("=" * 45)
    print("AI PASSWORD STRENGTH CHECKER")
    print("=" * 45)

    print("\nAnalyze password strength using Python and AI.")
    print("Password input is hidden for privacy.")
    print("The actual password is not sent to OpenAI.")
    print("\nUse a test password, not a real credential.")

    while True:


        password = input(
            "\nEnter a TEST password to analyze: "
        )

        # Run local checks
        analysis = analyze_password(password)

        # Display local results
        display_results(analysis)

        # AI assessment
        print("\nAI Assessment:")
        print("-" * 45)

        try:
            ai_result = get_ai_assessment(analysis)
            print(ai_result)

        except Exception:
            print("Unable to contact the AI service.")
            print("Local password analysis is still available.")
            print("Check your API key and network connection.")

        # Ask whether to analyze another password
        while True:

            choice = input(
                "\nAnalyze another password? (Y/N): "
            ).strip().upper()

            if choice == "Y":
                break

            elif choice == "N":
                print("\nThank you for using the password checker!")
                return

            else:
                print("Please enter Y or N.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram exited.")
