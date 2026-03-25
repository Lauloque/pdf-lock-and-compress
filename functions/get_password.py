from constants import PASSWORD_FILE


def get_password() -> str:
    """Return the owner password from the secrets file, creating it if needed."""
    if PASSWORD_FILE.exists():
        password = PASSWORD_FILE.read_text(encoding="utf-8").strip()
        if password:
            return password
        print(f"⚠ '{PASSWORD_FILE.name}' exists but is empty.")

    # file missing or empty: ask the user
    print(f"No password found in '{PASSWORD_FILE.name}'.")
    while True:
        password = input("Enter an owner password to use for protected PDFs: ").strip()
        if password:
            break
        print("  Password cannot be empty, please try again.")

    PASSWORD_FILE.write_text(password, encoding="utf-8")
    print(f"✅ Password saved to '{PASSWORD_FILE.name}' (excluded from git).\n")
    return password
