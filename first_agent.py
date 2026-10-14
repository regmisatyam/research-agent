from pathlib import Path

from pydantic import SecretStr
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.workspace import DockerWorkspace

llm = LLM(
    usage_id="research-agent",
    model="openai/llm1",
    base_url="http://172.40.1.35/ai/v1",
    api_key=SecretStr("local-no-key"),
    native_tool_calling=True,
    max_input_tokens=24000,
    max_output_tokens=4096,
    temperature=0,
    timeout=180,
    num_retries=2,
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ],
)

print("Starting Docker workspace...", flush=True)

with DockerWorkspace(
    server_image="ghcr.io/openhands/agent-server:latest-python",
    platform="linux/arm64",
    host_port=8010,
) as workspace:
    print("Checking model access from Docker...", flush=True)

    connection = workspace.execute_command(
        "python -c \"import urllib.request; "
        "print(urllib.request.urlopen("
        "'http://172.40.1.35/ai/v1/models', timeout=20"
        ").status)\""
    )
    print(connection.stdout)
    if connection.exit_code != 0:
        raise RuntimeError(
            f"Docker cannot reach the model server:\n{connection.stderr}"
        )

    conversation = Conversation(
        agent=agent,
        workspace=workspace,
    )

    try:
        conversation.send_message(
            "Use your tools to create /tmp/sum_numbers.py. "
            "The program must calculate the sum of integers from 1 to 100 "
            "and print only the numerical result. "
            "Execute the program, inspect its output, and fix any errors. "
            "Finish after confirming the result. Do not install dependencies."
        )
        conversation.run()

        # Check the program ourselves after the agent finishes.
        result = workspace.execute_command("python /tmp/sum_numbers.py")
        print("\nIndependent verification:", result.stdout.strip())

        if result.exit_code != 0 or result.stdout.strip() != "5050":
            raise RuntimeError(
                f"Verification failed:\n{result.stdout}\n{result.stderr}"
            )

        source = workspace.execute_command("cat /tmp/sum_numbers.py")
        if source.exit_code != 0:
            raise RuntimeError("Could not retrieve the generated program.")

        Path("generated_sum_numbers.py").write_text(source.stdout)
        print("PASS — saved generated_sum_numbers.py on your Mac.")
    finally:
        conversation.close()
