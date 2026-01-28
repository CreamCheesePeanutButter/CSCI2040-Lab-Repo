import fs from "fs";

const FILE_PATH = "./src/backend/catalog.csv";

export function readCatalog() {
  const data = fs.readFileSync(FILE_PATH, "utf-8");
  const lines = data.split("\n").slice(1);
  return lines
    .filter(Boolean)
    .map(line => {
      const [id, name, description] = line.split(",");
      return { id, name, description };
    });
}

export function saveCatalog(items) {
  const header = "id,name,description\n";
  const rows = items
    .map(i => `${i.id},${i.name},${i.description}`)
    .join("\n");
  fs.writeFileSync(FILE_PATH, header + rows);
}
