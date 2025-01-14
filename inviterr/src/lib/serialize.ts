import type { Document, WithId } from "mongodb";

export function serializeMongo(document: WithId<Document> | null): Record<string, any> | null {
  if (!document) return null;

  return { ...document, _id: document._id.toString() };
}