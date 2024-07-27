# Task Automation Orchestrator (TAO) v2.0


## Overview

The Task Automation Orchestrator (TAO) v2.0 is a powerful, flexible system designed to automate complex, multi-step workflows. This refactored version builds upon the original AI-driven design, transitioning to a more traditional, logic-based approach using Python. TAO v2.0 offers enhanced configurability, improved error handling, and a plugin-based architecture for maximum flexibility.

## Key Changes in v2.0

- **Operate as a standalone logic engine before implementing LLM**: A functional, configurable, rule-based logic engine must be able to stand alone before implementing AI-driven decision Orchestrator.
- **Plugin-based Architecture**: Introduced a modular, plugin-based system for enhanced flexibility and extensibility.
- **Enhanced Configuration**: Expanded YAML-based configuration for fine-grained control over workflows and tasks.
- **Improved Error Handling**: Implemented more robust, configurable error management at multiple levels.

## Key Features

- **Dual Configuration Modes**: Choose between complex and basic configuration setups to suit your workflow needs.
- **Plugin-based Architecture**: Easily extend functionality with custom plugins.
- **Advanced Conditional Logic**: Create sophisticated workflows with complex branching and decision-making.
- **Dynamic Data Flow**: Flexibly pass data between tasks and steps within your workflow.
- **Comprehensive Error Handling**: Robust error management at multiple levels (workflow, task, and step).
- **Detailed Logging**: Configure logging at global and task-specific levels.
- **Templating System**: Reuse common configurations across different workflows.
- **Resource Management**: Easily manage external resources like databases and API endpoints.
- **Security Features**: Built-in security configurations for sensitive operations.
- **Dynamic Variable Management**: Define, set, and use variables across your workflow for flexible task execution.
- **Enhanced Conditional Logic**: Create complex, data-driven decision trees using runtime variables and task outputs.

## Configuration Structure

TAO v2.0 supports two levels of configuration complexity:

1. **Complex Configuration** (`complex_config.yaml`):
   - Modular structure with references to other configuration files
   - Schema definitions for validation
   - Detailed task and step configurations
   - Advanced conditional logic and data flow management
   - Task-specific logging configurations
   - Dynamic variable definition and usage throughout the workflow

2. **Basic Configuration** (`basic_config.yaml`):
   - Essential configuration elements
   - Simplified workflow structure
   - Minimal plugin usage
   - Basic error handling and logging
   - Simple variable usage and basic conditional logic

## Variable Management

TAO v2.0 introduces a powerful variable management system:

1. **Defining Variables**: 
   Variables can be defined at the workflow level or within tasks:

   ```yaml
   workflow:
     variables:
       global_var: "I'm a global variable"
     tasks:
       - name: task1
         variables:
           task_var: "I'm a task-specific variable"
   ```

2. **Using Variables**:
   Reference variables using the `${variable_name}` syntax:

   ```yaml
   tasks:
     - name: print_message
       plugin: core_plugin
       function: print_message
       parameters:
         message: ${global_var}
   ```

3. **Setting Variables**:
   Tasks can set variables for use in subsequent tasks:

   ```yaml
   tasks:
     - name: set_variable
       plugin: core_plugin
       function: process_data
       set_variables:
         processed_result: "{{ result.data }}"
   ```

4. **Dynamic Expressions**:
   Use expressions for dynamic variable values:

   ```yaml
   variables:
     current_date: "{{ now().strftime('%Y-%m-%d') }}"
   ```

## Enhanced Conditional Logic

TAO v2.0 supports advanced conditional logic using variables and task outputs:

1. **Simple Conditions**:
   ```yaml
   tasks:
     - name: conditional_task
       plugin: core_plugin
       function: branch
       conditions:
         - condition: "{{ file_count > 0 }}"
           true_branch: process_files
           false_branch: handle_no_files
   ```

2. **Complex Conditions**:
   ```yaml
   tasks:
     - name: complex_conditional
       plugin: core_plugin
       function: evaluate
       conditions:
         - type: and
           conditions:
             - "{{ tasks.process_files.output.processed_count > 10 }}"
             - "{{ 'high_priority' in workflow.flags }}"
           true_branch: send_priority_notification
           false_branch: continue
   ```

## Advanced Configuration Example

Here's an example showcasing variable usage and advanced conditional logic:

