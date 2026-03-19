import { spawn } from 'child_process';

const RMMZ_PROJECT_PATH = "C:/Users/hirak/Documents/RMMZ/Project1";

async function callMcpTool(name: string, args: any) {
  return new Promise((resolve) => {
    const child = spawn('node', ['./build/index.js'], {
      env: { ...process.env, RMMZ_PROJECT_PATH },
      stdio: ['pipe', 'pipe', 'inherit']
    });

    const request = {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name,
        arguments: args
      }
    };

    child.stdout.on('data', (data) => {
      const response = JSON.parse(data.toString());
      resolve(response);
      child.kill();
    });

    child.stdin.write(JSON.stringify(request) + '\n');
  });
}

async function main() {
  console.log("Applying game settings via MCP...");

  // ヒロイン設定
  await callMcpTool("update_actor_name", { id: 1, name: "リア" });

  // 変数設定 (エロゲ用)
  const variables = [
    { id: 1, name: "好感度" },
    { id: 2, name: "淫乱度" },
    { id: 3, name: "絶頂回数" },
    { id: 4, name: "露出度" }
  ];

  for (const v of variables) {
    await callMcpTool("update_system_array", { type: "variables", id: v.id, name: v.name });
  }

  // スイッチ設定
  const switches = [
    { id: 1, name: "Hイベント進行中" },
    { id: 2, name: "目隠し状態" },
    { id: 3, name: "全裸状態" }
  ];

  for (const s of switches) {
    await callMcpTool("update_system_array", { type: "switches", id: s.id, name: s.name });
  }

  console.log("Done!");
}

main().catch(console.error);
