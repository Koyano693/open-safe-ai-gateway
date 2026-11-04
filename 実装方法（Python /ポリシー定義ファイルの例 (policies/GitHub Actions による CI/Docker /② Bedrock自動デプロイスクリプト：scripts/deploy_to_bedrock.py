import os
import sys
import yaml
import boto3
from botocore.exceptions import ClientError

def load_policy(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deploy():
    guardrail_id = os.environ.get("BEDROCK_GUARDRAIL_ID")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    
    if not guardrail_id:
        print("[ERROR] BEDROCK_GUARDRAIL_ID is not set.")
        sys.exit(1)

    policy = load_policy("policies/guardrail-config.yaml")
    client = boto3.client("bedrock", region_name=aws_region)

    content_config = [{"type": cf["type"], "inputStrength": cf["inputStrength"], "outputStrength": cf["outputStrength"]} for cf in policy.get("content_filters", [])]
    pii_config = [{"type": pii["type"], "action": pii["action"]} for pii in policy.get("pii_entities", [])]
    topics_config = [{"name": t["name"], "definition": t["description"], "examples": ["例"], "type": "DENY"} for t in policy.get("denied_topics", [])]
    cg_config = [{"type": cg["type"], "threshold": cg["threshold"]} for cg in policy.get("contextual_grounding", [])]

    try:
        print(f"[INFO] Updating Bedrock Guardrail ID: {guardrail_id}...")
        client.update_guardrail(
            guardrailIdentifier=guardrail_id,
            name=policy.get("policy_name"),
            description=policy.get("description"),
            contentPolicyConfig={"filtersConfig": content_config},
            sensitiveInformationPolicyConfig={"piiEntitiesConfig": pii_config},
            topicPolicyConfig={"topicsConfig": topics_config},
            contextualGroundingPolicyConfig={"filtersConfig": cg_config},
            blockedInputMessaging="プロンプトはセキュリティポリシーによりブロックされました。",
            blockedOutputsMessaging="出力はグラウンディングまたはセキュリティポリシーによりブロックされました。"
        )
        print("[SUCCESS] Guardrail configuration updated.")

        version_resp = client.create_guardrail_version(
            guardrailIdentifier=guardrail_id,
            description="Auto-deployed via GitHub Actions PaC"
        )
        print(f"[SUCCESS] New version published: {version_resp.get('version')}")

    except ClientError as e:
        print(f"[ERROR] AWS API Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
