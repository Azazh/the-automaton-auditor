# Code Style Standards for the Automaton Auditor

## Pydantic Rigor
- **Mandatory BaseModel Usage**: Every piece of data, including `Evidence`, `JudicialOpinion`, and other domain-specific entities, must inherit from `pydantic.BaseModel`.
- **Explicit Descriptions**: Each field in a Pydantic model must include a `description` that explains its role in the "Digital Courtroom."
- **Field Constraints**: Use Pydantic validators and field constraints (e.g., `constr`, `conint`, `conlist`) to enforce data integrity and domain-specific rules.

## Parallel State Management
- **Annotated Types**: Use `typing.Annotated` for all state fields to ensure clarity and enforce constraints.
- **Operator Usage**: 
  - Use `operator.add` for merging lists to prevent overwriting during parallel execution.
  - Use `operator.ior` for merging dictionaries to ensure state consistency.
- **State Safety**: Ensure that all state updates are atomic and thread-safe to support parallel execution of Detectives and Judges.

## Strict Typing
- **Prohibition of `Any`**: The use of `Any` is strictly prohibited.
- **Complete Type Hints**: Every function must include type hints for all inputs and outputs. Use `mypy` or similar tools to enforce this rule.
- **Type Aliases**: Define and use type aliases for complex types to improve readability and maintainability.

## Asynchronous Patterns
- **Async-First Design**: All LangGraph nodes and tools must be implemented as `async def` functions.
- **Concurrency**: Use `asyncio` primitives (e.g., `gather`, `Semaphore`) to manage concurrency effectively.
- **Non-Blocking I/O**: Ensure that all I/O operations (e.g., file reads, API calls) are non-blocking to maximize performance.

## Separation of Concerns
- **Forensic Tools**: Implement all system interactions (e.g., file parsing, git operations) in the `tools` directory. Tools must be reusable and stateless.
- **Nodes**: Nodes in the `nodes` directory should only handle state orchestration and must not contain business logic.
- **Clear Boundaries**: Avoid mixing concerns between tools and nodes. Each module should have a single, well-defined responsibility.

## Beyond the Rubric (Elite Tier)

### Self-Documenting Code
- **Field Descriptions**: Every Pydantic field must include a `description` that explains its role in the "Digital Courtroom."
- **Docstrings**: All functions, classes, and modules must include docstrings that describe their purpose, inputs, outputs, and exceptions.
- **Readable Code**: Write code that is easy to read and understand, even for developers unfamiliar with the project.

### Defensive Programming
- **Standardized Responses**: All tools must return a standard "No Evidence Found" object when no data is available, instead of raising unhandled exceptions.
- **Error Handling**: Use `try`-`except` blocks to handle errors gracefully and log meaningful messages.
- **Validation**: Validate all inputs to functions and raise descriptive exceptions for invalid data.

---

By adhering to these standards, the Automaton Auditor project will maintain the highest level of technical excellence and ensure that both human developers and AI agents achieve "Master Thinker" status.