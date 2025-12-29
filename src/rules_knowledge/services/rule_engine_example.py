"""
Example usage of RuleEngineService

This file demonstrates how to use the Rule Engine Service for evaluating
eligibility across different jurisdictions (UK, US, Canada, etc.).
"""

from rules_knowledge.services.rule_engine_service import RuleEngineService
from datetime import datetime


def example_eligibility_check():
    """
    Example: Run eligibility check for a case.
    
    This works for any jurisdiction (UK, US, Canada) as long as:
    1. The visa type exists in the database
    2. There's an active, published rule version for that visa type
    3. The case has facts stored
    """
    
    case_id = "550e8400-e29b-41d4-a716-446655440000"
    visa_type_id = "660e8400-e29b-41d4-a716-446655440001"
    
    # Run eligibility evaluation
    result = RuleEngineService.run_eligibility_evaluation(
        case_id=case_id,
        visa_type_id=visa_type_id,
        evaluation_date=None  # Uses current date by default
    )
    
    if result:
        print(f"Outcome: {result.outcome}")
        print(f"Confidence: {result.confidence:.2%}")
        print(f"Requirements Passed: {result.requirements_passed}/{result.requirements_total}")
        print(f"Missing Facts: {result.missing_facts}")
        
        # Convert to dict for API response
        result_dict = result.to_dict()
        return result_dict
    else:
        print("Evaluation could not be performed (no active rule version)")
        return None


def example_step_by_step():
    """
    Example: Step-by-step evaluation (for debugging or custom logic).
    """
    
    case_id = "550e8400-e29b-41d4-a716-446655440000"
    visa_type_id = "660e8400-e29b-41d4-a716-446655440001"
    
    # Step 1: Load case facts
    case_facts = RuleEngineService.load_case_facts(case_id)
    print(f"Case Facts: {case_facts}")
    
    # Step 2: Load active rule version
    rule_version = RuleEngineService.load_active_rule_version(visa_type_id)
    if not rule_version:
        print("No active rule version found")
        return
    
    print(f"Using Rule Version: {rule_version.id} (Effective from: {rule_version.effective_from})")
    
    # Step 3: Evaluate all requirements
    evaluation_results = RuleEngineService.evaluate_all_requirements(
        rule_version,
        case_facts
    )
    
    # Step 4: Aggregate results
    result = RuleEngineService.aggregate_results(evaluation_results, rule_version)
    
    print(f"Final Outcome: {result.outcome}")
    print(f"Confidence: {result.confidence:.2%}")


def example_evaluate_single_requirement():
    """
    Example: Evaluate a single requirement (for testing).
    """
    from rules_knowledge.selectors.visa_requirement_selector import VisaRequirementSelector
    
    requirement_id = "770e8400-e29b-41d4-a716-446655440002"
    case_facts = {
        "salary": 42000,
        "age": 29,
        "nationality": "NG",
        "has_sponsor": True
    }
    
    requirement = VisaRequirementSelector.get_by_id(requirement_id)
    
    result = RuleEngineService.evaluate_requirement(requirement, case_facts)
    
    print(f"Requirement: {result['requirement_code']}")
    print(f"Passed: {result['passed']}")
    print(f"Missing Facts: {result['missing_facts']}")
    
    return result

