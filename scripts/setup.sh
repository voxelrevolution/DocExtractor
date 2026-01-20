#!/usr/bin/env bash
# Local Document Extraction Copilot - Setup Script
# Bootstraps development environment: Python venv, PostgreSQL, Ollama, dependencies
# Run from repository root: ./scripts/setup.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Redirect all output to log file and stdout
exec 1> >(tee -a setup.log)
exec 2>&1

log_info "=========================================="
log_info "Local Document Extraction - Setup Script"
log_info "=========================================="
log_info "Start time: $(date)"

# 1. Check prerequisites
log_info "Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 not found. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_info "Python version: $PYTHON_VERSION"

# Check Docker
if ! command -v docker &> /dev/null; then
    log_warn "Docker not found. PostgreSQL setup will require manual intervention."
else
    log_info "Docker found: $(docker --version)"
fi

# Check for docker-compose or docker compose
if docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
    log_info "Using 'docker compose' command"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
    log_info "Using 'docker-compose' command"
else
    log_warn "docker-compose not found. Skipping PostgreSQL startup."
    DOCKER_COMPOSE=""
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    log_warn "Ollama not found. Please install Ollama from https://ollama.ai"
else
    log_info "Ollama found: $(ollama --version || echo 'installed')"
fi

# 2. Create Python venv
log_info ""
log_info "Setting up Python virtual environment..."

if [ -d "venv" ]; then
    log_warn "venv already exists. Skipping creation."
else
    python3 -m venv venv
    log_info "Virtual environment created at ./venv"
fi

# Activate venv
source venv/bin/activate
log_info "Virtual environment activated"

# 3. Upgrade pip and install requirements
log_info ""
log_info "Installing Python dependencies..."

pip install --upgrade pip setuptools wheel > /dev/null 2>&1
log_info "pip upgraded"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    log_info "Dependencies installed from requirements.txt"
else
    log_error "requirements.txt not found!"
    exit 1
fi

# 4. Environment file
log_info ""
log_info "Setting up environment variables..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_info ".env created from .env.example"
    else
        log_warn ".env.example not found. Skipping .env setup."
    fi
else
    log_info ".env already exists"
fi

# 5. PostgreSQL via Docker Compose
log_info ""
log_info "Starting PostgreSQL service..."

if [ -z "$DOCKER_COMPOSE" ]; then
    log_warn "docker-compose not available. Skipping PostgreSQL startup."
    log_warn "To manually start PostgreSQL, run: docker-compose up -d"
else
    $DOCKER_COMPOSE up -d postgres
    log_info "PostgreSQL started (waiting for ready state...)"
    
    # Wait for PostgreSQL to be ready
    sleep 5
    for i in {1..30}; do
        if $DOCKER_COMPOSE exec -T postgres pg_isready -U docextractor > /dev/null 2>&1; then
            log_info "PostgreSQL is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_warn "PostgreSQL took longer than expected. May not be ready yet."
        fi
        sleep 1
    done
fi

# 6. Verify Ollama model
log_info ""
log_info "Checking Ollama models..."

if command -v ollama &> /dev/null; then
    # Try to list models; if Ollama is not running, this will show an error
    if ollama list 2> /dev/null | grep -q "llama3.1:8b"; then
        log_info "llama3.1:8b model found in Ollama"
    else
        log_warn "llama3.1:8b model not found. Run: ollama pull llama3.1:8b"
        log_warn "(Optional) Alternative installed models may work, but llama3.1:8b is the recommended default."
    fi
else
    log_warn "Ollama not installed or not in PATH"
fi

# 7. Create necessary directories
log_info ""
log_info "Creating project directories..."

mkdir -p data/postgres
mkdir -p data/documents
mkdir -p logs
mkdir -p evidence
log_info "Directories created"

# 8. Database initialization (if PostgreSQL is available)
log_info ""
log_info "Initializing database..."

if [ ! -z "$DOCKER_COMPOSE" ] && $DOCKER_COMPOSE ps postgres 2>/dev/null | grep -q "postgres"; then
    # Run init script if it exists
    if [ -f "scripts/init_postgres.sql" ]; then
        $DOCKER_COMPOSE exec -T postgres psql -U docextractor -d docextractor_dev -f /docker-entrypoint-initdb.d/init.sql 2>/dev/null || log_warn "Database init script not yet available (container may still be initializing)"
        log_info "Database initialized"
    else
        log_warn "scripts/init_postgres.sql not found. Skipping database initialization."
    fi
else
    log_warn "PostgreSQL not running. Skipping database initialization."
fi

# 9. Run smoke tests
log_info ""
log_info "Running smoke tests..."

if command -v pytest &> /dev/null; then
    if [ -d "tests" ]; then
        pytest tests/test_setup.py -v || log_warn "Some tests failed. Check output above."
    else
        log_warn "tests/ directory not found. Skipping smoke tests."
    fi
else
    log_warn "pytest not found. Skipping smoke tests."
fi

# 10. Print summary
log_info ""
log_info "=========================================="
log_info "Setup Complete!"
log_info "=========================================="
log_info "Summary:"
log_info "  ✓ Python venv activated"
log_info "  ✓ Dependencies installed"
log_info "  ✓ PostgreSQL running (if Docker available)"
log_info "  ✓ Environment variables configured"
log_info ""
log_info "Next steps:"
log_info "  1. Review docs/ONBOARDING.md for detailed guidance"
log_info "  2. Verify services: psql, ollama list, pytest"
log_info "  3. Start development!"
log_info ""
log_info "To activate venv in future terminal sessions:"
log_info "  source venv/bin/activate"
log_info ""
log_info "To stop services:"
log_info "  docker-compose down"
log_info ""
log_info "End time: $(date)"
log_info "=========================================="
