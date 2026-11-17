
from pathlib import Path

PROJECT_STRUCTURE = {
    "src": {
        "__init__.py": None,

        "core": {
            "__init__.py": None,
            "config.py": None,
            "logging.py": None,
            "exceptions.py": None,
            "security.py": None,
        },

        "database": {
            "__init__.py": None,
            "connection.py": None,
            "base.py": None,
            "session.py": None,
            "models": {
                "__init__.py": None,
                "lead.py": None,
                "conversation.py": None,
                "document.py": None,
                "booking.py": None,
            },
        },

        "schemas": {
            "__init__.py": None,
            "chat.py": None,
            "lead.py": None,
            "booking.py": None,
            "documents.py": None,
        },

        "api": {
            "__init__.py": None,
            "dependencies.py": None,
            "routes": {
                "__init__.py": None,
                "chat.py": None,
                "leads.py": None,
                "bookings.py": None,
                "documents.py": None,
                "health.py": None,
            },
        },

        "rag": {
            "__init__.py": None,
            "ingestion.py": None,
            "chunking.py": None,
            "embeddings.py": None,
            "vector_store.py": None,
            "retriever.py": None,
            "guardrails.py": None,
            "pipeline.py": None,
        },

        "llm": {
            "__init__.py": None,
            "base.py": None,
            "openai_provider.py": None,
            "anthropic_provider.py": None,
            "router.py": None,
            "fallback.py": None,
        },

        "agents": {
            "__init__.py": None,
            "state.py": None,
            "graph.py": None,
            "nodes": {
                "__init__.py": None,
                "classify.py": None,
                "retrieve.py": None,
                "qualify_lead.py": None,
                "extract_lead.py": None,
                "booking.py": None,
                "respond.py": None,
            },
        },

        "integrations": {
            "__init__.py": None,
            "crm": {
                "__init__.py": None,
                "client.py": None,
                "webhooks.py": None,
            },
            "calendar": {
                "__init__.py": None,
                "client.py": None,
                "booking.py": None,
            },
            "n8n": {
                "__init__.py": None,
                "client.py": None,
            },
        },

        "services": {
            "__init__.py": None,
            "chat_service.py": None,
            "lead_service.py": None,
            "booking_service.py": None,
            "document_service.py": None,
        },
    },

    "evaluation": {
        "__init__.py": None,
        "datasets": {},
        "metrics": {
            "rag_metrics.py": None,
            "agent_metrics.py": None,
        },
        "tests": {
            "test_rag.py": None,
            "test_agent.py": None,
            "test_llm_fallback.py": None,
            "test_integrations.py": None,
        },
        "run_evaluation.py": None,
    },

    "tests": {
        "__init__.py": None,
        "unit": {},
        "integration": {},
        "e2e": {},
    },

    "scripts": {
        "ingest_documents.py": None,
        "create_tables.py": None,
    },

    "knowledge_base": {
        "raw": {},
        "processed": {},
    },

    "frontend": {
        "README.md": None,
    },

    "docs": {
        "architecture.md": None,
        "api_documentation.md": None,
        "deployment.md": None,
    },

    "": {
        ".env.example": None,
        ".gitignore": None,
        "requirements.txt": None,
        "Dockerfile": None,
        "docker-compose.yml": None,
        "README.md": None,
        "main.py": None,
    },
}


def create_structure(base_path: Path, structure: dict):
    for name, content in structure.items():

        if name == "":
            current_path = base_path
        else:
            current_path = base_path / name

        if content is None:
            current_path.parent.mkdir(parents=True, exist_ok=True)
            current_path.touch(exist_ok=True)
            print(f"FILE  : {current_path}")

        else:
            current_path.mkdir(parents=True, exist_ok=True)
            print(f"DIR   : {current_path}")

            create_structure(current_path, content)


def main():
    root = Path.cwd()

    print("\nCreating AI Customer Support Automation structure...\n")

    create_structure(root, PROJECT_STRUCTURE)

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    main()