```yaml
workflow:
  name: "Advanced Data Processing"
  variables:
    input_directory: "./data/input"
    file_count: 0
    error_threshold: 5
  tasks:
    - name: count_files
      plugin: file_operations_plugin
      function: count_files
      parameters:
        directory: ${input_directory}
      set_variables:
        file_count: "{{ result }}"
    
    - name: process_files
      plugin: data_plugin
      function: process_data
      conditions:
        - condition: "{{ file_count > 0 }}"
          true_branch: perform_processing
          false_branch: handle_no_files
      parameters:
        input_files: "{{ tasks.count_files.output.files }}"
      set_variables:
        processed_count: "{{ result.processed }}"
        error_count: "{{ result.errors }}"
    
    - name: evaluate_results
      plugin: core_plugin
      function: branch
      conditions:
        - type: and
          conditions:
            - "{{ processed_count > 0 }}"
            - "{{ error_count <= error_threshold }}"
          true_branch: generate_report
          false_branch: handle_errors
    
    - name: generate_report
      plugin: reporting_plugin
      function: create_report
      parameters:
        data: "{{ tasks.process_files.output.data }}"
    
    - name: handle_errors
      plugin: error_plugin
      function: log_errors
      parameters:
        error_count: ${error_count}
        threshold: ${error_threshold}
```

This example demonstrates how to use variables, set them dynamically, and use them in conditional logic to create a flexible, adaptive workflow.

## Repurposing for Different Tasks

To repurpose TAO for different tasks:

1. **Define Task-Specific Variables**: Identify the key parameters for your task and define them as variables in your workflow.

2. **Create Custom Plugins**: Develop plugins that encapsulate the core functionality of your specific tasks.

3. **Design Flexible Workflows**: Use variables and conditional logic to create workflows that can adapt to different inputs and scenarios.

4. **Utilize Dynamic Branching**: Leverage the enhanced conditional logic to create dynamic workflow paths based on task outputs and variable states.

5. **Parameterize Configurations**: Use variables for file paths, thresholds, and other configurable elements to make your workflows easily adaptable to different environments or requirements.

By leveraging these capabilities, you can easily adapt TAO to a wide range of automation tasks without modifying the core system.


## Error Handling and Logging

TAO v2.0 provides comprehensive error handling and logging:

- Configure global and task-specific logging in the YAML configuration.
- Use the `error_handling` section in the configuration to define retry logic and fallback actions.
- Implement custom error handling in your plugins by overriding the `handle_error` method.

Example configuration:

```yaml
logging:
  global:
    level: INFO
    file: "./logs/tao_log.txt"
  tasks:
    data_processing:
      level: DEBUG

error_handling:
  global:
    max_retries: 3
    retry_delay: 60
  tasks:
    api_call:
      max_retries: 5
      retry_delay: 30
```

## Security Best Practices

1. Use environment variables for sensitive information (API keys, passwords).
2. Implement proper authentication and authorization in your plugins.
3. Regularly update TAO and its dependencies.
4. Use HTTPS for any network communications.
5. Implement input validation for all user-supplied data.
6. Regularly audit your workflows and plugins for security vulnerabilities.

## Contributing

We welcome contributions to TAO! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

Common issues and their solutions:

1. **Plugin not loading**: Ensure the plugin is in the correct directory and properly registered in the configuration file.
2. **Configuration validation errors**: Check your YAML syntax and ensure all required fields are present.
3. **Task execution failures**: Review the logs for specific error messages and ensure all required resources are available.

## FAQ

Q: Can I mix complex and basic configurations?
A: Yes, you can start with a basic configuration and gradually add complex features as needed.

Q: How do I add a new task type?
A: Create a new plugin that implements the task logic, then reference it in your workflow configuration.

Q: Is TAO suitable for distributed workflows?
A: Currently, TAO is designed for local execution. Distributed workflow support is on our roadmap for future versions.

## Changelog

### v2.0.0 (Current)
- Refactored to plugin-based architecture
- Introduced dual configuration modes (complex and basic)
- Improved error handling and logging
- Added advanced conditional logic and data flow management
-  Removed AI driven workflow Management

### v1.5.0
- Added initial plugin support
- Improved workflow visualization

### v1.0.0
- Initial release with AI-driven workflow management

## Roadmap

- [ ] Distributed workflow execution support
- [ ] GUI for workflow design and monitoring
- [ ] Machine learning integration for workflow optimization
- [ ] Real-time collaboration features
- [ ] Extended API for third-party integrations
