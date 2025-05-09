# Contributing to Zack's CDK Library

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/zackrylangford/zacks-cdk-library.git
   cd zacks-cdk-library
   ```

2. Install the library in development mode:
   ```bash
   pip install -e .
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Adding New Constructs

1. Create a new file in the appropriate module directory (e.g., `zacks_cdk_lib/compute/`)
2. Implement your construct following the existing patterns
3. Update the `__init__.py` file to export your new construct
4. Add tests for your construct

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for all classes and methods
- Keep lines under 100 characters

## Testing

Before submitting a pull request, make sure your changes pass all tests:

```bash
pytest
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.