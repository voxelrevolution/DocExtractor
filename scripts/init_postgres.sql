-- PostgreSQL initialization script for DocExtractor
-- Creates pgvector extension and initializes schema

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    external_id UUID UNIQUE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    file_hash VARCHAR(64) UNIQUE NOT NULL,
    document_type VARCHAR(50),
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create extraction_results table
CREATE TABLE IF NOT EXISTS extraction_results (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    extraction_type VARCHAR(50),
    result_json JSONB NOT NULL,
    confidence_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create annotations table (for user corrections)
CREATE TABLE IF NOT EXISTS annotations (
    id SERIAL PRIMARY KEY,
    extraction_result_id INTEGER NOT NULL REFERENCES extraction_results(id),
    field_name VARCHAR(255),
    original_value TEXT,
    corrected_value TEXT,
    feedback_type VARCHAR(50),
    user_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create document embeddings table (for semantic search)
CREATE TABLE IF NOT EXISTS document_embeddings (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_file_hash ON documents(file_hash);
CREATE INDEX IF NOT EXISTS idx_documents_ingestion_timestamp ON documents(ingestion_timestamp);
CREATE INDEX IF NOT EXISTS idx_extraction_results_document_id ON extraction_results(document_id);
CREATE INDEX IF NOT EXISTS idx_annotations_extraction_result_id ON annotations(extraction_result_id);
CREATE INDEX IF NOT EXISTS idx_document_embeddings_document_id ON document_embeddings(document_id);

-- Create vector index for embeddings (using ivfflat for performance)
CREATE INDEX IF NOT EXISTS idx_document_embeddings_vector ON document_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO docextractor;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO docextractor;
