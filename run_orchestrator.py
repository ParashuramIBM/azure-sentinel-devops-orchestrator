import asyncio
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator

class PipelineTrigger:
    def __init__(self, code_changes, deployment_context):
        self.code_changes = code_changes
        self.deployment_context = deployment_context


async def main():
    orchestrator = DevOpsOrchestrator()

    pipeline_trigger = PipelineTrigger(
        code_changes={"files": ["app.py"], "summary": "Deploy update"},
        deployment_context={
            "changes": ["service config update"],
            "target_resources": ["resource-group"]
        }
    )

    result = await orchestrator.execute_pipeline(pipeline_trigger)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
