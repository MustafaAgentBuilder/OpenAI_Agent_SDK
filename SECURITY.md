# Security Guidelines

## API Key Management

This repository contains examples that require API keys. Follow these security best practices:

### 1. Never commit API keys to version control
- API keys should never be committed to Git
- Use `.env` files for local development (these are ignored by Git)
- Use environment variables in production

### 2. Setting up API keys

Each project directory contains a `.env.example` file. To set up your API keys:

1. Copy the `.env.example` file to `.env` in the same directory
2. Replace the placeholder values with your actual API keys
3. The `.env` file will be ignored by Git automatically

Example:
```bash
# In any project directory
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Required API Keys

Different examples require different API keys:

- **GEMINI_API_KEY**: Google Gemini API key (get from Google AI Studio)
- **GROQ_API_KEY**: Groq API key (get from Groq Console)
- **OPENAI_API_KEY**: OpenAI API key (get from OpenAI Platform)

### 4. Environment Variables

You can also set environment variables instead of using `.env` files:

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### 5. Security Best Practices

- Regularly rotate your API keys
- Use separate API keys for development and production
- Monitor API key usage in your provider's dashboard
- Never share API keys in chat, email, or other communication
- Use API key restrictions when available (IP restrictions, etc.)

### 6. If You Accidentally Commit an API Key

If you accidentally commit an API key:

1. **Immediately revoke the key** in your API provider's dashboard
2. Remove the key from Git history using `git filter-branch` or `git filter-repo`
3. Generate a new API key
4. Update your local `.env` file with the new key

### 7. Production Deployment

For production deployments:

- Use your platform's secret management (AWS Secrets Manager, Azure Key Vault, etc.)
- Set environment variables in your deployment platform
- Never include `.env` files in production builds
- Use CI/CD secrets for automated deployments

## Reporting Security Issues

If you find security vulnerabilities in this repository, please report them responsibly by contacting the maintainers directly rather than opening public issues.
