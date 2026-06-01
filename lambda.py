import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Parses structural AWS Config JSON rules payloads transmitted via EventBridge 
    and validates security state definitions.
    """
    logger.info("Received raw system configuration event envelope:")
    logger.info(json.dumps(event, indent=2))
    
    try:
        detail = event.get('detail', {})
        resource_id = detail.get('resourceId', 'Unknown-Resource-ID')
        compliance = detail.get('newEvaluationResult', {}).get('complianceType', 'UNKNOWN')
        
        logger.info(f"Evaluating target context resource: {resource_id} | Status: {compliance}")
        
        # Structure payload downstream data context for step function transitions
        return {
            "status": "NON_COMPLIANT_RESOURCE_DETECTED",
            "targetSecurityGroup": resource_id,
            "executionStatus": "PROCEED_TO_AUTOMATION_REMEDIATION"
        }
    except Exception as err:
        logger.error(f"Error handling configuration input pipeline analysis: {str(err)}")
        raise err