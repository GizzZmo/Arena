# Contributing to Arena

First off, thank you for considering contributing to Arena! This project thrives on community involvement, whether you're fixing bugs, adding features, improving documentation, or sharing training data.

## 🤝 Ways to Contribute

### 1. Code Contributions
- Bug fixes
- New features
- Performance optimizations
- Test coverage improvements
- Code refactoring

### 2. Documentation
- Improve README or ROADMAP
- Add code comments
- Create tutorials or guides
- Fix typos or clarify instructions
- Add architecture diagrams

### 3. Data Contributions
- Run games and share training data
- Share fine-tuning results
- Document interesting game patterns
- Performance benchmarks

### 4. Testing & Feedback
- Report bugs
- Test on different platforms (Windows/Mac/Linux)
- Suggest improvements
- Share use cases

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git installed on your system
- Stockfish chess engine
- Google Gemini API key (for testing AI features)

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Arena.git
   cd Arena
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install python-chess google-generativeai
   ```

5. **Configure the application:**
   - Copy `cyberchess.py` and update `STOCKFISH_PATH` and `GOOGLE_API_KEY`
   - Never commit your actual API keys!

6. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Keep functions focused and single-purpose

### Documentation
- Update README.md if adding user-facing features
- Update ROADMAP.md if implementing planned features
- Add inline comments for complex logic
- Include usage examples in docstrings

### Testing
- Test your changes thoroughly before submitting
- Verify functionality on your local environment
- Include test cases for new features (when applicable)
- Ensure existing functionality isn't broken

### Commit Messages
Use clear and descriptive commit messages:
```
✓ Good: "Add retry logic for Gemini API timeouts"
✓ Good: "Fix illegal move handling in get_gemini_move()"
✗ Bad: "fix bug"
✗ Bad: "updates"
```

Format:
```
Short summary (50 chars or less)

Longer explanation if needed. Wrap at 72 characters.
Explain what changed and why, not how.

- Bullet points are okay
- Reference issues: Fixes #123
```

## 🔄 Pull Request Process

### Before Submitting
1. **Update documentation** - README, ROADMAP, docstrings
2. **Test your changes** - Run the code and verify it works
3. **Check code style** - Ensure it follows project conventions
4. **Review your changes** - Look through the diff yourself first
5. **Update ROADMAP.md** - If implementing a planned feature, mark it complete

### Submitting a PR
1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Link to related issues (if any)
   - Screenshots for UI changes
   - Testing steps performed

3. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   Describe how you tested this
   
   ## Related Issues
   Fixes #123
   ```

### Code Review
- Be responsive to feedback
- Be open to suggestions
- Make requested changes promptly
- Ask questions if something is unclear
- Keep discussions professional and constructive

## 🐛 Reporting Bugs

### Before Reporting
- Check if the issue already exists
- Try to reproduce with latest version
- Collect relevant information

### Bug Report Template
```markdown
**Description:**
Clear description of the bug

**To Reproduce:**
1. Step one
2. Step two
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g., 3.11.2]
- Stockfish Version: [e.g., 16]
- Dependencies: [output of `pip list`]

**Error Messages:**
```
Paste error messages here
```

**Additional Context:**
Any other relevant information
```

## 💡 Suggesting Features

### Feature Request Template
```markdown
**Feature Description:**
Clear description of the feature

**Use Case:**
Why this feature is needed

**Proposed Solution:**
How it could work

**Alternatives Considered:**
Other approaches you've thought of

**Additional Context:**
Screenshots, examples, references
```

## 🏆 Recognition

Contributors will be:
- Listed in project acknowledgments
- Credited in release notes
- Mentioned in relevant documentation
- Given co-author credit in commits

## 📋 Priority Areas

See [ROADMAP.md](ROADMAP.md) for current priorities. High-priority areas:

### Phase 3 (Current Focus)
- Fine-tuning pipeline implementation
- Model evaluation metrics
- Performance tracking

### Code Quality
- Unit tests
- Integration tests
- CI/CD pipeline
- Code coverage

### Documentation
- Tutorial videos
- Architecture diagrams
- API documentation

## ❓ Questions?

- **GitHub Issues**: For technical questions
- **Discussions**: For general questions
- **Pull Requests**: For code-related questions

## 📜 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, experience level, nationality, personal appearance, race, religion, or sexual identity.

### Our Standards
**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement
Project maintainers have the right to remove, edit, or reject comments, commits, code, issues, and contributions that don't align with this Code of Conduct.

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to Arena! Your efforts help advance AI research and education. 🚀

*Last Updated: 2026-01-03*
