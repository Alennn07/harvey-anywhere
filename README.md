# Harvey Anywhere

**An open-source AI sales agent, extended for multiple AI providers and a more accessible developer experience.**

Harvey Anywhere is a community fork of [Harvey](https://github.com/ethanplusai/harvey), an autonomous AI sales agent designed to help teams discover potential customers, research businesses, identify decision-makers, prepare personalized outreach, and manage sales conversations.

Our goal is to make Harvey easier to adapt, run, and extend across different AI providers and development environments—while preserving the capabilities and safeguards that make the underlying project useful.

[Original project](https://github.com/ethanplusai/harvey) · [Report a bug](https://github.com/Alennn07/harvey-anywhere/issues) · [Contribute](CONTRIBUTING.md)

---

## Why Harvey Anywhere?

AI sales tools should be adaptable to the way developers and operators actually work. A project shouldn't be tied unnecessarily to one model provider, one development environment, or one contributor's setup.

Harvey Anywhere builds on the original Harvey codebase with a focus on:

- **Provider choice** — support for Claude, OpenAI Codex, and Google Gemini as the AI brain.
- **Developer accessibility** — improve setup and usability across supported environments, including Windows.
- **Practical automation** — connect prospect discovery, research, qualification, outreach drafting, and conversation management in one workflow.
- **Human oversight** — preserve review and approval safeguards around outbound communication.
- **Open development** — make the codebase easier to understand, test, extend, and contribute to.

This is an evolving community project. Our aim is to improve the experience without needlessly duplicating or breaking the upstream project's existing functionality.

## What can it do?

Harvey combines multiple stages of a sales workflow.

| Capability | Purpose |
|---|---|
| Prospect discovery | Find businesses that may match a target market. |
| Business research | Gather information to understand potential customers and their needs. |
| Decision-maker discovery | Identify relevant people and roles at prospective companies. |
| Lead qualification | Evaluate prospects against configured targeting criteria. |
| Personalized outreach | Prepare tailored sales messages and follow-ups. |
| Conversation management | Organize replies and maintain sales context. |
| Outbox and approval workflow | Review proposed messages before they are sent. |
| Local dashboard | Monitor activity and interact with the sales workflow. |

The exact capabilities available depend on configuration, integrations, credentials, and the selected provider.

## AI provider support

Harvey Anywhere currently includes three brain-provider options.

| Provider | Integration | Authentication model |
|---|---|---|
| Claude | Claude Code runtime | Your configured Claude environment |
| Codex | Codex runtime | Your configured Codex environment |
| Gemini | Google Gemini API | Gemini API key |

The selected provider is configured through Harvey's existing configuration system. Gemini support uses Google's `generateContent` API and includes input/output token usage tracking.

Provider capabilities, model availability, authentication requirements, usage limits, and costs differ. Selecting a provider does not guarantee that every provider behaves identically.

Harvey does not automatically switch providers simply because the selected provider fails.

## Getting started

### Requirements

- Python 3.11 or 3.12
- Git
- A supported AI provider configured for your chosen workflow
- The credentials required by any integrations you enable

Windows, macOS, and Linux are represented in the project's automated test matrix. Individual integrations and provider runtimes may have different platform requirements.

### 1. Clone the repository

```bash
git clone https://github.com/Alennn07/harvey-anywhere.git
cd harvey-anywhere
```

For the current development branch:

```bash
git switch feature/windows-gemini
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

**macOS or Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If your environment uses Python 3.12 instead, substitute `3.11` with `3.12`.

### 3. Configure your local environment

Start with the tracked configuration template, `.env.example`, and the project's setup instructions. Configure only the integrations you intend to use.

For Gemini, add your API key to your local `.env` file:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Obtain an API key through [Google AI Studio](https://aistudio.google.com/).

Keep API keys, personal configuration, contact data, and generated business intelligence out of commits. Never publish your `.env` file or share credentials in issue reports.

### 4. Configure Harvey

Review the configuration and setup guidance in the existing README and application documentation before running the agent. Configure your product, target market, and integrations for your own environment.

Do not start live outreach until you have reviewed the targeting, sender identity, compliance settings, and message approval behavior.

### 5. Explore the CLI

```bash
harvey --help
harvey status
harvey usage
```

These commands provide an entry point for discovering available commands, checking application status, and inspecting usage information.

Consult the CLI help and current configuration before using commands that discover prospects, modify state, or initiate outreach.

## Development and testing

Contributions should preserve existing behavior unless a change is intentional and documented.

Install the development dependencies and run the test suite:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

For focused Gemini provider tests:

```bash
python -m pytest -q tests/test_gemini_provider.py tests/test_brain_provider.py
```

The repository includes automated tests and a GitHub Actions workflow. Passing tests are useful evidence, but they do not guarantee that every live integration, model, credential setup, or operating-system configuration works.

When reporting results, distinguish automated tests, mocked integrations, and actual live-provider verification.

## Project structure

```text
harvey-anywhere/
├── .github/workflows/   # Automated test workflow
├── docs/                # Integration and feature documentation
├── harvey/              # Application and provider implementations
│   ├── agents/          # Sales workflow agents
│   ├── collectors/      # Discovery and research
│   ├── integrations/    # External services
│   └── web/              # Local dashboard assets
├── prompts/             # Agent prompts
├── skills/              # Sales knowledge and playbooks
├── tests/               # Automated tests
├── CONTRIBUTING.md      # Contribution guidelines
├── CHANGELOG.md         # Notable project changes
├── LICENSE              # Project license
└── pyproject.toml       # Python package and dependencies
```

This is a high-level map; consult the source tree for the current implementation.

## Security and responsible use

Harvey can process personal information and prepare outbound sales communications. Operators are responsible for configuring and using it appropriately.

- Keep credentials and private configuration out of version control.
- Use fictional contact data in tests and documentation.
- Respect opt-outs, do-not-contact lists, applicable laws, and provider terms.
- Review targeting and outreach settings before enabling sending.
- Prefer approval workflows until you have verified the behavior of your configuration.
- Report suspected security vulnerabilities privately rather than publishing exploit details or credentials in public issues.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the project's existing data-handling requirements.

## Contributing

We welcome thoughtful improvements to provider support, Windows usability, testing, documentation, reliability, and developer experience.

Before opening a pull request:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Keep changes focused and explain the reasoning behind them.
3. Add or update tests for changed behavior.
4. Run the relevant test suite.
5. Check your diff for credentials, real contact data, and private business information.

Please preserve upstream attribution and the existing license requirements.

## Roadmap

Areas of ongoing improvement include:

- A clearer onboarding experience for new contributors and operators.
- Consistent provider configuration and diagnostics.
- Reliable setup and testing across supported operating systems.
- Better architecture and troubleshooting documentation.
- Stronger automated checks and a more predictable contribution workflow.

This roadmap describes areas of focus, not a promise that every item is already implemented.

## Acknowledgements

Harvey Anywhere builds on the original [Harvey project](https://github.com/ethanplusai/harvey). We acknowledge the upstream authors and contributors whose work makes this community fork possible.

This is an independent community project and is not an official Google, Anthropic, or OpenAI product.

## License

Harvey Anywhere retains the license included in the repository. See [LICENSE](LICENSE) for the applicable terms and attribution requirements.

### Email warmup

Harvey supports TrulyInbox warmup integration. Learn more: https://trulyinbox.com/?via=harvey

