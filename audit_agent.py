from datetime import datetime, timezone
from pathlib import Path
import json

from pydantic import SecretStr
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.workspace import DockerWorkspace

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "workspace"
LOGS = ROOT / "logs"
WORK.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
events_path = LOGS / f"{run_id}-events.jsonl"
status_path = LOGS / f"{run_id}-status.json"

def save_status(status, **details):
    status_path.write_text(json.dumps({
        "run_id": run_id,
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        **details,
    }, indent=2))

def record_event(event):
    with events_path.open("a") as stream:
        stream.write(event.model_dump_json() + "\n")

task = (ROOT / "AUDIT_TASK.md").read_text()

llm = LLM(
    usage_id="research-agent",
    model="openai/llm1",
    base_url="http://172.40.1.35/ai/v1",
    api_key=SecretStr("local-no-key"),
    native_tool_calling=True,
    max_input_tokens=80000,
    max_output_tokens=4096,
    temperature=0,
    timeout=600,
    num_retries=2,
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ],
)

save_status("starting")
print(f"Run: {run_id}", flush=True)
print(f"Research files: {WORK}", flush=True)

try:
    with DockerWorkspace(
        server_image="ghcr.io/openhands/agent-server:latest-python",
        platform="linux/arm64",
        host_port=8010,
        working_dir="/workspace",
        volumes=[f"{WORK}:/workspace:rw"],
    ) as workspace:
        # Confirm that container writes reach the Mac.
        check = workspace.execute_command(
            "printf 'connected' > /workspace/.mount-check"
        )
        if check.exit_code != 0:
            raise RuntimeError(f"Shared-folder check failed: {check.stderr}")
        if (WORK / ".mount-check").read_text() != "connected":
            raise RuntimeError("Shared-folder contents did not match.")

        conversation = Conversation(
            agent=agent,
            workspace=workspace,
            callbacks=[record_event],
            max_iteration_per_run=40,
            stuck_detection=True,
        )

        try:
            save_status("running")
            conversation.send_message(task)
            conversation.run()
            save_status(
                "agent_run_returned",
                execution_status=str(conversation.state.execution_status),
            )
        finally:
            conversation.close()

except BaseException as error:
    save_status("interrupted_or_failed", error=str(error))
    raise

print("\nRun ended. Research files remain in:", WORK)
print("Inspect the report and measurements before accepting conclusions.")
