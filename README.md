# Guardrails CSV Validator

![csv-validator](csv-validator.jpg)

[![apache license](https://img.shields.io/badge/License-Apache2-blue.svg)](https://opensource.org/licenses/Apache-2-0)

A CSV validator for [Guardrails AI](https://www.guardrailsai.com/).

This validator checks for various CSV issues such as mismatched column lengths, or mismatched quote delimiters.

## Guardrails

Guardrails AI is the leading open-source framework to define and enforce assurance for LLM applications. It offers:

- Framework for creating custom validations at an application level
- Orchestration of prompting → verification → re-prompting
- Library of commonly used validators for multiple use cases
- Specification language for communicating requirements to LLM

## Under the hood

Guardrails provides an object definition called a Rail for enforcing a specification on an LLM output, and a lightweight wrapper called a Guard around LLM API calls to implement this spec.

1. `rail`` (Reliable AI markup Language) files for specifying structure and type information, validators and corrective actions over LLM outputs. The concept of a Rail has evolved from markup - Rails can be defined in either Pydantic or RAIL for structured outputs, or directly in Python for string outputs.

2. Guard wraps around LLM API calls to structure, validate and correct the outputs.


### Testing and using your validator
- Open [test/test-validator.py](test/test-validator.py) to test your new validator 
- Import your new validator and modify `ValidatorTestObject` accordingly
- Modify the TEST_OUTPUT and TEST_FAIL_OUTPUT accordingly
- Run `python test/test-validator.py` via terminal, make sure the returned output reflects the input object 
- Write advanced tests for failures, etc.
