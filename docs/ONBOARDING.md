# Getting Started – Local Document Extraction Copilot

## Prerequisites
- **Python 3.11+** – Required for type hints and modern async
- **Docker & Docker Compose** – PostgreSQL will run in a container
- **Ollama** – Download from https://ollama.ai (includes Mixtral support)
- **Git** – For version control and repository access
- **Disk space** – ~50GB recommended (Ollama models + database)

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DocExtractor
```

### 2. Run Setup Script
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- Create a Python virtual environment (venv)
- Install all dependencies
- Start PostgreSQL in Docker
- Verify Ollama model availability
- Run smoke tests

### 3. Activate Virtual Environment
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 4. You're Ready!
Start developing. See "Next Steps" below.

---

## Detailed Setup (if Quick Start doesn't work)

### Step 1: Verify Python
```bash
python3 --version  # Should be 3.11 or higher
```

### Step 2: Verify Docker
```bash
docker --version
docker-compose --version  # or: docker compose --version
```

### Step 3: Install Ollama
Visit https://ollama.ai and download the installer for your OS.

After installation, verify:
```bash
ollama --version
```

### Step 4: Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Start PostgreSQL
```bash
docker-compose up -d postgres
```

Wait a few seconds, then verify:
```bash
docker-compose ps  # Should show postgres as healthy
```

### Step 7: Initialize Database
```bash
docker-compose exec postgres psql -U docextractor -d docextractor_dev \
  -f scripts/init_postgres.sql
```

### Step 8: Verify Ollama Model
```bash
ollama list
# Should show: mixtral:latest (or similar)
# If not, pull it:
ollama pull mixtral:latest
```

### Step 9: Run Tests
```bash
pytest tests/ -v
```

---

## Troubleshooting

### "Python 3 not found"
Install Python 3.11+ from https://python.org

### "Docker not found"
Install Docker Desktop from https://docker.com

### "PostgreSQL connection refused"
```bash
# Check if container is running
docker-compose ps

# If not, start it
docker-compose up -d postgres

# Check logs
docker-compose logs postgres
```

### "ollama: command not found"
Ollama may not be in your PATH. Try:
```bash
/Applications/Ollama.app/Contents/MacOS/ollama list  # macOS
# Or reinstall and ensure it's in your PATH
```

### "Mixtral model not found in Ollama"
```bash
ollama pull mixtral:latest
# This may take a few minutes and requires internet
```

### "psycopg2 installation fails"
On macOS, you might need PostgreSQL headers:
```bash
# macOS with Homebrew:
brew install libpq
export PATH="/usr/local/opt/libpq/bin:$PATH"

# Then retry:
pip install -r requirements.txt
```

### "Port 5432 already in use"
Another PostgreSQL instance is running. Either:
- Stop it: `docker-compose down`
- Change the port in docker-compose.yml

---

## Verification Checklist

After setup, verify everything works:

```bash
# 1. Python venv is active
python --version  # Should show 3.11+

# 2. PostgreSQL is running
psql -U docextractor -d docextractor_dev -h localhost -c "SELECT version();"

# 3. Ollama is running and has models
ollama list  # Should show mixtral

# 4. Python dependencies are installed
pip list | grep fastapi  # Should show fastapi version

# 5. Run smoke tests
pytest tests/ -v  # All tests should pass
```

---

## Next Steps

### For Developers
1. Read `docs/DEVELOPER_GUIDE.md` (coming soon)
2. Start with E01 deliverables in `roadmap/R01.../`
3. Check `PROJECT_STATUS_DASHBOARD.md` for current tasks

### For Contributing
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test: `pytest tests/`
3. Format code: `black src/`
4. Lint code: `ruff check src/`
5. Run type checks: `mypy src/`
6. Push and create a Pull Request

### For Troubleshooting
- Check `setup.log` for detailed setup output
- Review GitHub Issues for known problems
- Contact the tech lead for help

---

## Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PostgreSQL Documentation](https://postgresql.org/docs)
- [SQLAlchemy Documentation](https://sqlalchemy.org)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs)

---

**Last Updated:** 2026-01-13  
**Project Lead:** Senior Technical Lead  
**Questions?** Contact your team lead or check the project wiki.
