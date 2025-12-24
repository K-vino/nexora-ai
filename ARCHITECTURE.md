# NEXORA AI - Architecture Documentation

## Overview

NEXORA AI is built on a **Hexagonal Architecture** (also known as Ports and Adapters) pattern, ensuring clean separation of concerns, high testability, and maintainability.

## Architecture Layers

### 1. Core Layer (`src/nexora/core/`)

The innermost layer containing fundamental abstractions and utilities.

**Components:**
- `base.py`: Abstract base classes for all major components
  - `BaseProcessor`: Generic data processor interface
  - `BaseRepository`: Data persistence interface
  - `BaseService`: Application service interface
  - `Configurable`: Configuration interface
  - `BaseAdapter`: Adapter interface

- `exceptions.py`: Custom exception hierarchy
  - `NexoraException`: Base exception with context and original exception tracking
  - Domain-specific exceptions (ValidationException, ModelingException, etc.)

- `logger.py`: Structured logging configuration
  - `setup_logging()`: Configure application-wide logging
  - `get_logger()`: Get module-specific loggers

**Key Principles:**
- No dependencies on outer layers
- Pure business logic abstractions
- Type-safe with complete type hints

### 2. Domain Layer (`src/nexora/domain/`)

Contains business entities and domain logic.

**Entities:**
- `DataSource`: Represents a data source (immutable value object)
- `Dataset`: Represents a dataset with quality metrics
- `Feature`: Engineered feature with metadata
- `Model`: Machine learning model with performance metrics
- `Explanation`: Model explanation results
- `Report`: Generated report
- `WorkflowExecution`: Workflow execution state

**Enumerations:**
- `DataQuality`: UNKNOWN, POOR, FAIR, GOOD, EXCELLENT
- `ProcessingStatus`: PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED

**Key Principles:**
- Rich domain model with behavior
- Immutability where appropriate (dataclasses with frozen=True)
- Self-contained validation logic

### 3. Application Layer (`src/nexora/application/`)

Orchestrates business operations and defines interfaces.

**Ports (Interfaces):**
- `DataIngestionPort`: Interface for data ingestion
- `DataValidationPort`: Interface for data validation
- `FeatureEngineeringPort`: Interface for feature engineering
- `ModelingPort`: Interface for ML modeling
- `ExplainabilityPort`: Interface for model explanation
- `GenAIPort`: Interface for GenAI operations
- `ReportingPort`: Interface for report generation

**Use Cases:**
- `IngestDataUseCase`: Orchestrates data ingestion and validation
- `TrainModelUseCase`: Orchestrates feature engineering and model training
- `ExplainModelUseCase`: Orchestrates explanation generation with GenAI insights
- `GenerateReportUseCase`: Orchestrates report generation with GenAI narratives

**Key Principles:**
- Port interfaces define contracts (dependency inversion)
- Use cases coordinate between ports
- No direct dependencies on adapters or infrastructure

### 4. Adapter Layer (`src/nexora/adapters/`)

Concrete implementations of port interfaces.

**Ingestion Adapters:**
- `FileIngestionAdapter`: Ingest from local files (CSV, JSON, Parquet)
- `DatabaseIngestionAdapter`: Ingest from databases (PostgreSQL, MySQL, SQLite, MongoDB)

**Validation Adapters:**
- `StandardValidationAdapter`: Common validation rules
- `SchemaValidationAdapter`: Schema-based validation

**Feature Engineering Adapters:**
- `StandardFeatureEngineeringAdapter`: Standard transformations
- `TimeSeriesFeatureEngineeringAdapter`: Time series features

**Modeling Adapters:**
- `SklearnModelingAdapter`: Scikit-learn models
- `DeepLearningModelingAdapter`: Deep learning models (PyTorch/TensorFlow)

**Explainability Adapters:**
- `SHAPExplainabilityAdapter`: SHAP-based explanations
- `LIMEExplainabilityAdapter`: LIME-based explanations
- `PermutationImportanceAdapter`: Permutation importance

**GenAI Adapters:**
- `LocalLLMAdapter`: Local LLM integration
- `PromptBasedGenAIAdapter`: Prompt engineering approach

**Reporting Adapters:**
- `MarkdownReportingAdapter`: Markdown reports
- `HTMLReportingAdapter`: HTML reports
- `JSONReportingAdapter`: JSON reports

**Key Principles:**
- Each adapter implements a specific port
- Adapters can be swapped without changing business logic
- Error handling with custom exceptions

### 5. Infrastructure Layer (`src/nexora/infrastructure/`)

Cross-cutting concerns and configuration.

**Components:**
- `Configuration`: Configuration data class
- `ConfigurationLoader`: Load configuration from files, env vars, or dictionaries

**Key Principles:**
- Framework-independent
- Environment-aware
- Validation on load

