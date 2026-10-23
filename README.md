# GitHub Email Enumerator

A small command-line tool that collects email addresses exposed in a GitHub user's public profile, public events, and commit metadata. It groups Gmail address variants and saves a text report and CSV file.

> **Responsible use:** Use this tool only for your own account or an assessment you are explicitly authorized to perform. Email addresses are personal data. Handle reports securely, follow applicable privacy laws and GitHub's terms, and do not use collected addresses for unsolicited contact or phishing.

## Features

- Checks the public profile email, when available.
- Reads public push events and commit author/committer metadata.
- Scans a specified repository or a limited selection of repositories returned by GitHub for the user.
- Groups Gmail variants by removing dots and `+tags` from the local part and normalizing `googlemail.com` to `gmail.com`.
- Labels GitHub `noreply` addresses and includes available source, name, and login information.
- Writes a human-readable text report and a CSV file.
- Uses Colorama for colored terminal output.

This tool uses data returned by GitHub's API and does not bypass its access controls. API results may depend on the token's permissions; only provide a token and repository for data you are authorized to access. Results are limited to the data and scan limits described below; they are not an exhaustive history.

## Requirements

- Python 3.8 or newer

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run interactively:

```bash
python main.py
```

The program prompts for a GitHub username, an optional repository URL or `owner/repo`, and an optional GitHub token.

Arguments can also be supplied in this order:

```text
python main.py <username> [repository] [token]
```

For example, to scan a repository you own or are authorized to assess:

```bash
python main.py <your-github-username> <owner/repository>
```

To pass a token without specifying a repository, leave the repository argument empty:

```bash
python main.py <your-github-username> "" <your-token>
```

A token is optional. For better secrecy, prefer the interactive prompt instead of putting a token in a command, where it may be saved in shell history or visible to other local processes.

## Scan limits

The default limits are defined in [`nya/settings.py`](nya/settings.py):

- **User scan:** up to 3 pages of public events, and up to 15 recently pushed repositories returned by GitHub, with up to 2 commit pages per repository.
- **Repository scan:** up to 5 commit pages for the specified repository.
- Each API page requests up to 100 items.

These limits are intended to keep scans bounded. GitHub API rate limits may restrict results, especially for unauthenticated requests.

## Output

The report files are saved in the current working directory:

```text
github_gmail_enum_<username>.txt
github_gmail_enum_<username>.csv
```

The text report groups addresses into Gmail, GitHub `noreply`, and other email sections. The CSV includes the email type, observed names and logins, sources, occurrence count, and target-match count.

## Project layout

```text
main.py             Command-line entry point
nya/                Application modules
requirements.txt    Python dependencies
```
