# AI Tools Collection

A personal collection of AI-related tools and utilities, featuring:
- Setup and management of AI services like OpenWebUI
- Retrieval-Augmented Generation (RAG) systems for web search and sports data
- Automated backup and configuration management
- Integration with SearxNG and Reddit for enhanced data retrieval

The project combines Go-based service management with Python-based RAG implementations, providing a comprehensive toolkit for AI applications.

## Features

### OpenWebUI Management
- **Setup**: Automated installation and setup of OpenWebUI
- **Backup**: Backup functionality for OpenWebUI database and configurations
  - Automatically detects Python installation and site packages
  - Safely backs up the WebUI database

### RAG System
- Python-based Retrieval-Augmented Generation implementation
- Includes development tools and testing framework
- Supports both MacOS and Linux environments

#### Available RAG APIs
- **Web Search RAG**: 
  - Integrates with SearxNG for web search capabilities
  - Supports customizable search parameters (time range, website filtering)
  - Reddit integration for social media content retrieval
- **Football Data RAG**:
  - Fetches and processes football match data
  - Supports multiple tournaments and date-based queries

### Coming Soon
- SearXNG setup and configuration (In development)

## Prerequisites

- Go 1.24.0 or higher
- Python (for OpenWebUI functionality)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ai
```

2. Build the project:
```bash
make build
```

This will create the `ai` binary in the `target` directory.

## Usage

### OpenWebUI

Set up OpenWebUI:
```bash
make setup-owui
```

Backup OpenWebUI data:
```bash
make backup
```
This will create a backup in the `tmp` directory.

## Development

Run tests:
```bash
make test
```

## Project Structure

```
.
├── cmd/          # Command-line interface implementations
├── rags/         # RAG system implementation
│   ├── src/          # RAG source code
│   │   ├── api/         # FastAPI endpoints
│   │   ├── rags/        # RAG implementations
│   │   │   ├── web_search/  # Web search RAG
│   │   │   └── football/    # Football data RAG
│   │   └── owui/        # OpenWebUI integration
│   ├── pyproject.toml   # Python dependencies
│   └── Makefile        # RAG-specific build commands
├── src/          # Source code for different services
│   ├── openwebui/    # OpenWebUI related functionality
│   ├── searxng/     # SearXNG related functionality (WIP)
│   └── utils/       # Shared utilities
├── Makefile     # Build and automation scripts
└── go.mod       # Go module definition
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License

Copyright (c) 2024 Shun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