### 6. Orchestration Layer (`src/nexora/orchestration/`)

Workflow coordination and execution.

**Components:**
- `WorkflowDefinition`: Defines a workflow with steps
- `WorkflowStep`: Individual workflow step with dependencies
- `WorkflowOrchestrator`: Executes workflows with dependency resolution
- `WorkflowBuilder`: Fluent API for building workflows

**Key Principles:**
- Dependency-aware execution
- Retry logic support
- Execution tracking

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        Use Case                              │
│  (Orchestrates business logic using multiple ports)          │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │       Ports            │
    │   (Interfaces)         │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │      Adapters          │
    │  (Implementations)     │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │   External Systems     │
    │ (Files, DBs, APIs)     │
    └───────────────────────┘
```

## Dependency Rules

1. **Dependencies point inward**: Outer layers depend on inner layers, never the reverse
2. **Core has no dependencies**: The core layer is dependency-free
3. **Domain is pure**: Domain layer has no infrastructure dependencies
4. **Application defines interfaces**: Application layer defines ports, adapters implement them
5. **Adapters are swappable**: Multiple implementations of the same port can coexist

## Design Patterns Used

### Hexagonal Architecture (Ports and Adapters)
- **Purpose**: Separate business logic from external concerns
- **Implementation**: Ports define interfaces, adapters implement them
- **Benefit**: Easy testing, swappable implementations

### Dependency Inversion Principle
- **Purpose**: High-level modules don't depend on low-level modules
- **Implementation**: Use cases depend on port interfaces, not concrete adapters
- **Benefit**: Loose coupling, flexibility

### Repository Pattern
- **Purpose**: Abstracting data access
- **Implementation**: BaseRepository abstract class
- **Benefit**: Consistent data access interface

### Strategy Pattern
- **Purpose**: Interchangeable algorithms
- **Implementation**: Multiple adapters for same port
- **Benefit**: Runtime algorithm selection

### Template Method Pattern
- **Purpose**: Define algorithm skeleton
- **Implementation**: BaseProcessor with abstract process() method
- **Benefit**: Consistent processing structure

### Builder Pattern
- **Purpose**: Construct complex objects step-by-step
- **Implementation**: WorkflowBuilder for workflow construction
- **Benefit**: Fluent, readable API

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock dependencies using port interfaces
- Test domain logic without infrastructure

### Integration Tests
- Test interactions between layers
- Use real adapters with test data
- Verify end-to-end workflows

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── core/               # Core layer tests
│   ├── domain/             # Domain layer tests
│   ├── application/        # Application layer tests
│   └── adapters/          # Adapter tests
└── integration/            # Integration tests
    ├── workflows/         # Workflow tests
    └── end_to_end/       # Full pipeline tests
```

## Extension Points

### Adding New Adapters

1. Define port interface in `application/ports.py`
2. Implement adapter in `adapters/<domain>/`
3. Follow naming convention: `<Type>Adapter`
4. Handle errors with domain-specific exceptions
5. Add comprehensive logging
6. Write unit tests

### Adding New Use Cases

1. Create use case class in `application/use_cases.py`
2. Inject required ports via constructor
3. Implement execute() method
4. Add error handling and logging
5. Write unit tests with mocked ports

### Adding New Entities

1. Define entity in `domain/entities.py`
2. Use dataclasses for immutability
3. Add business logic methods
4. Include validation
5. Write unit tests

## Performance Considerations

### Lazy Loading
- Configuration loaded on demand
- Adapters initialized only when needed

### Caching
- Implement caching at adapter level
- Cache expensive operations (model loading, etc.)

### Async Support
- Ready for async/await pattern
- Ports can be extended with async methods

### Resource Management
- Use context managers for resources
- Proper cleanup in BaseService.shutdown()

## Security Considerations

### Input Validation
- Validate all inputs at adapter level
- Use domain entities for type safety

### Error Handling
- Never expose internal details in exceptions
- Log sensitive errors internally only

### Configuration
- Never hardcode credentials
- Use environment variables or secure vaults

## Monitoring and Observability

### Logging
- Structured logging throughout
- Consistent log levels
- Contextual information in logs

### Metrics
- Track workflow execution times
- Monitor adapter performance
- Count successes/failures

### Tracing
- Execution IDs for tracking
- Step-by-step workflow logging

## Future Enhancements

1. **Async/Await Support**: Add async versions of ports and adapters
2. **Event Sourcing**: Track all state changes as events
3. **CQRS**: Separate read and write models
4. **GraphQL API**: Add GraphQL layer on top of use cases
5. **Streaming**: Support for streaming data processing
6. **Distributed Execution**: Execute workflows across multiple nodes
7. **Real-time Monitoring**: Dashboard for live workflow monitoring
8. **Plugin System**: Load adapters dynamically from plugins

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
