# Contributing to PyPI Banner Generator

Thank you for your interest in contributing to the PyPI Banner Generator! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue templates** when available
3. **Provide detailed information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

### Suggesting Features

1. **Open a discussion** first for major features
2. **Describe the use case** clearly
3. **Consider backwards compatibility**
4. **Provide mockups or examples** when possible

### Code Contributions

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/PYPI-Banner-Generator.git
   cd PYPI-Banner-Generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style
- Follow **PEP 8** style guidelines
- Use **meaningful variable names**
- Add **docstrings** to functions and classes
- Keep functions **focused and small**
- Use **type hints** where appropriate

##### Adding New Themes
When adding new themes to `ALL_THEMES`:

```python
'XX': {
    'name': 'theme_name',           # snake_case, descriptive
    'description': 'Brief description', # User-friendly description
    'type': 'category',             # professional, minimal, gradient, modern, etc.
    'bg': '#ffffff',                # Background color (or bg_start/bg_end for gradients)
    'primary': '#000000',           # Primary text color
    'secondary': '#666666',         # Secondary text color
    'accent': '#0066cc',            # Accent color for highlights
    'card': '#f8f9fa',             # Card/container background
    'border': '#dee2e6'            # Border color
}
```

##### Adding New Features
- **Test thoroughly** with different packages
- **Consider performance impact**
- **Update documentation** (README.md)
- **Add command-line options** if applicable
- **Maintain backwards compatibility**

#### Testing

Before submitting:

1. **Test with multiple packages**:
   ```bash
   python banner_generator.py --package requests
   python banner_generator.py --package numpy
   python banner_generator.py --package django
   ```

2. **Test all generation modes**:
   - Single theme
   - Multiple themes  
   - All themes
   - Category selection

3. **Test command-line interface**:
   ```bash
   python banner_generator.py --help
   python banner_generator.py --list-themes
   python banner_generator.py --package requests --theme 1
   ```

4. **Verify output quality**:
   - Check generated images
   - Verify file sizes are reasonable
   - Test with/without logo

#### Pull Request Process

1. **Update documentation** if needed
2. **Add your changes** to the description
3. **Reference any related issues**
4. **Ensure CI passes** (if applicable)
5. **Request review** from maintainers

##### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tested with multiple packages
- [ ] Tested all generation modes
- [ ] Verified output quality
- [ ] Updated documentation

## Screenshots
(If applicable)
```

## 🎨 Design Guidelines

### Theme Design Principles
- **Professional**: Suitable for business/corporate use
- **Readable**: High contrast, clear typography
- **Consistent**: Coherent color scheme
- **Scalable**: Works at banner size (1200x630)
- **Accessible**: Consider color blindness

### Visual Hierarchy
1. **Package name** - Most prominent
2. **Version badge** - Secondary importance
3. **Description** - Readable but not overpowering
4. **Install command** - Clear and actionable
5. **URL/metadata** - Subtle but present

### Color Guidelines
- **Use hex colors** for consistency
- **Test contrast ratios** for accessibility
- **Consider dark/light modes** if applicable
- **Avoid overly bright colors** for professional use

## 📁 Project Structure

```
PYPI-Banner-Generator/
├── banner_generator.py      # Main application
├── requirements.txt         # Dependencies
├── setup.py                # Package configuration
├── README.md               # Project documentation
├── CONTRIBUTING.md         # This file
├── LICENSE                 # MIT license
├── .gitignore             # Git ignore rules
├── .github/               # GitHub configuration
│   └── workflows/         # CI/CD workflows
├── DejaVuSans-Bold.ttf    # Font files
├── DejaVuSans.ttf
├── pypi_logo.png          # Default logo
└── output/                # Generated banners (ignored)
```

## 🔧 Development Tips

### Debugging
- Use `print()` statements for debugging
- Test with edge cases (long names, missing data)
- Verify API responses from PyPI

### Performance
- Consider image processing performance
- Optimize font loading and reuse
- Monitor memory usage for batch generation

### Compatibility
- Test on different Python versions (3.7+)
- Consider different operating systems
- Verify font rendering across platforms

## 📞 Getting Help

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Email**: Contact maintainers for sensitive issues

## 🏆 Recognition

Contributors will be:
- **Listed in README.md** acknowledgments
- **Credited in release notes** for significant contributions
- **Invited as collaborators** for ongoing contributors

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make PyPI Banner Generator better! 🚀
