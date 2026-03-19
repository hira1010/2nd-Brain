import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs/promises";
import * as path from "path";

const PROJECT_PATH = process.env.RMMZ_PROJECT_PATH || "C:/Users/hirak/Documents/RMMZ/Project1";
const DATA_PATH = path.join(PROJECT_PATH, "data");

class RmmzServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "rmmz-mcp-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    
    this.server.onerror = (error) => console.error("[MCP Error]", error);
    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: "get_actors",
          description: "Get list of actors from the RPG Maker MZ project",
          inputSchema: { type: "object", properties: {} },
        },
        {
          name: "update_actor_name",
          description: "Update the name of a specific actor",
          inputSchema: {
            type: "object",
            properties: {
              id: { type: "number", description: "Actor ID" },
              name: { type: "string", description: "New name for the actor" },
            },
            required: ["id", "name"],
          },
        },
        {
          name: "get_switches",
          description: "Get list of switches defined in the project",
          inputSchema: { type: "object", properties: {} },
        },
        {
          name: "get_variables",
          description: "Get list of variables defined in the project",
          inputSchema: { type: "object", properties: {} },
        },
        {
          name: "update_system_array",
          description: "Update a switch or variable name at a specific index",
          inputSchema: {
            type: "object",
            properties: {
              type: { type: "string", enum: ["switches", "variables"] },
              id: { type: "number" },
              name: { type: "string" },
            },
            required: ["type", "id", "name"],
          },
        },
        {
          name: "list_maps",
          description: "List all maps in the project",
          inputSchema: { type: "object", properties: {} },
        },
        {
          name: "get_map",
          description: "Get detailed data for a specific map",
          inputSchema: {
            type: "object",
            properties: {
              id: { type: "number", description: "Map ID (e.g. 1 for Map001.json)" },
            },
            required: ["id"],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case "get_actors":
          return await this.handleGetActors();
        case "update_actor_name":
          return await this.handleUpdateActorName(request.params.arguments as any);
        case "get_switches":
          return await this.handleGetSystemArray("switches");
        case "get_variables":
          return await this.handleGetSystemArray("variables");
        case "update_system_array":
          return await this.handleUpdateSystemArray(request.params.arguments as any);
        case "list_maps":
          return await this.handleListMaps();
        case "get_map":
          return await this.handleGetMap(request.params.arguments as any);
        default:
          throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${request.params.name}`);
      }
    });
  }

  private async handleGetActors() {
    try {
      const content = await fs.readFile(path.join(DATA_PATH, "Actors.json"), "utf-8");
      const actors = JSON.parse(content);
      return {
        content: [{ type: "text", text: JSON.stringify(actors.filter((a: any) => a !== null), null, 2) }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error reading Actors.json: ${error.message}` }],
        isError: true,
      };
    }
  }

  private async handleUpdateActorName(args: { id: number; name: string }) {
    try {
      const filePath = path.join(DATA_PATH, "Actors.json");
      const content = await fs.readFile(filePath, "utf-8");
      const actors = JSON.parse(content);
      
      const actor = actors.find((a: any) => a && a.id === args.id);
      if (!actor) {
        return {
          content: [{ type: "text", text: `Actor with ID ${args.id} not found.` }],
          isError: true,
        };
      }

      actor.name = args.name;
      await fs.writeFile(filePath, JSON.stringify(actors, null, 0)); // RMMZ usually saves with no indentation or some specific format, but the editor can handle standard JSON.
      
      return {
        content: [{ type: "text", text: `Successfully updated actor ${args.id} name to "${args.name}".` }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error updating Actor: ${error.message}` }],
        isError: true,
      };
    }
  }

  private async handleGetSystemArray(key: "switches" | "variables") {
    try {
      const content = await fs.readFile(path.join(DATA_PATH, "System.json"), "utf-8");
      const system = JSON.parse(content);
      const list = system[key] || [];
      const formatted = list.map((name: string, index: number) => ({ id: index, name: name || "(None)" }));
      return {
        content: [{ type: "text", text: JSON.stringify(formatted.filter((i: any) => i.id > 0), null, 2) }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error reading System.json: ${error.message}` }],
        isError: true,
      };
    }
  }

  private async handleUpdateSystemArray(args: { type: "switches" | "variables"; id: number; name: string }) {
    try {
      const filePath = path.join(DATA_PATH, "System.json");
      const content = await fs.readFile(filePath, "utf-8");
      const system = JSON.parse(content);
      
      if (!system[args.type]) system[args.type] = [];
      
      while (system[args.type].length <= args.id) {
        system[args.type].push("");
      }
      
      system[args.type][args.id] = args.name;
      await fs.writeFile(filePath, JSON.stringify(system, null, 0));
      
      return {
        content: [{ type: "text", text: `Successfully updated ${args.type} ${args.id} to "${args.name}".` }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error updating System: ${error.message}` }],
        isError: true,
      };
    }
  }

  private async handleListMaps() {
    try {
      const content = await fs.readFile(path.join(DATA_PATH, "MapInfos.json"), "utf-8");
      const maps = JSON.parse(content);
      return {
        content: [{ type: "text", text: JSON.stringify(maps.filter((m: any) => m !== null), null, 2) }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error reading MapInfos.json: ${error.message}` }],
        isError: true,
      };
    }
  }

  private async handleGetMap(args: { id: number }) {
    try {
      const fileName = `Map${args.id.toString().padStart(3, '0')}.json`;
      const content = await fs.readFile(path.join(DATA_PATH, fileName), "utf-8");
      const map = JSON.parse(content);
      return {
        content: [{ type: "text", text: JSON.stringify(map, null, 2) }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Error reading ${args.id}: ${error.message}` }],
        isError: true,
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("RMMZ MCP Server running on stdio");
  }
}

const server = new RmmzServer();
server.run().catch(console.error);
