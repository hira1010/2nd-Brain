const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname);
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
};

http
  .createServer((request, response) => {
    const filePath = resolveRequestPath(request.url);

    if (!filePath) {
      sendText(response, 403, "forbidden");
      return;
    }

    fs.readFile(filePath, (error, data) => {
      if (error) {
        sendText(response, 404, "not found");
        return;
      }

      response.writeHead(200, { "Content-Type": getContentType(filePath) });
      response.end(data);
    });
  })
  .listen(5179, "127.0.0.1");

function resolveRequestPath(url) {
  const route = decodeURIComponent(url.split("?")[0]);
  const filePath = route === "/" ? path.join(root, "index.html") : path.resolve(root, route.replace(/^\/+/, ""));

  if (!filePath.startsWith(root + path.sep) && filePath !== root) {
    return "";
  }

  return filePath;
}

function getContentType(filePath) {
  return types[path.extname(filePath)] || "application/octet-stream";
}

function sendText(response, status, message) {
  response.writeHead(status, { "Content-Type": "text/plain; charset=utf-8" });
  response.end(message);
}
